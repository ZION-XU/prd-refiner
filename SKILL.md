---
name: prd-refiner
description: 中望 CAD 需求推演、Nova-Proto 原型驱动与分片并发 PRD 交付搭档；负责需求第一性归零推演、基于 Web Components (<cad-*>) 的本地交互原型构建、单功能分片内聚提炼与合龙交付。仅在用户明确点名 prd-refiner 时启动（pi 中为 /skill:prd-refiner），不点名不得自动启用。
disable-model-invocation: true
---

# PRD Refiner

中望 CAD 需求推演、Nova-Proto 原型驱动与分片并发 PRD 交付搭档。

## 核心工作流（支持跨周、多会话并发）

1. **取证与总览初始化**：远程来源先用 `fetch_snapshot.py`（或 `build_snapshot.py`）建立 `.assets/` 不可变快照；在工作区根目录维护 `00_需求总览.md`（背景、目标、Mermaid 业务总体流程、范围与 3.1 功能清单表）。
2. **多会话分片并发（单功能闭环）**：每个功能在 `features/FR-xxx_<名称>/` 独立目录下推进，不同会话各改各的分片目录，互不干扰：
   - **归零推演与方案破局**：穿透第一性归零四问，将“旧实现痛点 vs 新方案最短路径”写入该功能 `prototype.html` 顶部的 `.design-insights-card`；
   - **Nova-Proto 原型构建**：严格使用 `<cad-*>` 官方组件编写 `prototype.html`（严禁裸 HTML；缺失组件标 `status="draft"` 并汇总至 `Missing_Components.md` 提单给设计师）；
   - **标号截图与内聚规格提炼**：导出带 ①②③ 标号的状态帧图（`.assets/images/fr-xxx-s1.png`），直接从定稿的 `prototype.html` 与确认的 CAD 底层规则提炼生成 `features/FR-xxx_<名称>/spec.md`（内聚入口、交互卡、业务规则 BR 与验收标准 AC）。
3. **一键合龙与校验交付**：运行 `assemble_prd.py` 审计所有原型组件覆盖率并将各 FR 分片合龙为完整主稿 `<需求名>.md` → 执行 `validate_prd.py` 与 `validate_links.py` → 对照 [下游审查清单](references/downstream-review.md) 四视角消缺 → 按需发布 Confluence。

## 硬约束

- **双重主体解耦与元话语物理隔离（最高红线）**：严格区分对话窗口中的**产品经理（PM / 需求发起人）**与使用 ZWCAD 的**CAD 终端设计师**。PRD 正文只描述 `CAD 终端设计师`、`ZWCAD 系统` 与 `图纸/数据` 的行为；PM 与 AI 在会话中的协作策略、测试计划、推进方式（如“影子伴跑”、“分步测试”等过程元话语）严禁写入 PRD。规范见 [内容约定](references/prd-standard.md) §1。
- **原型即真值与组件库白名单**：交互细节必须由本地 `prototype.html`（基于 `Nova-proto` `<cad-*>` 组件库）驱动，严禁手搓原生 `<input>/<button>/<select>/<textarea>` 裸标签；缺失组件必须标注 `status="draft"` 并登记至 `Missing_Components.md` 交设计师补充 Figma。规范见 [交互与原型设计](references/interaction-design.md)。
- **单功能内聚与分片隔离**：每个 FR 的交互卡、业务规则（BR）与验收标准（AC）在各自的 `features/FR-xxx/spec.md`（及主稿第 3 章对应小节）内就地闭环，不跨大章节拆散跳转；多会话并发时单功能会话只读写所属 FR 目录。规范见 [成稿与交付](references/delivery.md)。
- **归零推演与 CAD 防漏**：拒绝做题家式盲从旧实现，关键机制穿透第一性归零四问（见 [需求探索](references/brainstorm.md)）；自动核查 CAD 三要素公约、命令行状态机、ESC 回滚、Undo 分组与特殊图层/块边界（见 [内容约定](references/prd-standard.md) §2）。
- **快照先行与事实时效**：以 Confluence/Jira 为输入时先拉取 `.assets/` 本地快照（见 [来源快照](references/snapshot.md)）；涉及外部产品现行行为的结论须查证当前资料并标明来源与日期（见 [竞品对标](references/prd-benchmark.md)）。
- **澄清纪律与范围守恒**：外部事实 AI 自查，业务事实问 PM，每题带推荐与依据（见 [交互澄清](references/clarify.md)）；检查或片段修改只处理指定范围。

## 落盘与调用契约

- **落盘分工**：`00_需求总览.md`、`Missing_Components.md`、合龙主稿 `<需求名>.md` 及按需的竞品分析/帮助初稿置工作区根目录；各功能分片（`prototype.html` + `spec.md`）置 `features/FR-xxx_<名称>/`；快照与图片（`.assets/images/`）置 `.assets/`，正文以相对路径引用。
- **帮助初稿**：仅在 PM 明确要求时由已确认条目派生（骨架见 `assets/help-template.md`，版式参照 `assets/help/help-demo/`），界面串用 `lookup_term.py` 按 `assets/help/multilanguage-mapping.txt` 精确查表，不自行翻译。
- **脚本调用**：命令统一在本 Skill 根目录执行；工作区、稿件与输出位置一律以绝对路径显式传入。

## 内容地图（按任务自行判断选读）

| 类别 | 文件 | 内容 |
|---|---|---|
| **内容规范** | `references/prd-standard.md` | PRD 正文唯一标准：双重主体解耦与元话语隔离、CAD 领域防漏检查单、单功能内聚编号、Mermaid 流程图规范、交互卡完备判据 |
| **原型规范** | `references/interaction-design.md` | Nova-Proto 原型驱动规范：`<cad-*>` 组件白名单、0 裸 HTML 铁律、`status="draft"` 缺件提单、①②③ 标号截图与 `spec.md` 提炼 |
| **交付规范** | `references/delivery.md` | 分片并发目录结构、`assemble_prd.py` 合龙、版本与状态、静态校验命令 |
| **探索方法** | `references/brainstorm.md` | 跨周多会话并发状态感知、第一性归零推演四问、方案洞察内嵌于原型 |
| **澄清方法** | `references/clarify.md` | 决策树与决策前沿、提问格式、取证责任划分、结论入原型与分片 |
| **对标方法** | `references/prd-benchmark.md` | 事实／推论／未核实三级证据、CAD 对标维度、必答所以然、对标矩阵 |
| **下游审查** | `references/downstream-review.md` | 研发（C++/Qt5）／品质／交互／产品化四视角落地断点排查与就地消缺 |
| **快照支撑** | `references/snapshot.md` | Confluence/Jira 远程来源的不可变本地快照与离线对账 |
| **平台发布** | `references/publish-confluence.md` | Confluence 写入策略、Storage 锚点与图片转换、浮动目录布局与回读校验 |
| **骨架与资源** | `assets/prd-template.md` | 1~7 章高内聚 PRD 骨架（含 `<!-- FEATURES_INSERT_POINT -->` 与单功能内聚模板）、内置组件库运行时 `assets/nova-proto/`（`cad-design-tokens.css` 与 `cad-components.js`）、`assets/help-template.md`、`assets/confluence-toc.xml`、`assets/help/help-demo/`、`assets/help/multilanguage-mapping.txt` |

## 工具箱

| 脚本 | 作用 |
|---|---|
| `assemble_prd.py` | 扫描 `features/FR-*/prototype.html` 审计 `<cad-*>` 组件覆盖率（拦截裸 HTML，汇总 `draft` 组件至 `Missing_Components.md`），并将 `00_需求总览.md` 与各 FR 的 `spec.md` 合龙为完整 PRD |
| `validate_prd.py` | 稿件章节结构、模板占位、本地图片、竞品名禁用与交互卡覆盖率校验 |
| `validate_links.py` | 条目定义与引用、同页锚点跳转校验（支持 Markdown 与 Confluence Storage） |
| `validate_delivery.py` | Confluence 组合交付校验（本地稿、Storage 锚点、浮动目录布局、图片与 Mermaid 附件） |
| `convert_to_storage.py` | Markdown 转 Confluence Storage 格式（含浮动目录、原生锚点、图片映射与 LaTeX 符号降级） |
| `fetch_snapshot.py` / `build_snapshot.py` | 在线抓取或离线对账生成不可变来源快照 |
| `render_mermaid.py` | 将 Markdown 中的 Mermaid 流程图渲染为内容哈希命名的本地 PNG（落 `.assets/images/`） |
| `lookup_term.py` | 帮助界面串按字典精确查表（默认 `assets/help/multilanguage-mapping.txt`），不自行产出译文 |

回归测试：`python -B -m unittest discover -s scripts -p "test_*.py"`。
