# 交互与原型设计（Nova-Proto 驱动规范）

仅在设计单个功能（FR）的界面交互、编写本地 HTML 原型或从原型提炼功能分片 `spec.md` 时读取。

## 一、 原型与规格正文的正向分工（高信息密度原则）

本 Skill 采用 **本地 Web Components 原型（`prototype.html`）+ 高密度工程规格（`spec.md`）** 双件套协同，二者职责严格正交、互不重复：

| 载体 | 正向承载的专属信息 | 消费对象 |
|---|---|---|
| **本地原型与状态帧图**<br>（`prototype.html` + `fr-xxx-sx.png`） | **视觉布局与组件选型**：对话框结构、控件方位、文案排布、尺寸间距、所使用的 `<cad-*>` 组件标签及方案对比洞察（`.design-insights-card`） | PM 评审、UI 设计师核对、前端/Qt 界面布局映射 |
| **功能规格正文**<br>（`spec.md` 交互卡与规则） | **画面看不见的工程契约**：控件的数据源与默认值记忆、合法取值域与失焦校验、跨控件联动算法、命令行 `-CMD` 等价流、DWG 图元数据契约、CAD 特殊环境边界与 ESC/Undo 事务 | C++/Qt 核心研发编写业务逻辑、QA 编写测试用例 |

---

## 二、 Nova-Proto 组件库构建规范（针对 `prototype.html`）

所有本地 HTML 原型基于公司 Figma 组件库 1:1 转换的 **Nova-Proto Web Components 设计系统**构建。核心运行时已随本 Skill 内置于 `assets/nova-proto/`（`cad-design-tokens.css` 与 `cad-components.js`）：

1. **工作区运行时自包含注入**：初始化工作区或运行 `scripts/assemble_prd.py --workspace <工作区绝对路径> --init-only` 时，自动将 CSS 与 JS 同步至 `<工作区>/.assets/nova-proto/`。各分片 `features/FR-xxx/prototype.html` 统一使用相对路径引用：
   ```html
   <link rel="stylesheet" href="../../.assets/nova-proto/cad-design-tokens.css">
   <script src="../../.assets/nova-proto/cad-components.js"></script>
   ```
2. **官方标准组件组合（Level 1）**：在 `prototype.html` 中使用已注册的 18 个官方 `<cad-*>` 组件拼装界面：
   - **容器与导航**：`<cad-dialog>`、`<cad-tabs>`、`<cad-form-group>`、`<cad-divider>`
   - **数据录入**：`<cad-input>`、`<cad-select>`、`<cad-checkbox>`、`<cad-radio>`、`<cad-switch>`、`<cad-slider>`、`<cad-picker>`、`<cad-file-loader>`
   - **动作与展示**：`<cad-button>`、`<cad-icon>`、`<cad-table>`、`<cad-tag>`、`<cad-alert>`、`<cad-banner>`
3. **缺失组件标记与提单（Level 3 Draft）**：遇到现有官方组件未覆盖的特殊控件，在 `prototype.html` 中使用自定义 `<cad-*>` 标签并标注 `status="draft"` 与 `label="用途说明"`；运行 `scripts/assemble_prd.py` 自动扫描汇总至 `Missing_Components.md` 供设计师补齐 Figma 组件库。

---

## 三、 单功能分片 `spec.md` 的四部分正向职责

从定稿的 `prototype.html` 与状态截图（`fr-xxx-s1.png`）提炼 `features/FR-xxx/spec.md` 时，按 [模板](../assets/prd-template.md) 第 3 章结构分为四个职责完全正交的部分，每条信息只在其唯一归属处定义一次：

### 1. 入口与命令契约
专注定义：**如何触发功能，以及无弹窗命令行怎么走**。
- 写明命令英文名、命令别名（PGP）、菜单与功能区路径、前置选择集支持（先选后执行 Noun-Verb vs 先执行后选 Verb-Noun）；
- 写明命令行 `-CMD` 的完整提示文案序列、关键字分支与按 `Enter`/空格的默认行为。

### 2. 状态画面与控件逻辑（交互卡）
置顶嵌入带数字标号（①、②、③）的状态帧图（`FR-xxx-Sx`）。每个标号只针对有业务逻辑的控件，正向回答 **3 个数据与状态问题**：
1. **数据源与默认值**：初始值取自哪个系统变量（如 `CTABLESTYLE`）、当前图元属性，还是记住上一次会话输入值？
2. **合法取值域与校验恢复**：数据类型（整数/浮点/枚举）、闭区间范围、精度与量纲单位（图纸单位 vs 视口像素），以及输入越界或非法字符时的拦截、提示与失焦恢复值。
3. **联动计算与状态迁移**：修改该控件会触发哪些关联控件的数值重算、显隐/禁用态切换，或点击后调起哪个子命令/进入哪个视口交互态？

### 3. CAD 内核与环境边界（`BR-xxx`）
专注定义：**脱离界面控件之后，CAD 内核如何处理图元、几何与特殊环境**。
- **图元与持久化契约**：生成的底层实体类型（如 `AcDbTable`）、DXF 组码、扩展数据（XData/Xrecord）及与系统变量的双向同步时机；
- **复杂几何与环境边界**：在锁定/冻结/关闭图层、块编辑器（BEDIT）、外部参照（Xref）、非 WCS（UCS 用户坐标系）或极端缩放比例下的处理算法与保持项；
- **中断与事务边界**：各阶段按 `ESC` 键的现场清理与回滚范围，以及 `Ctrl+Z`（Undo）的原子事务分组。

### 4. 验收标准（`AC-xxx`）
专注定义：**QA 用什么具体样本测试，以及检验什么量化真值**。
- `Given` 给出可构造的图纸环境与初始参数；`When` 给出明确操作序列或异常边界输入；`Then` 给出可测量的图元特性值、几何坐标尺寸或系统变量结果。

---

## 四、 轻量与无界面功能的交互卡表达

1. **纯命令行或纯视口动态交互**：对于视口橡皮筋拖拽、捕捉追踪等交互，使用多状态帧图（或状态事件表）配合视口几何计算公式、HUD 读数规则及极值保护阈值进行定义。
2. **纯后台与数据功能**：无界面与命令行交互的纯数据迁移或接口功能，直接写一行 `交互卡：未涉及（具体原因说明）`。
