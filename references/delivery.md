# 成稿与交付

规定分片并发目录契约、一键合龙、版本状态及交付校验流程。

## 1. 工作区双模式组织契约（单文件直改 vs 分片并发合龙）

根据需求规模与协作方式，工作区支持两种组织模式：

### 模式 A：单文件直接维护（适用于已有单文件 PRD 优化、单功能微调或单会话闭环需求）
- 当工作区根目录已存在单文件主稿 `<需求名>.md`（且无 `00_需求总览.md` 与 `features/` 子目录）时，**直接就地读写与更新 `<需求名>.md`**，状态帧图存放在 `.assets/images/`，无需强行拆分为多个分片目录。

### 模式 B：分片并发合龙（适用于跨周、多会话并发打磨多个 FR 原型的新建或大型重构需求）
- 为支持同时开启多个会话窗口并行推进不同功能、互不覆盖，采用 **“总览骨架 + 功能分片 + 自动合龙”** 结构：

```text
<需求工作区>/
├── 00_需求总览.md                  # 全局骨架：文档头、第 1~2 章、3.1 功能清单（含 <!-- FEATURES_INSERT_POINT -->）、第 4~7 章
├── Missing_Components.md          # 缺失组件提单：自动汇总各原型中 status="draft" 的待补 Figma 组件
├── features/                      # 【并发隔离区】每个功能独立目录，多会话并行互不覆盖
│   ├── FR-001_功能名称/
│   │   ├── prototype.html         # 基于 Nova-proto (<cad-*>) 的本地交互原型
│   │   └── spec.md                # 从 prototype.html 提炼的单功能内聚规格（含交互卡、BR、AC）
│   └── FR-002_功能名称/
│       ├── prototype.html
│       └── spec.md
├── .assets/                       # 底层机器资产与图片目录
│   ├── nova-proto/                # 自动注入的组件库运行时 (cad-design-tokens.css, cad-components.js)
│   ├── images/                    # 原型导出的状态帧图（fr-001-s1.png）、Mermaid 渲染图、快照原图
│   └── source.md / manifest.json  # 远程来源不可变快照（按需，见 snapshot.md）
└── <需求名>.md                    # 【合龙主稿】由 assemble_prd.py 自动拼接生成（未命名时用 prd.md）
```

- **单点修改与全量合龙**：
  - 多会话并发打磨原型时，各会话只读写各自 `features/FR-xxx/` 下的 `prototype.html` 与 `spec.md`，状态帧图统一导出至 `.assets/images/`；
  - 需要生成或更新完整 PRD 时，运行合龙脚本自动执行 **`prototype.html` 组件覆盖率审计 + `Missing_Components.md` 同步 + 分片拼接**：
    ```bash
    python scripts/assemble_prd.py --workspace <工作区绝对路径> --output <工作区绝对路径>/<需求名>.md
    ```
- **附加按需资产**：
  - `<需求名>_竞品分析.md`：仅在开展深度同类产品调研时落盘（见 [竞品对标](prd-benchmark.md)）；
  - `<需求名>_帮助初稿.md`：仅在 PM 明确要求由需求派生帮助文档时产出。

## 2. 版本、作者与状态

- **版本**：新文档从 `0.1` 开始；每次修订递增末级数字并追加修订记录行（如 `0.1 → 0.2`），不覆盖历史记录；文首版本与最新修订行一致。
- **修订人**：PAT 快照场景可从快照元数据 `author.display_name` 读取姓名填写“`中文名+PrdRefiner`”（不可读时标“`中文名待补充+PrdRefiner`”）；非 PAT 按实际变更人。
- **密级与审核**：密级按依据勾选，未知注明；未审核、未批准留空。
- **文档状态**（三选一）：

| 状态 | 适用条件 |
|---|---|
| **待补充工作稿** | 部分核心 FR 尚在打磨原型或待决项较多，仅记录已完成分片与缺口 |
| **初版待核对** | 各 FR 原型与内聚规格已合龙，未决项已登记 DEC，完成静态检查待 PM 核对 |
| **可供团队讨论的初版** | 满足初版条件，且经 PM 确认与下游四视角消缺，可交付研发与品质评审 |

## 3. 本地交付校验

合龙生成完整 Markdown 主稿后，依次执行静态校验与下游审查：

1. **分片合龙与静态检查**：

```bash
python scripts/assemble_prd.py --workspace <工作区绝对路径> --output <稿件绝对路径>
python scripts/validate_prd.py <稿件绝对路径> --profile template
python scripts/validate_links.py <稿件绝对路径> --format markdown --profile template
```

- `assemble_prd.py` 检查所有 `features/*/prototype.html` 是否满足 **0 裸 HTML 标签**（`<input>/<button>/<select>/<textarea>` 为 0），统计 `<cad-*>` 官方组件与 `status="draft"` 草稿组件覆盖率，并将草稿组件自动汇总至 `Missing_Components.md`，随后拼合生成完整主稿。
- `validate_prd.py` 检查核心章节、模板占位清理、本地图片存在性、竞品名禁用、元话语污染拦截，以及每个 FR 的交互卡覆盖率。
- `validate_links.py` 检查条目单一定位与同页锚点跳转。

| 场景 | 对应参数 | 说明 |
|---|---|---|
| **优化已有稿** | `--source <原始文档>`（`validate_prd.py`） | 检查模板结构与原稿图片保留情况 |
| **未完成中间稿 / 旧稿诊断** | `--profile draft` / `existing` | `draft` 用于尚有分片未完成的中间稿；`existing` 仅用于输入旧稿诊断 |
| **外部图片 / 位置引用** | `--image-policy external` / `--reference-policy location` | 仅在目标环境明确要求外链或不支持锚点时使用 |

2. **下游审查与消缺**：
   静态检查通过后，对照 [下游审查清单](downstream-review.md) 完成研发、品质、交互与产品化四视角排查并就地消缺。写入 Confluence 时的平台转换与校验见 [平台写入](publish-confluence.md)。

## 4. 帮助初稿交付

仅在 PM 明确要求由 PRD 派生帮助内容时执行：
- **单一源**：只维护 `<需求名>_帮助初稿.md`（依据 [帮助初稿模板](../assets/help-template.md) 或随附样例 `assets/help/help-demo/`），包含主题结构、只登记不画图的截图清单及界面术语对照。
- **术语查表**：使用 `scripts/lookup_term.py` 按 `assets/help/multilanguage-mapping.txt` 精确查表，区分命中、未命中与缺英文源串，严禁 AI 自行翻译。
