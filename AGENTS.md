# AGENTS.md

本仓库是 `prd-refiner` 技能本体（SKILL.md 是唯一规范源，内容以它为准）。只在用户明确点名 prd-refiner（pi 中为 `/skill:prd-refiner`）时才会作为工作上下文加载；通常不直接改动本仓库，而是调用脚本处理用户工作区。

## 关键事实

- **语言**：规范、文档、模板与交付物全部为中文。本技能针对中望 CAD。
- **入口**：`SKILL.md` 定义硬约束、落盘契约与内容地图；规范分布在各 `references/*.md`，每个规范只有一个「家」，其余文件只写指针——改规范先找到归属文件。
- **纯标准库**：`scripts/*.py` 只用 Python 标准库与互导（无第三方依赖，无 lockfile、无构建）。Python 3.10 已验证。
- **运行前提**：脚本在导入时互引（如 `validate_links.py` 从 `validate_prd.py` 导入），命令一律在**技能仓库根目录**执行；工作区、稿件、输出路径一律用绝对路径显式传入，写入型脚本不按当前目录推断目标。
- **测试**：`python -B -m unittest discover -s scripts -p "test_*.py"`。改动脚本、模板或文档后均需执行回归测试验证。
- **模板纯洁与规范隔离**：`assets/prd-template.md` 纯粹是字段骨架，告诉读者“格子填什么”，严禁包含具体实现方案、工具脚本名称（如 `*.py`）或规范要求；所有关于“应当怎么写、必须怎样、工具如何调用”的规范一律且只能写在 `references/prd-standard.md`，模板只写超链接指针。依靠 Agent 架构规则与语义审查保障纯洁性，不为特定中文语句在测试中维护脆弱且易膨胀的字符串白名单。

## 脚本速查（详见 SKILL.md 工具箱）

| 脚本 | 职责 | 关键参数 |
|---|---|---|
| `validate_prd.py` | 稿件结构/占位/图片校验 | `--profile {template,draft,existing}`、`--source`、`--image-policy` |
| `validate_links.py` | 条目定义引用、锚点校验（Markdown 或 Confluence Storage） | `--format {markdown,storage}`、`--reference-policy location` |
| `validate_delivery.py` | Confluence 组合交付校验 | `--workspace` 必填，Storage 正文跑两遍（提交稿 + 服务端回读） |
| `convert_to_storage.py` | Markdown 转 Confluence Storage 格式 | `--output` 必填，`--layout {floating,inline}`，含 LaTeX 降级与 XML 校验 |
| `gate_state.py` | 门禁台账（`macro→fr→scope→review` 顺序） | `--workspace` 必填，`--read`/`--clear <gate>`/`--waive`/`--reset`，写入必带 `--evidence` |
| `fetch_snapshot.py` | 在线抓 Confluence 快照 | `--page-id`、`--workspace`；自动复用 MCP/环境凭据 |
| `build_snapshot.py` | 离线对账建快照 | `--json-file`/`--source-file`、`--workspace`、`--page-id`、`--page-version`；缺图/重名/不安全引用一律失败不降级 |
| `render_mermaid.py` | Mermaid 渲染为哈希命名 PNG | `--output-dir`、`--force` |
| `lookup_term.py` | 界面串按字典精确查表，不产出译文 | `--mapping`（绝对路径）、`--terms`/`--terms-file` |

## 易错点

- **快照先行**：以 Confluence/Jira/外部文档为输入必须先建 `.assets/` 不可变快照，未建快照不得直接读取或修改远程来源。`manifest.json` 为快照完成标记。
- **落盘分工**：人读资产（主稿、探讨/对标/澄清记录）在**工作区根目录**；机器资产（快照、渲染图、校验报告、`gates.json`）在**工作区 `.assets/`**，正文用相对路径引用。不把机器资产散落在工作区根目录，也不把主稿写进 `.assets/`。
- **范围守恒**：校验发现的缺陷只修用户范围内部分；范围外来稿问题只报告不扩改。
- **主稿命名**：单文件，名称确定用 `<需求名>.md`，未定用 `prd.md`；版本从 `0.1` 起，每次修订递增末级并在修订记录追加一行，不覆盖历史。
- **成稿与交付门禁**：macro/fr/scope 三处确认（或用户直接出稿 waive）后才成稿；成稿经静态校验后，完成四视角审查与消缺并取得 review 确认方可交付；确认后立即记台账，换需求先 `--reset`，续接先 `--read`。
- **事实时效**：涉及竞品/产品现行行为的结论必须查证当前资料并标注来源与日期，不得以记忆先验充当事实。