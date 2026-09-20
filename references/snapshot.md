# 来源快照

Confluence 页面或远程资料作为来源时读取。

## 1. 抓取与构建快照

Confluence 来源首次读取时，运行脚本建立不可变本地快照：

```bash
python scripts/fetch_snapshot.py --page-id <PAGE_ID_OR_URL>
```

- **认证复用**：脚本自动读取当前宿主已配置的 Atlassian MCP 凭据或环境变量。
- **产物基准**：脚本返回 `passed: true` 且 `manifest.json` 为 `complete` 即完成快照；本地完整稿必须基于快照的 `source.md` 生成。
- **落盘位置**：快照直接落在 `.assets/`（`source.md`、`source.original.txt`、`manifest.json`、`images/`），不建需求名子目录；`manifest.json` 为完成标记，最后写入。

## 2. 离线备用与缺口处理

- **离线环境**：脱机或已有外部资料包时，运行 `python scripts/build_snapshot.py` 传入本地 JSON 与资产目录完成对账。
- **缺口处理**：快照缺图或元数据缺失时，如实标明受影响范围；后续分析与成稿只读该快照，写入前核对远端最新版本。
