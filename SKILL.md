---
name: prd-refiner
description: 中望 CAD 需求探讨、原型设计与 PRD 编写辅助工具；提供需求深度分析思路、50 个 <cad-*> 原型组件库、高信息密度 PRD 规范、工作区文件约定与自动化交付脚本。仅在用户明确点名 prd-refiner 时启动（pi 中为 /skill:prd-refiner），不点名不得自动启用。
disable-model-invocation: true
---

# PRD Refiner

辅助产品经理（PM）探讨中望 CAD 功能方案、用 `<cad-*>` 组件库构建原型、编写高信息密度 PRD 并交付 Confluence。

## 协作方式（按需执行）

根据 PM 当前的意图灵活响应，只做当前需要的事：
- **只探讨方案**：帮 PM 理清真实使用场景、指出既有做法痛点并提供更顺手的设计方案；
- **只画/改原型**：读取 `references/interaction-design.md`，直接用 `<cad-*>` 组件生成或修改 `prototype.html`；
- **只写/改文档**：读取 `references/prd-standard.md`，编写或修改对应的 Markdown 文档；
- **完整需求推进**：按需串联方案探讨、原型构建、规格提炼与合龙校验（支持单文件直接维护，也支持跨多会话按 `features/FR-xxx/` 分片推进）。

## 核心要求

- **深度思考，不照搬旧界面**：探讨功能时，不要凭经验直接照搬传统 CAD 软件的现成弹窗。先想清楚：**设计师在什么场景下用它？数据从哪来？做完这步操作后他的下一步是什么？以前的做法笨在哪（如多层弹窗、繁琐向导、缺少预览）？** 顺着真实目的给出更少步骤、更直观的方案（见 [需求探索](references/brainstorm.md)）。
- **原型纯粹且用标准组件**：`prototype.html` 只画纯粹的 CAD 界面，使用内置的 50 个 `<cad-*>` 官方组件构建；若现有组件满足不了某个特殊交互，用语义化 `<cad-*>` 标签加 `status="draft"` 与 `label="用途说明"`，汇总到 `Missing_Components.md` 交设计师补充 Figma（见 [交互与原型设计](references/interaction-design.md)）。
- **PRD 高信息密度，图文不重复**：
  - 正文面向研发与品质（QA），只写确认的 **ZWCAD 软件行为与规则**（围绕 `CAD 终端设计师`、`ZWCAD 系统`、`图纸／图元／系统变量` 展开）；
  - **原型上已经能看懂的常规控件（普通按钮、常规文案、布局尺寸）不在文档里重复罗列**；正文只写静态画面看不见的**特殊逻辑、跨控件联动、CAD 底层边界（命令与 `-CMD`、系统变量、特殊图层/块/UCS、ESC 回滚与 Undo）及量化验收标准**（见 [内容约定](references/prd-standard.md)）。
- **事实取证与清晰提问**：能通过代码、组件表或公开资料查到的事实自己查（分析外部产品现行行为须查证当前资料并注明来源与日期，见 [竞品对标](references/prd-benchmark.md)）；需要 PM 拍板的业务取舍，提问时带上推荐做法和理由（见 [交互澄清](references/clarify.md)）。以 Confluence/Jira 为输入时，先用脚本拉取 `.assets/` 快照（见 [来源快照](references/snapshot.md)）。

## 文件存放位置（防止乱放）

- **单文件模式**（优化已有 PRD 或轻量需求）：直接读写 `<工作区>/<需求名>.md`。
- **多模块分片模式**（大型重构或多会话并行推进，详见 [成稿与交付](references/delivery.md)）：
  - `<工作区>/00_需求总览.md`：全局背景、范围、3.1 功能清单总表及全局章节；
  - `<工作区>/features/FR-xxx_<名称>/prototype.html` 与 `spec.md`：单个功能的原型与规格；
  - `<工作区>/Missing_Components.md`：缺失的 `status="draft"` 组件汇总表；
  - `<工作区>/<需求名>.md`：由 `assemble_prd.py` 合龙生成的完整 PRD。
- **公共资源与按需文件**：
  - 组件库运行时置 `<工作区>/.assets/nova-proto/`；图片（状态截图、Mermaid 渲染图、快照原图）统一置 `<工作区>/.assets/images/`，文档内用相对路径引用；
  - 帮助初稿仅在 PM 明确要求时生成（骨架见 `assets/help-template.md`，版式参照 `assets/help/help-demo/`），界面词条用 `lookup_term.py` 查 `assets/help/multilanguage-mapping.txt`，不自行翻译。
- **脚本执行位置**：所有 Python 脚本统一在本 Skill 根目录下运行，工作区与文件路径传入绝对路径。

## 参考文档（按当前任务选读）

| 场景 | 文件 | 说明 |
|---|---|---|
| **写 PRD 正文** | `references/prd-standard.md` | 高信息密度原则、CAD 常见防漏清单（命令/变量/图层/块/ESC/Undo）、编号与引用规范 |
| **画 `<cad-*>` 原型** | `references/interaction-design.md` | 50 个 `<cad-*>` 官方组件与属性速查表、`status="draft"` 缺件标记、从原型提炼重点规格 |
| **探讨功能方案** | `references/brainstorm.md` | 从真实场景与下一步动作出发思考方案，以及多会话分片目录如何配合 |
| **向 PM 提问确认** | `references/clarify.md` | 先定大方向再问细节、带推荐答案提问、把结论落到原型与文档 |
| **管理目录与合龙** | `references/delivery.md` | 单文件与分片双模式目录结构、版本状态、`assemble_prd.py` 合龙与静态校验命令 |
| **成稿自检** | `references/downstream-review.md` | 从研发（C++/Qt5）、品质（QA）、交互、产品化四个角度检查有无遗漏（参考 [下游审查清单](references/downstream-review.md)） |
| **做竞品调研** | `references/prd-benchmark.md` | 区分事实与推论、CAD 对比维度、对标表格写法 |
| **拉取远程快照** | `references/snapshot.md` | 把 Confluence/Jira 页面抓取为本地 `.assets/` 快照 |
| **发布到 Confluence** | `references/publish-confluence.md` | Markdown 转 Confluence Storage 格式、上传图片附件与回读校验 |
| **模板与内置资源** | `assets/prd-template.md` | PRD 章节骨架、内置组件库 `assets/nova-proto/`（`cad-design-tokens.css` 与 `cad-components.js`）、`assets/help-template.md`、`assets/confluence-toc.xml`、`assets/help/help-demo/`、`assets/help/multilanguage-mapping.txt` |

## 脚本工具箱

| 脚本 | 作用 |
|---|---|
| `assemble_prd.py` | 同步 `.assets/nova-proto/` 组件库；检查 `features/FR-*/prototype.html` 是否混入原生裸 HTML、汇总 `status="draft"` 缺失组件至 `Missing_Components.md`，并将 `00_需求总览.md` 与各 `spec.md` 合龙为完整 PRD |
| `validate_prd.py` | 检查 PRD 章节完整性、未清理的模板占位符、本地图片路径、禁用词与交互卡覆盖情况 |
| `validate_links.py` | 检查条目编号定义与同页锚点跳转是否有效（支持 Markdown 与 Confluence Storage） |
| `validate_delivery.py` | 发布 Confluence 前后的组合校验（正文、锚点、目录布局与图片附件） |
| `convert_to_storage.py` | 将 Markdown 转换为 Confluence Storage XML（含浮动目录、锚点与图片转换） |
| `fetch_snapshot.py` / `build_snapshot.py` | 抓取或构建 Confluence/Jira 本地不可变快照 |
| `render_mermaid.py` | 将 Markdown 中的 Mermaid 流程图渲染为 `.assets/images/` 下的 PNG 图片 |
| `lookup_term.py` | 按多语言字典（`assets/help/multilanguage-mapping.txt`）精确查表核对界面中英文词条 |

回归测试：`python -B -m unittest discover -s scripts -p "test_*.py"`。
