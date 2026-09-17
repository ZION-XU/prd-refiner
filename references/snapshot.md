# 来源快照

Confluence 页面或远程资料作为来源时读取。

## 快照一键构建（推荐）

Confluence 来源首次读取时，直接运行一键抓取脚本建立不可变本地快照：

`ash
python scripts/fetch_snapshot.py --page-id <PAGE_ID_OR_URL>
`

- **凭据与地址自动发现**：脚本自动复用宿主环境已配置的 MCP（如 Antigravity、OpenCode、Windsurf、Cursor 的 atlassian MCP 配置）或环境变量中的 PAT 与 Confluence URL，与用户的 MCP 配置保持 100% 一致，零多余配置。
- **免反查与零 Token 损耗**：脚本直接通过正文文件名直连 Confluence 高速端点下载图片，无需大模型往返调用 MCP 反查 Attachment ID，彻底避开 API 分页截断暗坑，耗时秒级且消耗 0 Token。
- **不可变基准检验**：脚本返回 passed: true 且 manifest.json 为 complete 即在 .assets/source_snapshot/ 建立不可变本地快照。本地完整稿必须基于快照的 source.md 生成。

## 备用离线校验

若处于完全脱机或外部已有离线包场景，使用 scripts/build_snapshot.py 传入本地 json 与 asset 目录进行离线哈希对账与路径重写。

快照缺图或元数据不全时报告具体缺口；仍可指出局部文字问题，但须注明未检查完整页面。后续分析、澄清与成稿只读该快照；写入前核对远端最新版本。
