# PRD Refiner

PRD Refiner 是一个面向产品经理的多平台 Agent 插件，用于把传统 PRD 和可选原型资料优化为同时适合人工评审、AI coding、测试和下游自动化消费的结构化需求包。产品经理确认后，还可通过 MCP 将结果写入公司 Confluence。

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
        ↓（可选，产品经理确认后）
写入指定 Confluence 页面并回读校验
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
├── .mcp.json                 # Codex 随插件注册的 Confluence MCP
├── integrations/confluence-mcp/ # 首次配置与锁定版本启动器
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
| 企业 Confluence MCP | 文本、层级与原生图片引用已验证 | 已在 Confluence 7.19.4 完成搜索、读取、已有页更新、子页面创建/更新、层级、HTML 回读，以及表格/正文中的跨页面附件图片引用；本地图片上传仍待扩展 |

不要将“结构与语法就绪”表述为“已在真实客户端验证”。完整状态见 [docs/platform-support.md](docs/platform-support.md)。

## 安装与使用

安装方式因 Agent 平台而异；如果同时使用多个平台，需要分别安装。当前仅 Codex App / CLI 完成了真实安装与交互验证，其他平台的适配状态见 [docs/installation.md](docs/installation.md)。

### Codex App / CLI 源码安装

当前插件未发布到公共插件市场，只提供源码安装。安装前需要确保 Git 已具备仓库访问权限；克隆源码后，将本地仓库目录登记给 Codex 插件安装器并安装：

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

更新时在本地仓库目录拉取最新代码并重新安装：

```powershell
git pull
codex plugin add prd-refiner@prd-refiner-dev
```

这里的本地 marketplace 只是 Codex 安装源码插件所需的目录登记机制，不表示插件已经发布到公共市场。

## 企业 Confluence MCP

### 认证方式与固定地址

公司环境固定连接：

```text
https://confluence.zwcad.com
```

这是公司自建的 Confluence 7.19.4，不需要 Atlassian Cloud 或 Rovo 网站账号。每位使用者只需要自己的公司 Confluence 用户名和 Personal Access Token（PAT）；最终读写权限仍由该用户在目标空间和页面上的既有权限决定。

获取 PAT：

1. 登录 <https://confluence.zwcad.com>；
2. 打开个人头像下的个人设置；
3. 进入 **Personal Access Tokens**；
4. 创建一个用于 PRD Refiner 的 Token，按公司策略设置有效期；
5. 立即复制并妥善保存。PAT 通常只在创建时完整显示一次。

如果个人设置中没有 Personal Access Tokens，请联系 Confluence 管理员确认该功能和个人权限，不要改用 Atlassian Rovo 账号。

### 首次配置

插件包已包含 MCP 清单和启动器，但插件安装器不会自动执行凭据采集脚本。安装插件后，在仓库根目录运行一次：

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass `
  -File .\integrations\confluence-mcp\configure.ps1
```

脚本会手动询问公司 Confluence 用户名和 PAT。PAT 输入不回显，并使用 Windows 当前用户的 DPAPI 加密后保存到：

```text
%APPDATA%\PRDRefiner\confluence.json
```

该文件位于插件仓库之外，PAT 不写入 Git、插件包、PRD 需求包或日志。加密内容只能由同一个 Windows 用户解密。配置脚本还会通过 `uv` 预下载已验证的 MCP 依赖；完成后需要新建 Agent 任务，让宿主重新加载 MCP。

首次配置需要系统已安装 `uv`。验证阶段锁定以下组合，不要无约束升级：

```text
mcp-atlassian==0.8.4
atlassian-python-api==3.41.21
markdown-to-confluence==0.3.0
mcp==1.9.4
```

锁定原因：`mcp-atlassian 0.23.0` 当前会解析到 `atlassian-python-api 5.0.2`，后者对公司 Confluence 7.19.4 生成了错误的 `/rest/api/1.0/rest/api/...` 路径。上述组合已完成实际页面搜索、读取、已有页更新、子页面创建/更新、父子层级、HTML 回读，以及表格和正文中的 Confluence 原生跨页面附件图片引用验证。

插件通过 `integrations/confluence-mcp/server.py` 启动锁定版本，并关闭上游默认的标题 Anchor 自动生成。普通 PRD 标题因此保存为原生 `<h1>`～`<h6>`，不会在编辑器中额外出现 Anchor 宏；确实需要章节跳转时再显式添加 Anchor。

### 随插件安装与跨 Agent 使用

Codex 安装 PRD Refiner 时会读取根目录的 `.mcp.json`，随插件注册 `prd-refiner-confluence`。依赖由首次配置脚本准备，不需要用户单独编写 Codex MCP 配置。

其他支持 stdio MCP 的 Agent 可以复用同一个启动器和同一份加密配置。将下面命令注册为 MCP 服务即可，其中脚本路径应替换为实际插件目录的绝对路径：

```text
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File <PRD-REFINER目录>\integrations\confluence-mcp\launch.ps1
```

Claude Code、Cursor、ZCode 等使用 `command`/`args` 形式时，可采用：

```json
{
  "mcpServers": {
    "prd-refiner-confluence": {
      "command": "powershell.exe",
      "args": [
        "-NoLogo",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        "D:\\path\\to\\prd-refiner\\integrations\\confluence-mcp\\launch.ps1"
      ]
    }
  }
}
```

OpenCode 的本地 MCP 可复用同一命令：

```json
{
  "mcp": {
    "prd-refiner-confluence": {
      "type": "local",
      "command": [
        "powershell.exe",
        "-NoLogo",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        "D:\\path\\to\\prd-refiner\\integrations\\confluence-mcp\\launch.ps1"
      ]
    }
  }
}
```

不同 Agent 的插件安装格式可以不同，但不要复制 PAT 到各平台配置中；统一调用启动器即可。目前已从 Codex 的已安装插件副本完成 Confluence 文本读取、已有页更新、子页面创建/更新和回读验证，其他 Agent 的自动注册仍需逐一实测。

### 写入安全边界

- 默认先生成本地需求包和 Confluence 写入预览；
- 必须由产品经理确认目标空间、父页面、页面标题、创建/更新动作和附件清单；
- 不静默覆盖正式页面，不把待确认内容伪装成已确认需求；
- 写入后回读页面 ID、标题、版本、正文和附件清单；
- 失败时明确记录已完成项和待重试项；
- 当前已验证更新已有页面、创建与更新子页面、父子层级、Markdown 表格转 HTML、回读，以及在表格和正文中用 `ri:attachment + ri:page` 引用另一 Confluence 页的图片。不要把需要登录的附件下载地址当作 `ri:url` 外部图片，否则页面可能提示无法加载。公开且无需登录的外部图片才可直接使用 URL；本地截图仍需后续补充上传工具，或先由用户上传后再用原生附件引用。

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
