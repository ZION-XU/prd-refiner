# 交互与原型设计（Nova-Proto 驱动规范）

仅在设计单个功能（FR）的界面交互、编写本地 HTML 原型或从原型提炼功能分片 `spec.md` 时读取。

## 一、 原型即真值（Prototype-as-SSOT）

桌面 CAD 的功能细节由离散的“界面状态 × 视口/命令行事件”决定。为杜绝纯文字空谈与人机对话幻觉，本 Skill 采用 **本地 Web Components 原型驱动（Nova-Proto）** 机制：

1. **对话只改原型与规则，不直接湊正文**：产品经理（PM）与 AI 的多轮探讨，唯一目标是打磨该功能分片目录下的 `prototype.html` 并敲定不可见的 CAD 内核契约（命令名、系统变量、DWG 持久化、ESC 回滚与 Undo 分组）。
2. **从 `prototype.html` 逆向提炼 `spec.md`**：原型定稿后，AI 直接解析 `prototype.html` 中的 `<cad-*>` 组件树与导出的状态截图，一对一生成 `features/FR-xxx/spec.md`；**严禁从聊天记录中摘抄推进策略或测试指令写入 PRD**。
3. **方案取舍内嵌于原型**：关键方案对比（如“老版实现弊端 vs 本次破局解法”）直接写在 `prototype.html` 顶部的可折叠洞察卡片（`.design-insights-card`）中，评审时打开 HTML 即可同屏对照，无需维护易污染上下文的外部闲聊记录。

---

## 二、 Nova-Proto 组件库白名单与缺件提单铁律

所有本地 HTML 原型基于公司 Figma 组件库 1:1 转换的 **Nova-Proto Web Components 设计系统**构建。为实现跨机器开箱即用与便携分发，核心运行时已随本 Skill 内置于 `assets/nova-proto/`（包含 `cad-design-tokens.css` 与 `cad-components.js`）：

- **工作区运行时自包含注入**：在初始化工作区或运行 `scripts/assemble_prd.py --workspace <工作区绝对路径> --init-only` 时，脚本自动将 `assets/nova-proto/` 下的 CSS 与 JS 同步至 `<工作区>/.assets/nova-proto/`；
- **标准相对路径引用**：各分片 `features/FR-xxx/prototype.html` 统一使用相对路径引用工作区内的运行时，严禁写死个人电脑的本地绝对路径（确保整个需求目录打包发给任何同事或研发双击即可运行）：
  ```html
  <link rel="stylesheet" href="../../.assets/nova-proto/cad-design-tokens.css">
  <script src="../../.assets/nova-proto/cad-components.js"></script>
  ```

### 1. 官方标准组件白名单（Level 1）
构建交互界面时，必须优先使用已封装的官方 Web Components 标签：
- **容器与导航**：`<cad-dialog>`、`<cad-tabs>`、`<cad-form-group>`、`<cad-divider>`
- **数据录入**：`<cad-input>`、`<cad-select>`、`<cad-checkbox>`、`<cad-radio>`、`<cad-switch>`、`<cad-slider>`、`<cad-picker>`、`<cad-file-loader>`
- **动作与展示**：`<cad-button>`、`<cad-icon>`、`<cad-table>`、`<cad-tag>`、`<cad-alert>`、`<cad-banner>`

### 2. 零裸 HTML 容忍度
- **严禁手搓野生控件**：原型 DOM 中严禁直接使用未封装的原生交互标签（`<input>`、`<button>`、`<select>`、`<textarea>` 数量必须为 `0`）。
- 合龙与审计脚本（`scripts/assemble_prd.py`）会自动扫描所有 `prototype.html` 的组件化覆盖率，发现裸 HTML 标签即报错阻断。

### 3. 缺件阻断与设计师提单机制（Level 3 Draft）
当某个 CAD 交互场景在现有官方 `<cad-*>` 组件库中找不到对应组件时，**严禁 AI 私自用 `<div>` 拼凑伪造**，必须执行以下标准动作：
1. **显式草稿标记**：在原型中使用语义化扩展标签并必须携带 `status="draft"` 属性（例如 `<cad-draft-linetype-preview status="draft" label="线型预览"></cad-draft-linetype-preview>`），触发运行时右上角紫色草稿角标。
2. **登记缺失组件需求单**：立即在工作区根目录的 `Missing_Components.md`（或由 `scripts/assemble_prd.py` 自动扫描汇总）登记给 UI 设计师的补充需求：
   - 所属功能分片（`FR-xxx`）与使用场景；
   - 建议组件名称与对应的 Qt5 目标控件类型；
   - 所需尺寸、属性插槽及交互状态（默认/悬停/禁用/报错）。
   待设计师在 Figma 补齐并经 `sync_figma.py` 同步入库后，再移除 `status="draft"` 转正。

---

## 三、 逐 FR 独立分片工作流（支持多会话并发）

每个功能在 `features/FR-xxx_<功能名>/` 独立目录下闭环，不同会话各自操作不同目录，互不干扰：

1. **建立/迭代 `prototype.html`**：
   - 使用 `<cad-*>` 组件拼装对话框或面板状态机；
   - 编写关键状态切换逻辑（如模式切换、单选联动置灰、异常校验态）。
2. **挂标号导出状态帧图（`fr-xxx-s1.png`）**：
   - 在各关键状态画面（`FR-001-S1` 默认态、`FR-001-S2` 联动/预览态等）的核心控件旁标注清晰的数字标号（①、②、③...）；
   - 使用无头浏览器将各状态渲染导出为高清本地图片（存入 `.assets/images/fr-001-s1.png`），并用 VLM 实查确认画面无截断、文字与标号清晰（静态画面只证明可见布局，不脑补画面未呈现的规则）。
3. **提炼生成单功能规格 `spec.md`**：
   - 对照 `prototype.html` 与状态帧图，按 [模板](../assets/prd-template.md) 第 3 章单功能结构写出内聚规格：
     - **1. 入口与流程简述**：菜单/Ribbon/命令行入口、前置条件、主流程、命令行等价（`-CMD`）；
     - **2. 界面与交互说明（交互卡）**：置顶嵌入状态帧图（含帧 ID `FR-001-S1`），顺着标号 ①、②、③ 逐项写明控件名称（含 `<cad-*>` 标签名）、默认值、取值范围/枚举、操作后的界面变化与命令行回显；
     - **3. 业务规则与异常处理（内聚 `BR-xxx`）**：系统变量双向绑定、特殊图层（锁定/冻结）与复杂图元（块/Xref）边界、ESC 取消回滚与 Undo 分组；
     - **4. 验收标准（内聚 `AC-xxx`）**：覆盖关键状态迁移与逆向异常的 Given / When / Then 判据。

---

## 四、 轻量与无界面功能的交互卡表达

1. **纯命令行或轻量视口交互**：无需构建复杂对话框 HTML 时，交互卡可采用经典表格形态（含“状态与事件表”和“帧 ID 画面表”）；涉及橡皮筋、捕捉追踪等视口动态反馈时，用起始、拖动中、完成的多帧序列加文字标注表达。
2. **确无交互的后台功能**：纯数据迁移、后台计算或接口改动，显式写一行 `交互卡：未涉及（具体原因说明）`，原因不得写“无”等空话。
