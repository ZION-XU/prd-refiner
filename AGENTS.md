# AGENTS.md

本仓库是 `prd-refiner` 技能本体（`SKILL.md` 是唯一入口规范源）。只在用户明确点名 `prd-refiner`（pi 中为 `/skill:prd-refiner`）时作为工作上下文加载；通常调用脚本处理外部需求工作区。

## 关键事实

- **核心定位**：
  - 针对中望 CAD 桌面软件开展需求头脑风暴、构建 `<cad-*>` 桌面端界面原型、编写高信息密度 PRD 并交付 Confluence；
  - 支持**单文件直接维护**（`<工作区>/<需求名>.md`）与**多会话分片并发**（`00_需求总览.md` + `features/FR-xxx_<名称>/{prototype.html, spec.md}`，通过 `scripts/assemble_prd.py` 合龙）；
  - 原型通过 `figma-components-web` MCP（及内置 `assets/nova-proto/` 兜底）使用 `<cad-*>` 官方组件构建纯粹界面（缺失组件标 `status="draft"` 并汇总至 `Missing_Components.md`）；PRD 正文只写特殊/增量逻辑与 CAD 业务环境边界，不重复罗列原型中已自明的常规控件。
- **Python 侧纯标准库**：`scripts/*.py` 仅使用 Python 标准库（Python 3.10+），命令一律在**技能仓库根目录**执行，工作区与文件路径以绝对路径显式传入。
- **模板纯洁与规范隔离**：`assets/prd-template.md` 纯粹是字段骨架，严禁包含工具脚本名称（如 `*.py`）或规范要求；所有规范写在 `references/*.md`，模板只写超链接指针。
- **Antigravity 宿主同步要求**：Antigravity 宿主不支持软链接（Junction/Symlink）加载技能目录。每次修改本仓库文件后，必须使用 `robocopy "D:\prd-refiner" "C:\Users\Administrator\.gemini\config\skills\prd-refiner" /MIR /XD .git __pycache__ .pytest_cache` 将实体文件同步至 `.gemini\config\skills\prd-refiner`（严禁将其改为软链接）。

## 脚本速查

| 脚本 | 职责 | 关键参数 |
|---|---|---|
| `assemble_prd.py` | 检查各 FR 的 `prototype.html` 组件覆盖率（拦截裸 HTML、提取 `draft` 组件至 `Missing_Components.md`）并合龙生成完整 PRD | `--workspace` 必填，`--output`、`--overview`、`--init-only` |
| `validate_prd.py` | 稿件核心章节、模板占位符、重号与本地图片存在性校验 | `--profile {template,draft,existing}`、`--source`、`--image-policy` |
| `validate_links.py` | 条目定义与 `#anchor` 锚点跳转校验（Markdown 或 Confluence Storage） | `--format {markdown,storage}`、`--profile {template,draft,existing}` |
| `validate_delivery.py` | Confluence 组合交付校验 | `--workspace` 必填，Storage 正文跑两遍（提交稿 + 服务端回读） |
| `convert_to_storage.py` | Markdown 转 Confluence Storage 格式 | `--output` 必填，`--layout {floating,inline}` |
| `fetch_snapshot.py` / `build_snapshot.py` | 在线抓取或离线对账建 Confluence/Jira 快照 | `--page-id`、`--workspace` |
| `render_mermaid.py` | Mermaid 流程图渲染为哈希命名 PNG | `--output-dir`、`--force` |
| `lookup_term.py` | 界面串按字典精确查表 | `--mapping`、`--terms`/`--terms-file` |
