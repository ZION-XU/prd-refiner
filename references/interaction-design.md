# 交互与原型设计（Nova-Proto 驱动规范）

仅在设计单个功能（FR）的界面交互、编写本地 HTML 原型或从原型提炼功能规格时读取。

## 一、 原型与规格正文的分工（高信息密度原则）

本地 Web Components 原型（`prototype.html`）与 PRD 正文（`spec.md` / 主稿第 3 章）分工明确、互不重复：

| 载体 | 承载的专属信息 | 消费对象 |
|---|---|---|
| **本地原型与状态帧图**<br>（`prototype.html` + `fr-xxx-sx.png`） | **纯粹的 CAD 视觉布局与常规控件外观**：对话框结构、控件方位、文案排布、尺寸间距、常规按钮/输入框外观及所使用的 `<cad-*>` 组件标签（原型只画纯粹界面，不塞方案说明卡片） | PM 评审、UI 设计师核对、前端/Qt 界面布局映射 |
| **功能规格正文**<br>（交互卡与内核规则） | **静态画面看不见的特殊逻辑与增量契约**：特殊控件的数据源与默认记忆、复杂取值校验与恢复、跨控件联动算法、命令行 `-CMD` 等价流、DWG 图元数据契约、CAD 特殊环境边界与 ESC/Undo 事务 | C++/Qt 核心研发编写业务逻辑、QA 编写测试用例 |

---

## 二、 使用 `figma-components-web` MCP 构建原型（针对 `prototype.html`）

本地 HTML 原型基于公司 Figma 组件库 1:1 转换的 **Nova-Proto Web Components (`<cad-*>`) 设计系统**构建。组件查询、图标检索、设计变量（Design Tokens）与原型校验已封装在 **`figma-components-web` MCP 服务**中（同时本 Skill 在 `assets/nova-proto/` 下内置了 `cad-design-tokens.css` 与 `cad-components.js` 运行时兜底）：

### 1. 标准构建流程（按需调用 MCP 工具）
编写或修改 `prototype.html` 时，直接调用 `figma-components-web` MCP 工具，无需死记硬背组件属性：

1. **获取原型骨架并注入运行时**：
   - 调用 `get_prototype_scaffold(title="功能名称", workspace_dir="<工作区绝对路径>", asset_prefix="...")`（根目录原型用 `.assets/nova-proto`，`features/FR-xxx/` 子目录原型用 `../../.assets/nova-proto`；离线或无 MCP 环境时可运行 `python scripts/assemble_prd.py --workspace <工作区绝对路径> --init-only` 注入运行时）。
   - 若属于常见复合场景（如图层设置弹窗、项目浏览器、状态栏），可调用 `get_scene_recipe` 参考标准结构。
2. **按需查询组件、图标与样式变量**：
   - **查组件**：调用 `search_components(query="表格/弹窗/树...")` 或 `list_cad_components(category="...")` 找到所需 `<cad-*>` 标签；
   - **查属性与调用范例**：对目标组件调用 `get_component_spec(tag_name="cad-xxx")` 获取完整支持属性（`supported_attributes`）与标准 HTML 示例（需要查看内部插槽或事件细节时可调 `get_component_module`）；
   - **查图标与颜色变量**：需要图标时调用 `search_icons(query="...")`（从 339+ 官方 CAD/BIM 图标中获取 `<cad-icon name="...">`）；需要写局部布局样式时调用 `get_design_tokens` 使用标准 CSS 变量。
3. **校验原型与标记缺失组件（`status="draft"`）**：
   - **零原生裸 HTML 交互控件**：界面中的按钮、输入、下拉、复选、表格、弹窗一律使用 `<cad-*>` 组件，不混写原生 `<button>`、`<input>`、`<select>`、`<textarea>`；
   - **缺失组件标记**：当官方 50 个 `<cad-*>` 组件均无法满足某个特定 CAD 交互时，使用语义化的自定义 `<cad-*>` 标签，并显式添加 `status="draft"` 与 `label="用途说明"`（例如 `<cad-linetype-preview status="draft" label="线型实时预览"></cad-linetype-preview>`）；
   - **静态自检**：生成代码后调用 MCP 的 `validate_prototype_html`（或在合龙时运行 `scripts/assemble_prd.py`），自动检查标签拼写并将 `status="draft"` 组件汇总至工作区根目录的 `Missing_Components.md` 供 UI 设计师补齐 Figma。

---

## 三、 从原型提炼单功能规格（只写特殊与增量逻辑）

从定稿的 `prototype.html` 与状态截图（`fr-xxx-s1.png`）提炼功能规格时，按 [模板](../assets/prd-template.md) 第 3 章结构分为四个部分：

### 1. 入口与命令契约
专注写清：**怎么触发这个功能，以及无弹窗命令行怎么走**。
- 命令英文名、命令别名（PGP）、菜单与功能区路径、是否支持先选对象再执行命令（Noun-Verb）；
- 命令行 `-CMD` 的完整提示顺序、关键字分支与默认回车行为。

### 2. 状态画面与重点交互逻辑（交互卡）
置顶嵌入状态截图（`FR-xxx-Sx`）。**原型已经清楚表达的常规控件（如普通按钮、常规文本标签、静态布局）无需逐一点名说明**；仅针对存在**特殊业务规则、复杂联动或本次改动**的重点控件，写清：
1. **数据源与默认记忆**：初始值取自哪个系统变量（如 `CTABLESTYLE`）、当前图元属性，还是跨命令记住上次输入值？
2. **特殊取值校验与恢复**：非显而易见的范围约束、精度单位转换，以及越界/非法输入时的拦截与恢复方式。
3. **跨控件联动与状态迁移**：修改该项如何触发其他控件的动态重算、置灰禁用或切换进入视口交互状态？

### 3. CAD 内核与环境边界（`BR-xxx`）
专注写清：**脱离界面控件之后，CAD 内核如何处理图元、几何与特殊环境**。
- **图元与持久化契约**：生成的底层实体类型（如 `AcDbTable`）、DXF 组码、扩展数据及系统变量同步时机；
- **复杂几何与环境边界**：在锁定/冻结/关闭图层、块编辑器（BEDIT）、外部参照（Xref）、UCS 坐标系或极端缩放比例下的处理规则；
- **中断与事务边界**：各阶段按 `ESC` 键的现场清理与回滚范围，以及 `Ctrl+Z`（Undo）的撤销分组。

### 4. 验收标准（`AC-xxx`）
专注写清：**QA 用什么具体样本测试，以及检验什么量化结果**（Given / When / Then）。
