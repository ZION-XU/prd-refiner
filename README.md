# PRD Refiner

PRD Refiner 是一个面向产品经理的多平台 Agent 插件，用于把传统 PRD 和可选原型资料优化为同时适合人工评审、AI coding、测试和下游自动化消费的结构化需求包。

插件不会替产品经理做业务决策。它识别需求中的缺失、模糊和冲突，在支持结构化输入的平台中与产品经理逐项或成组澄清，并保留完整的决策依据。

## 核心工作流

```text
显式启动 prd-refiner
        ↓
输入 PRD 与可选原型资料
        ↓
解析需求、原型观察和信息来源
        ↓
识别缺失、歧义、冲突和下游风险
        ↓
产品经理进行结构化澄清与确认
        ↓
生成并校验 AI-Ready 需求包
```

高影响或存在依赖的决策会单独询问；彼此独立且优先级相近的问题可按 2–3 项成组确认。Codex 用户需要在进入结构化澄清前切换至 Plan 模式。

## 输出

- `ai-ready-prd.md`：结构化、可追溯的需求正文；
- `interaction-spec.md`：页面、控件、状态、反馈及PRD—原型对齐；
- `clarification-log.md`：问题、候选项、产品经理回答、结论和影响；
- `traceability-matrix.md`：来源、需求、原型、澄清和验收的双向映射；
- `quality-report.md`：完整性、清晰性、原型一致性、可测试性及下游消费风险；
- `evaluation-scorecard.md`：使用同一量表评价原始资料和优化后需求包。

有原型图片、流程图或状态图时，需求包还会包含 `assets/prototype-images/` 和 `assets/diagrams/`；没有实际资产时不创建空目录。

## 方法成果

- [PRD 优化规范](skills/prd-refiner/references/prd-optimization-spec.md)：面向任意格式人工 PRD 的十二维检查、证据边界、问题分级和追溯规则；
- [交互式工作流](skills/prd-refiner/references/interactive-workflow.md)：显式启动到校验交付的十环节流程；
- [评价标准](skills/prd-refiner/references/evaluation-standard.md)：八维、100 分、同尺评价和过程红线；
- [原型分析规范](skills/prd-refiner/references/prototype-analysis.md)：输入分级、`UI-xxx`、PRD—原型冲突和资产规则；
- [评价表模板](skills/prd-refiner/assets/evaluation-scorecard-template.md)：优化前后评分与客观计数模板；
- [CAD 图层批量状态案例](examples/cad-layer-batch-state/01-original-prd.md)：从非固定格式原始PRD、原型观察和澄清到六文档需求包及前后评分的完整合成案例。

## 项目架构

`skills/prd-refiner/` 是唯一业务核心。平台目录只负责安装、Skill 注册和宿主工具映射，不复制业务规则。

```text
prd-refiner/
├── skills/prd-refiner/       # 单一核心 Skill
├── examples/                 # 合成案例与效果评价
├── .codex-plugin/            # Codex
├── .claude-plugin/           # Claude Code
├── .cursor-plugin/           # Cursor
├── .kimi-plugin/             # Kimi Code
├── .opencode/                # OpenCode
├── .pi/                      # Pi
├── .hermes-plugin/           # Hermes Agent
├── .devin-plugin/            # Devin
├── gemini-extension.json     # Gemini CLI
├── GEMINI.md
├── package.json              # OpenCode / Pi 包入口
├── docs/                     # 架构、安装和平台状态
└── scripts/                  # 项目级校验工具
```

架构细节见 [docs/architecture.md](docs/architecture.md)。

## 平台状态

| 平台 | 状态 | 说明 |
|---|---|---|
| Codex App / CLI | 已验证 | 支持插件安装、显式 Skill 调用和 Plan 模式结构化澄清 |
| Claude Code | 待实测 | 已提供插件清单，共享核心 Skill |
| Cursor | 待实测 | 已提供插件清单，共享核心 Skill |
| Kimi Code | 待实测 | 已提供插件清单和提问工具映射 |
| OpenCode | 待实测 | 已提供 Skill 路径注册插件 |
| Pi | 待实测 | 已提供 Skill 资源发现扩展 |
| Gemini CLI | 待实测 | 已提供扩展清单和显式调用说明 |
| Hermes Agent | 待实测 | 已提供 Skill 注册适配器 |
| Devin | 待实测 | 已提供插件清单 |

不要将“结构与语法就绪”表述为“已在真实客户端验证”。完整状态见 [docs/platform-support.md](docs/platform-support.md)。

## 安装与使用

安装方式因 Agent 平台而异；如果同时使用多个平台，需要分别安装。当前仅 Codex App / CLI 完成了真实安装与交互验证，其他平台的适配状态见 [docs/installation.md](docs/installation.md)。

### Codex App / CLI

当前仓库为私有开发源码，安装前需要确保 Git 已具备仓库访问权限。

直接从 GitHub 注册 marketplace 并安装：

```powershell
codex plugin marketplace add ZION-XU/prd-refiner --ref main
codex plugin add prd-refiner@prd-refiner-dev
```

如需在本地修改插件，也可以克隆仓库并把仓库根目录注册为本地 marketplace。两种方式选择一种即可，不要同时注册：

```powershell
git clone https://github.com/ZION-XU/prd-refiner.git
cd prd-refiner
codex plugin marketplace add .
codex plugin add prd-refiner@prd-refiner-dev
```

安装完成后新建 Codex 任务并显式调用：

```text
$prd-refiner
```

随后提供 PRD 文本或文件，并可附加截图、Figma 链接或 Axure 材料。普通对话仅提及 PRD 时，插件不会自动启动。

从 GitHub 安装的插件按以下方式更新：

```powershell
codex plugin marketplace upgrade prd-refiner-dev
codex plugin add prd-refiner@prd-refiner-dev
```

本地开发安装则在仓库目录拉取最新代码并重新安装：

```powershell
git pull
codex plugin add prd-refiner@prd-refiner-dev
```

## Figma 扩展方向

当前版本将截图、可访问链接和用户补充作为原型输入。未来可接入 Figma API、MCP 或其他连接器；连接器只提供可观察证据，不直接决定业务规则。接口边界见 [figma-integration.md](skills/prd-refiner/references/figma-integration.md)。

## 开发与校验

主要校验命令：

```powershell
$env:PYTHONUTF8='1'
python scripts/validate_cross_platform.py
python skills/prd-refiner/scripts/validate_requirement.py <output-directory>
```

维护规则见 [AGENTS.md](AGENTS.md)。版本变化见 [RELEASE-NOTES.md](RELEASE-NOTES.md)。

## 许可

当前为私有项目，保留所有权利。未经版权所有者书面许可，不得复制、分发或公开发布。详见 [LICENSE](LICENSE)。
