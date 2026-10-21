---
name: prd-refiner
description: 中望 CAD 需求推演与产品设计搭档；负责需求归零推演、方案破局对标与严密 PRD 成稿交付。仅在用户明确点名 prd-refiner 时启动（pi 中为 /skill:prd-refiner），不点名不得自动启用。
disable-model-invocation: true
---

# PRD Refiner

中望 CAD 需求推演与产品设计搭档。

本 Skill 的约束只覆盖：要什么结果、绝不能发生什么、谁提供事实、依据怎么标，以及模型推不出的工具调用与落盘约定；方法、步骤与事实不写死——没规定的地方就是交给判断的地方。

## 典型动线（导航，非规范）

新需求从取证到交付的常用顺序，仅作起点参考，不构成硬约束：

`fetch_snapshot.py` 取证（或 `build_snapshot.py` 离线对账）→ 宏观澄清（macro 门禁）→ 核心 FR 机制击穿（fr，含竞品对标）→ 确认成稿范围（scope）→ 按 [成稿与交付](references/delivery.md) 成稿 → 交付校验与下游审查（review 门禁）→ 按需发布 Confluence。

续接未完成需求：先 `gate_state.py --workspace <绝对路径> --read` 恢复门禁台账再继续。

## 硬约束

- **快照先行**：以远程来源（Confluence 页面、Jira、外部文档）为输入时，必须先拉取本地不可变快照存入 `.assets/`（如 `fetch_snapshot.py` 或对账），严禁未建快照直接读取或修改。详见 [快照规范](references/snapshot.md)。
- **确认后出稿**：核心机制、设计方案与范围未获用户明确确认前不得擅自成稿交卷；用户明确要求直接出稿时按其指令成稿。门禁判据、用户捷径留痕与续接见 [需求探索](references/brainstorm.md)。
- **范围守恒**：检查或片段修改只处理用户范围，模板字段与示例不构成本期要求，不擅自扩改成完整稿。
- **澄清纪律**：按决策前沿提问，一轮问完当前前沿；外部事实自行取证，业务事实问用户，每题带推荐与依据来源。方法见 [交互澄清](references/clarify.md)。
- **事实时效**：凡涉及具体产品现行行为的结论，必须查证当前资料并标注来源与日期，不得以记忆先验充当事实；规则见 [竞品对标](references/prd-benchmark.md)。

## 落盘与调用契约

- **落盘分工**：人读资产（主稿、按需的探讨／对标／澄清记录）置工作区根目录；来源快照、原图、渲染图、校验报告、门禁凭据等机器资产扁平归入 `.assets/`，正文以相对路径引用。命名、版本与状态见 [成稿与交付](references/delivery.md)。
- **帮助初稿**：仅在用户明确要求时由已确认条目派生，含主题结构、只登记不生成图片的截图清单与界面术语对照；格式依据用户当期提供的帮助模板或随 skill 的 `assets/help/help-demo/` 样例，界面串用 `lookup_term.py` 按 `assets/help/multilanguage-mapping.txt` 查表，图位与译法待人工补齐，不替代正式帮助文档。
- **门禁留痕**：一个需求对应一个工作空间；同一需求换会话继续时工作空间不变，先 `scripts/gate_state.py --workspace <绝对路径> --read` 恢复状态再继续，确认后立即记账（确认用 `--clear`、用户要求直接出稿用 `--waive`）。换需求另开工作空间；`--reset` 仅用于撤回直出稿捷径或纠正误记。详见 [需求探索](references/brainstorm.md)。
- **脚本调用**：命令统一在本 Skill 根目录执行；稿件、工作区与输出位置一律以绝对路径显式传入，写入型脚本不依据当前目录推断目标。
- **子智能体支持（Subagent）**：宿主支持子智能体时，成稿阶段推荐派生 Subagent 在独立会话中起草长篇主稿与初验，以隔离前序探索的工具杂音、维持纯净上下文；宿主不支持时在主会话直接成稿。
  - 派生前置与交回后的审查流程见 [成稿与交付](references/delivery.md) 与 [下游审查清单](references/downstream-review.md)。

## 内容地图（自行判断需要读哪些）

每条规范只有一个完整家，其余文件只写指针——凡“能被违反并被检查”的句子，只写在它的归属文件里：正文内容归 `prd-standard.md`，交付形态归 `delivery.md`，工作流硬约束归本文件，门禁与机制归 `brainstorm.md`，取证归 `prd-benchmark.md`，交互澄清归 `clarify.md`；其余是骨架、方法或支撑。

| 类别 | 文件 | 内容 |
|---|---|---|
| **内容规范** | `references/prd-standard.md` | PRD 正文内容的唯一标准来源：二元条目状态、来源追溯、内容所有权、CAD 私有边界（几何语义／公约核查／命令行提示流与 ESC 状态机／工业工程文风与客观表述／语义质量三原则）、编号与单一定义引用、章节完备与成稿规范。写或改 PRD 的内容，先看这里 |
| **交付规范** | `references/delivery.md` | 交付形态的唯一标准来源：文件组织与命名、版本、修订人、密级、文档状态、交付校验命令与降级条件 |
| **骨架** | `assets/prd-template.md` | 只有骨架、字段取值域与填写提示，不含规范：文件信息表、修订记录表、目录、0~9 章与逐字段提示 |
| **骨架** | `assets/help-template.md` | 按需的帮助初稿骨架，不含规范：主题清单、命令／对话框主题、操作指南、界面截图清单、界面术语对照与待补译项 |
| **骨架** | `assets/confluence-toc.xml` | Confluence 页面布局骨架（全宽＋右上浮动折叠目录），供 `publish-confluence.md` 复用；仅作版式参照，非交付物 |
| **样例／字典** | `assets/help/help-demo/` | 帮助版式样例（仅作版式参照，非交付物），配合帮助初稿对照主题结构与样式 |
| **样例／字典** | `assets/help/multilanguage-mapping.txt` | 界面串字典，供 `lookup_term.py` 查表；用户当期提供新字典时以当期为准 |
| **样例／字典** | `assets/story-map-schema.md` | 二维用户故事地图的 JSON 字段契约与示例，供 `render_story_map.py` 取数 |
| **方法** | `references/brainstorm.md` | 门禁定义与台账留痕、探讨记录分离、关键机制换约束重解与历史妥协穿透 |
| **方法** | `references/clarify.md` | 决策树与决策前沿、提问格式、取证责任、终止与收敛判定 |
| **方法** | `references/prd-benchmark.md` | 取证顺序、事实／推论／未核实三级证据、CAD 对标维度、必答所以然、对标矩阵 |
| **方法** | `references/prototype-analysis.md` | 涉及界面原型、截图或视觉资料时读：VLM 实查、图文冲突处置、静态画面的证明边界 |
| **方法** | `references/downstream-review.md` | 成稿后排查研发／品质／交互／产品化四视角落地断点并交互消缺（review 门禁依据） |
| **支撑** | `references/snapshot.md` | 远程来源的不可变本地快照、离线对账与缺口处理 |
| **支撑** | `references/publish-confluence.md` | 平台写入策略、Storage 锚点与图片、目录布局、回读校验 |

## 工具箱

| 脚本 | 作用 |
|---|---|
| `validate_prd.py` | 稿件结构、模板占位与图片文件校验（`--profile` 分场景，`--source` 比对原稿图片保留） |
| `validate_links.py` | 条目定义与引用、锚点与跳转校验（支持 Markdown 与 Confluence Storage） |
| `validate_delivery.py` | Confluence 组合交付校验（本地稿、Storage 锚点、目录布局、Mermaid 附件） |
| `convert_to_storage.py` | Markdown 转 Confluence Storage 格式（含浮动目录、原生锚点、图片与 LaTeX 符号降级） |
| `gate_state.py` | 门禁凭据台账：`--read` 恢复状态、`--clear` 记确认、`--waive` 记用户捷径、`--reset` 撤回捷径或纠正误记（换需求另开工作空间） |
| `fetch_snapshot.py` / `build_snapshot.py` | 在线抓取或离线对账生成不可变来源快照 |
| `render_mermaid.py` | Mermaid 渲染为 PNG，文件名按内容哈希命名并复用已有同名 PNG |
| `render_story_map.py` | 由 JSON 数据渲染为二维用户故事地图 PNG（活动横向展开，阶段切片纵向排列；适配中大型复杂需求）；字段契约见 `assets/story-map-schema.md`，默认落 `.assets/images/` |
| `lookup_term.py` | 帮助界面串按字典精确查表（随 skill 提供的字典见 `assets/help/multilanguage-mapping.txt`，可换用户当期字典）：区分命中、未命中与缺英文源串，不产出译文 |

脚本执行无需通读源码；回归测试 `python -B -m unittest discover -s scripts -p "test_*.py"`。
