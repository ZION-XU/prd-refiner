# 来源快照

Confluence 页面、Jira 单据或远程资料作为来源时读取。快照是工作区的机器资产，工作区必须显式传入。

本地已有材料（客户反馈文件、草图、截图等）本身就是不可变输入，无需走快照脚本：原件归档入 `.assets/` 后直接作为分析输入，整理与命名规则见 [成稿与交付](delivery.md)。

## 1. 在线抓取快照（Confluence / Jira）

远程来源首次读取时，优先运行脚本建立不可变本地快照（支持 Confluence 页面 ID/URL 与 Jira 单据号/URL）：

```bash
python scripts/fetch_snapshot.py --page-id <PAGE_ID_OR_JIRA_KEY_OR_URL> --workspace <需求工作区绝对路径>
```

- **内外网 MCP 凭据全兼容**：脚本自动发现并复用宿主已配置的 Atlassian MCP 凭据（支持 JSON、Codex `config.toml`、命令行 `args`、`--env-file` 及 `{file:...}` 指令），兼容 PAT（Bearer）、用户名＋API Token/密码（Basic Auth 自动回退）、自定义请求头（`CONFLUENCE_CUSTOM_HEADERS`／`JIRA_CUSTOM_HEADERS`）及内外网证书环境。
- **产物基准**：脚本返回 `passed: true` 且 `manifest.json` 为 `complete` 即完成快照；本地完整稿必须基于快照的 `source.md` 生成。
- **落盘位置**：快照落在 `<工作区>/.assets/`（`source.md`、`source.original.txt`、`manifest.json`、`images/`）；`manifest.json` 为完成标记，最后写入。
- **工作区必填**：`--workspace` 不设默认值，以免快照落到当前目录（如 Skill 仓库本身）；已有快照需重取时加 `--force`，它只覆盖快照自身的文件。

## 2. MCP 工具抓取与离线对账兜底

当宿主通过远端网关（SSE / Streamable HTTP）或托管 OAuth 连接 MCP、本机脚本无直连凭据，或处于脱机资料包环境时，**只要宿主 MCP 工具能访问 Confluence 或 Jira，即可先由 MCP 工具取回内容与图片，再用 `build_snapshot.py` 对账建快照**：

```bash
python scripts/build_snapshot.py --source-file <正文> --asset-dir <图片目录> \
    --workspace <需求工作区绝对路径> --page-id <PAGE_ID_OR_JIRA_KEY> --page-version <版本>
```

- **MCP 协同路径**：调用宿主 MCP 工具（如 `confluence_get_page` + `confluence_download_attachment`／`confluence_download_content_attachments`，或 `jira_get_issue` + `jira_download_attachments`）将正文与引用图片保存至临时目录后，传入 `build_snapshot.py` 生成标准不可变快照。
- **严密对账**：`--json-file` 与 `--source-file` 二选一；`--workspace`、`--page-id`、`--page-version` 必填，缺图、非法图片、重名冲突或不安全引用一律失败而非降级。
- **缺口处理**：快照缺图或元数据缺失时，如实标明受影响范围；后续分析与成稿只读该快照。
