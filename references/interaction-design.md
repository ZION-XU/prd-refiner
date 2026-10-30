# 交互与原型设计（Nova-Proto 驱动规范）

仅在设计单个功能（FR）的界面交互、编写本地 HTML 原型或从原型提炼功能规格时读取。

## 一、 原型与规格正文的正向分工（高信息密度原则）

本 Skill 采用 **本地 Web Components 原型（`prototype.html`）+ 高密度工程规格（`spec.md` / 主稿第 3 章）** 协同，二者职责严格正交、互不重复：

| 载体 | 正向承载的专属信息 | 消费对象 |
|---|---|---|
| **本地原型与状态帧图**<br>（`prototype.html` + `fr-xxx-sx.png`） | **视觉布局与常规控件自明信息**：对话框结构、控件方位、文案排布、尺寸间距、常规按钮/输入框外观、所使用的 `<cad-*>` 组件标签及方案对比洞察（`.design-insights-card`） | PM 评审、UI 设计师核对、前端/Qt 界面布局映射 |
| **功能规格正文**<br>（交互卡与内核规则） | **静态画面看不见的特殊逻辑与增量契约**：特殊控件的数据源与默认记忆、复杂取值校验与恢复、跨控件联动算法、命令行 `-CMD` 等价流、DWG 图元数据契约、CAD 特殊环境边界与 ESC/Undo 事务 | C++/Qt 核心研发编写业务逻辑、QA 编写测试用例 |

---

## 二、 Nova-Proto 50 组件库白名单与属性速查表（针对 `prototype.html`）

所有本地 HTML 原型基于公司 Figma 组件库 1:1 转换的 **Nova-Proto Web Components 设计系统**构建。核心运行时已随本 Skill 内置于 `assets/nova-proto/`（`cad-design-tokens.css` 与 `cad-components.js`，含 5 大类 50 个官方组件 + 舱壁熔断隔离）：

### 1. 运行时自包含注入与相对路径引用
- 初始化工作区或运行 `scripts/assemble_prd.py --workspace <工作区绝对路径> --init-only` 时，自动将 CSS 与 JS 同步至 `<工作区>/.assets/nova-proto/`；
- 原型文件统一使用相对路径引用（分片目录 `features/FR-xxx/prototype.html` 用 `../../.assets/nova-proto/`，根目录原型用 `.assets/nova-proto/`）：
  ```html
  <link rel="stylesheet" href="../../.assets/nova-proto/cad-design-tokens.css">
  <script src="../../.assets/nova-proto/cad-components.js"></script>
  ```

### 2. 官方 50 组件全景白名单与核心属性签名（API Cheat Sheet）

| 分类 | 组件标签 | 对应 Qt5 控件 | 核心支持属性（`observedAttributes`）与用法说明 |
|---|---|---|---|
| **1. 通用基础** | `<cad-button>` | `QPushButton` | `type="primary\|secondary\|text"`, `size="small\|large"`, `disabled` |
| | `<cad-typography>` | `QLabel` | `type="title\|body\|caption"`, `size`, `color`, `weight`, `copyable` |
| | `<cad-divider>` | `QFrame` | `direction="horizontal\|vertical"`, `dashed`, `type` |
| | `<cad-scrollbar>` | `QScrollBar` | `orientation="vertical\|horizontal"`, `theme="light\|dark"` |
| | `<cad-link>` | `QLabel` | `href`, `target`, `disabled`, `underline` |
| | `<cad-tag>` | `QLabel (Tag)` | `color="blue\|green\|orange\|red\|gray"`, `theme="light\|dark\|plain"`, `size` |
| **2. 导航菜单** | `<cad-tabs>` | `QTabWidget` | `type="segmented\|card\|line"`, `value="当前激活值"`, `items='[{"value":"a","label":"标签A"}]'` |
| | `<cad-icon>` | `QIcon` | `name="info\|search\|close\|..."`, `size="14px"`, `color` |
| | `<cad-menu>` | `QMenu` | `open`, `trigger="click\|hover\|contextmenu"` |
| | `<cad-dropdown>` | `QToolButton` | `title`, `disabled`, `placement="bottomLeft\|bottomRight"` |
| **3. 数据录入** | `<cad-input>` | `QLineEdit` | `type="text\|number\|search"`, `value`, `placeholder`, `size="small\|large"`, `prefix-label`, `suffix-label`, `min`, `max`, `step`, `disabled` |
| | `<cad-select>` | `QComboBox` | `value`, `placeholder`, `size="small\|large"`, `disabled`（内部放 `<option>` 或文本） |
| | `<cad-checkbox>` | `QCheckBox` | `checked`, `indeterminate`, `disabled` |
| | `<cad-radio>` | `QRadioButton` | `checked`, `name`, `value`, `disabled` |
| | `<cad-switch>` | `QCheckBox` | `checked`, `disabled` |
| | `<cad-slider>` | `QSlider` | `value`, `min`, `max`, `step`, `show-input`, `disabled` |
| | `<cad-color-picker>` | `QColorDialog` | `value="ByLayer\|#FF0000"`, `disabled` |
| | `<cad-tree>` | `QTreeWidget` | `data='[{"label":"节点","children":[...]}]'`, `checkable` |
| | `<cad-tree-select>` | `QTreeWidget` | `value`, `placeholder`, `disabled` |
| | `<cad-table>` | `QTableWidget` | `cols="4"`, `rows="5"`, `col-width="50"`, `row-height="8"`, `show-title="true"`, `show-header="true"`, `show-summary="false"`, `title-text="标题"`, `headers='["列1","列2"]'`, `data='[["值1","值2"]]'`, `zoom="100"`, `empty="false"` |
| | `<cad-form>` | `QFormLayout` | `layout="horizontal\|vertical"`, `label-width="80px"`, `disabled` |
| | `<cad-form-group>` | `QGroupBox` | `title="分组标题"`, `bg="true\|false"`, `collapsible`, `collapsed`, `size` |
| | `<cad-picker>` | `CAD Picker` | `value`, `placeholder="拾取点/对象"`, `disabled` |
| | `<cad-file-loader>` | `QFileDialog` | `value`, `placeholder="选择或拖拽文件"`, `disabled` |
| | `<cad-material-select>` | `QWidget` | `value`, `disabled` |
| | `<cad-picture>` | `QLabel` | `src`, `alt`, `width`, `height` |
| **4. 数据反馈** | `<cad-dialog>` | `QDialog` | `title="窗口标题"`, `subtitle`, `size="480x240\|480x360\|600x360\|720x600\|840x600\|960x600"`, `width`, `height`, `confirm-text="确定"`, `cancel-text="取消"`, `help-text="帮助"`, `show-help="false"`, `show-footer-help="true"` |
| | `<cad-alert>` | `QMessageBox` | `type="info\|success\|warning\|error"`, `title`, `description`, `multiline`, `confirm-text`, `cancel-text` |
| | `<cad-alert-banner>` / `<cad-banner>` | `QFrame` | `type="info\|success\|warning\|error"`, `title`, `closable` |
| | `<cad-panel>` | `QDockWidget` | `title`, `width`, `dock="left\|right"`, `collapsible`, `collapsed` |
| | `<cad-tooltip>` | `QToolTip` | `title`, `content`, `placement="top\|bottom\|left\|right"` |
| | `<cad-popover>` | `QWidget` | `title`, `trigger="click\|hover"` |
| | `<cad-popconfirm>` | `QMessageBox` | `title`, `ok-text`, `cancel-text` |
| | `<cad-message>` | `Toast` | `type="info\|success\|warning\|error"`, `duration` |
| | `<cad-progress>` | `QProgressBar` | `percent="0~100"`, `stroke-width`, `show-info="true"` |
| | `<cad-filter>` | `FilterBar` | `placeholder` |
| **5. 业务场景** | 平台与专业工具组件 | `QWidget` / `QDockWidget` | `<cad-ribbon active-tab>`、`<cad-quick-nav>`、`<cad-main-toolbar direction>`、`<cad-status-bar coords scale>`、`<cad-command-tool prompt>`、`<cad-property-panel title>`、`<cad-project-browser title>`、`<cad-options-dialog open>`、`<cad-composite-input label value>`、`<cad-wall-tool>`、`<cad-door-tool>`、`<cad-stair-tool>`、`<cad-axis-grid>`、`<cad-family-mgr>` |

### 3. 缺失组件标记与提单（Level 3 Draft）
当上述 50 个官方组件均无法满足某个特定 CAD 交互时，在 `prototype.html` 中使用自定义 `<cad-*>` 标签并显式添加 `status="draft"` 与 `label="用途说明"`；运行 `scripts/assemble_prd.py` 自动扫描汇总至 `Missing_Components.md` 供设计师补齐 Figma。

---

## 三、 单功能规格的四部分正向职责（只写特殊与增量逻辑）

从定稿的 `prototype.html` 与状态截图（`fr-xxx-s1.png`）提炼功能规格时，按 [模板](../assets/prd-template.md) 第 3 章结构分为四个正交部分：

### 1. 入口与命令契约
专注定义：**如何触发功能，以及无弹窗命令行怎么走**。
- 命令英文名、命令别名（PGP）、菜单与功能区路径、前置选择集支持（Noun-Verb vs Verb-Noun）；
- 命令行 `-CMD` 的完整提示文案序列、关键字分支与按 `Enter`/空格的默认行为。

### 2. 状态画面与重点交互逻辑（交互卡）
置顶嵌入状态帧图（`FR-xxx-Sx`）。**原型已经清楚表达的常规控件（如普通按钮、常规文本标签、静态布局）无需逐一点名说明**；仅针对存在**特殊业务规则、复杂联动或本次增量变更**的重点控件，正向回答：
1. **数据源与默认记忆**：初始值取自哪个系统变量（如 `CTABLESTYLE`）、当前图元属性，还是跨命令记住上次输入值？
2. **特殊取值校验与恢复**：非显而易见的范围约束、精度单位转换，以及越界/非法输入时的拦截与恢复策略。
3. **跨控件联动与状态迁移**：修改该项如何触发其他控件的动态重算、置灰禁用或切换进入视口交互状态？

### 3. CAD 内核与环境边界（`BR-xxx`）
专注定义：**脱离界面控件之后，CAD 内核如何处理图元、几何与特殊环境**。
- **图元与持久化契约**：生成的底层实体类型（如 `AcDbTable`）、DXF 组码、扩展数据及系统变量同步时机；
- **复杂几何与环境边界**：在锁定/冻结/关闭图层、块编辑器（BEDIT）、外部参照（Xref）、UCS 坐标系或极端缩放比例下的处理算法与保持项；
- **中断与事务边界**：各阶段按 `ESC` 键的现场清理与回滚范围，以及 `Ctrl+Z`（Undo）的原子事务分组。

### 4. 验收标准（`AC-xxx`）
专注定义：**QA 用什么具体样本测试，以及检验什么量化真值**（Given / When / Then）。
