# 来源快照

Confluence 页面或远程资料作为来源时读取。快照是工作区的机器资产，工作区必须显式传入。

本地已有材料（客户反馈文件、草图、截图等）本身就是不可变输入，无需走快照脚本：原件归档入 `.assets/` 后直接作为分析输入，整理与命名规则见 [成稿与交付](delivery.md)。

## 1. 抓取与构建快照

Confluence 来源首次读取时，运行脚本建立不可变本地快照：

```bash
python scripts/fetch_snapshot.py --page-id <PAGE_ID_OR_URL> --workspace <需求工作区绝对路径>
```

- **认证复用**：脚本自动读取当前宿主已配置的 Atlassian MCP 凭据或环境变量，并从 `--workspace` 起逐级向上查找 `.mcp.json`／`mcp_config.json`。
- **产物基准**：脚本返回 `passed: true` 且 `manifest.json` 为 `complete` 即完成快照；本地完整稿必须基于快照的 `source.md` 生成。
- **落盘位置**：快照落在 `<工作区>/.assets/`（`source.md`、`source.original.txt`、`manifest.json`、`images/`）；`manifest.json` 为完成标记，最后写入。
- **工作区必填**：`--workspace` 不设默认值，以免快照落到当前目录（如 Skill 仓库本身）；已有快照需重取时加 `--force`，它只覆盖快照自身的文件。

## 2. 离线备用与缺口处理

- **离线环境**：脱机或已有外部资料包时，用 `build_snapshot.py` 对账生成快照：

```bash
python scripts/build_snapshot.py --source-file <正文> --asset-dir <图片目录> \
    --workspace <需求工作区绝对路径> --page-id <ID> --page-version <版本>
```

  `--json-file` 与 `--source-file` 二选一；`--workspace`、`--page-id`、`--page-version` 必填，缺图、非法图片、重名冲突或不安全引用一律失败而非降级。
- **缺口处理**：快照缺图或元数据缺失时，如实标明受影响范围；后续分析与成稿只读该快照。
