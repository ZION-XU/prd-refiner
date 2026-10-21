# PRD Refiner

中望 CAD 需求推演与产品设计搭档：辅助产品人员做需求归零推演、方案破局对标与严密 PRD 成稿交付。Skill 的约束只覆盖模型推不出的部分——要什么结果、绝不能发生什么、谁提供事实、依据怎么标，以及工具调用与落盘约定；方法、步骤与事实不写死，没规定的地方交给模型自行判断。

## 设计元规则

**规范的存在理由只有一个——矫正大模型的系统性缺陷；凡是模型涌现能力能覆盖的，一个字不写。**

- 写规范，只针对系统性缺陷：懒惰（最短路径，没确认就交卷）→ 门禁强制确认；幻觉（拿记忆先验当现行事实）→ 快照先行与三级证据；假装确定 → 条目二元状态；长上下文注意力漂移 → 状态落盘与续接；范围漂移 → 范围守恒；自查遗漏 → 脚本兑底；脑补 → VLM 实查。怎么理解需求、怎么组织文章、遇到没见过的输入怎么办——这些模型本来就比人强，一条规范都没有。
- **新增规范前先自问：这是模型的系统性缺陷，还是它本来就会？** 是缺陷才配拥有规范；是“本来就会”就一个字不加——写了反而占上下文，还会产生暗示效应（枚举了音频怎么办，模型就会推断其他输入也该有规定），抑制它本来的判断力。
- 实测中发现某条规范对应的是“模型本来就会的事”，删掉它——规范集应越测越瘦，而不是越测越胖。

## 安装与使用

将本目录拷贝（或通过软链接/目录联接）到对应宿主的 Skill 目录下，仅在用户明确点名时启动，不点名不得自动启用。Python 3.10+ 用于标准库校验器；本地资料任务无需企业账号，远程能力依赖宿主已有凭据。

### 常用宿主 Skill 路径

将本仓库目录直接拷贝为对应宿主路径下的 `prd-refiner` 文件夹即可：

- **Codex**：`~/.codex/skills/prd-refiner`（调用：对话中明确指明使用 `prd-refiner`，或在 Plan 模式下使用 `$prd-refiner`）
- **ZCode**：`~/.zcode/skills/prd-refiner`（调用：对话中明确点名 `prd-refiner`）
- **Pi**：`~/.agents/skills/prd-refiner`（调用：输入 `/skill:prd-refiner`）
- **Antigravity**：`~/.gemini/config/skills/prd-refiner`（调用：对话中指明或输入 `/prd-refiner`）

> 如需单项目隔离生效，亦可直接放置在项目根目录的 `.agents/skills/prd-refiner`（或 `.codex/skills/`、`.zcode/skills/`）下。

### 使用范例

```text
/prd-refiner 一起优化这份 PRD，先讨论关键问题。
/prd-refiner 只检查歧义和遗漏，不改文件。
/prd-refiner 修改 FR-002，保持其他功能并检查相关验收。
```

新需求从取证到交付的典型动线：快照取证 → 宏观澄清（macro 门禁）→ 核心 FR 机制击穿（fr，含竞品对标）→ 确认成稿范围（scope）→ 成稿 → 交付校验与下游审查（review 门禁）→ 按需发布 Confluence。一个需求对应一个工作空间，门禁确认由 `scripts/gate_state.py` 记入该工作空间的台账；同一需求换会话续接（如背景确认后另开会话推进具体功能）时工作空间不变，`--read` 即恢复，不必重复盘问，也不需要重置台账；换需求则另开工作空间。

完整稿按统一模板交付工作区 Markdown：主稿为单文件（名称确定用 `<需求名>.md`，未定用 `prd.md`），版本从 `0.1` 起递增并追加修订记录；探讨结论、竞品分析与澄清决策独立落盘根目录供用户查阅及跨会话流转。来源快照、原图、Mermaid 渲染图、门禁凭据、校验报告等机器文件统一扁平放入 `.assets/`。Confluence 来源必须先建不可变本地快照再分析；写回时使用 Storage、浮动折叠目录、原生锚点和附件图片。凡涉及具体产品现行行为的结论必须查证当前资料并标注来源与日期，不得以记忆先验充当事实。用户指定目的地或配套要求时遵循其选择。

帮助初稿只由已确认条目派生：主题结构、只登记不生成图片的界面截图清单与界面术语对照，图位和译法留待人工在真实软件操作中补齐；界面串用 `scripts/lookup_term.py` 按字典精确查表——优先用户当期提供的字典，否则用随 skill 的 `assets/help/multilanguage-mapping.txt`；查不到就列为待补译，不由模型自译。

## 目录结构

```text
prd-refiner/
├─ SKILL.md                 入口：硬约束、落盘契约与内容地图（读哪些由模型判断）
├─ README.md                本文件：设计元规则、安装使用、目录结构、维护验证
├─ AGENTS.md                仓库维护说明与脚本速查
├─ references/              规范与方法，每条规范只有一个完整家
│  ├─ prd-standard.md       内容规范：正文内容的唯一标准来源
│  ├─ delivery.md           交付规范：交付形态的唯一标准来源
│  ├─ brainstorm.md         方法：门禁定义与台账留痕、探讨记录分离、机制换约束重解
│  ├─ clarify.md            方法：决策树与决策前沿、提问格式、取证责任、收敛判定
│  ├─ prd-benchmark.md      方法：三级证据、CAD 对标维度、必答所以然、对标矩阵
│  ├─ prototype-analysis.md 方法：VLM 实查、图文冲突处置、静态画面的证明边界
│  ├─ downstream-review.md  方法：四视角落地断点排查与消缺（review 门禁依据）
│  ├─ snapshot.md           支撑：远程来源的不可变本地快照、离线对账与缺口处理
│  └─ publish-confluence.md 支撑：平台写入策略、Storage 锚点与图片、回读校验
├─ assets/                  骨架、版式参照与字典（不含规范）
│  ├─ prd-template.md       主稿骨架、字段取值域与填写提示
│  ├─ help-template.md      帮助初稿骨架（主题结构、截图清单、界面术语对照）
│  ├─ story-map-schema.md   二维用户故事地图 JSON 字段契约与示例
│  ├─ confluence-toc.xml    Confluence 页面布局骨架，供 publish-confluence.md 复用
│  └─ help/
│     ├─ help-demo/         帮助版式样例（Commands/、images/、styles/，仅作版式参照）
│     └─ multilanguage-mapping.txt  界面串字典，供 lookup_term.py 查表
└─ scripts/                 纯标准库 Python，命令在仓库根目录执行
   ├─ validate_prd.py       稿件结构、模板占位与图片校验
   ├─ validate_links.py     条目定义与引用、锚点与跳转校验
   ├─ validate_delivery.py  Confluence 组合交付校验
   ├─ convert_to_storage.py Markdown 转 Confluence Storage（含 LaTeX 降级）
   ├─ gate_state.py         门禁凭据台账：--read／--clear／--waive／--reset
   ├─ fetch_snapshot.py     在线抓取来源形成不可变快照
   ├─ build_snapshot.py     离线对账生成不可变快照
   ├─ render_mermaid.py     Mermaid 渲染为确定性 PNG
   ├─ render_story_map.py   用户故事地图 JSON 渲染为二维 PNG
   ├─ lookup_term.py        帮助界面串按字典精确查表
   └─ test_*.py             回归测试，覆盖上述脚本与文档架构不变量
```

## 文件与加载

入口 [SKILL.md](SKILL.md) 只维护硬约束、落盘契约与内容地图：写明每个文件里有什么，由模型按任务自行判断需要读哪些，不设“每次必读”。**每条规范只有一个完整家**——凡“能被违反并被检查”的句子只写在归属文件里，其余文件只写指针：正文内容归 `prd-standard.md`，交付形态归 `delivery.md`，工作流硬约束归 SKILL.md，门禁与机制归 `brainstorm.md`，取证归 `prd-benchmark.md`，交互澄清归 `clarify.md`；其余是骨架、方法或支撑。

- [内容约定](references/prd-standard.md)：唯一内容规范——二元条目状态、来源追溯、内容所有权、CAD 私有边界（几何语义／公约核查／命令行提示流与 ESC 状态机／语义质量三原则）、编号与单一定义引用、章节完备与成稿规范。
- [交付规范](references/delivery.md)：唯一交付规范——文件组织与命名、版本、修订人、密级、文档状态、交付校验与降级条件。
- [模板](assets/prd-template.md)：骨架、字段取值域与填写提示（不含规范）。
- [帮助初稿骨架](assets/help-template.md)：帮助主题结构、界面截图清单与界面术语对照的字段提示（不含规范）。
- [需求探索](references/brainstorm.md)：门禁（macro→fr→scope→review）的唯一完整定义与台账留痕、探讨记录分离、关键机制换约束重解与历史妥协穿透。
- [交互澄清](references/clarify.md)：决策树与决策前沿、提问格式、取证责任、终止与收敛判定。
- [竞品对标](references/prd-benchmark.md)：取证责任、事实／推论／未核实三级证据、CAD 对标维度、必答所以然、对标矩阵。
- [原型分析](references/prototype-analysis.md)：VLM 实查、图文冲突处置、静态画面的证明边界。
- [下游审查清单](references/downstream-review.md)：研发／品质／交互／产品化四视角的落地断点排查与消缺（review 门禁依据）。
- [来源快照](references/snapshot.md)：远程来源的不可变本地快照、离线对账与缺口处理。
- [Confluence 写入](references/publish-confluence.md)：仅在用户明确要求写入平台时使用，复用 [布局骨架](assets/confluence-toc.xml)。
- `scripts/`：结构、引用、交付与门禁校验，Storage 格式转换与 LaTeX 符号清洗降级，帮助术语查表，快照抓取与对账，Mermaid 渲染；执行无需通读源码。架构不变量（规范唯一归属、模板不含规范、入口覆盖全部文件）由 `scripts/test_doc_contract.py` 守住。
- [AGENTS.md](AGENTS.md)：仓库维护说明与脚本速查。

## 维护验证

```text
python -B -m unittest discover -s scripts -p "test_*.py"
```

文稿校验命令、降级条件与检查边界见交付规范。静态测试不证明需求正确或宿主对话行为。改动后核对三条路由：内容地图能定位模板与内容约定；Confluence 来源检查需要图片；写入 Confluence 需要平台格式与图片映射。业务资料、生成文稿和分析材料存放仓库外。
