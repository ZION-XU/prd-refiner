# AGENTS.md

本仓库是 `prd-refiner` 技能本体（`SKILL.md` 是唯一入口规范源）。只在用户明确点名 `prd-refiner`（pi 中为 `/skill:prd-refiner`）时作为工作上下文加载；通常调用脚本处理外部需求工作区。

## 关键事实

- **核心范式（v2 Nova-Proto 驱动 + 分片并发）**：
  - 针对中望 CAD 桌面软件需求，支持跨数周、数十个会话并发推进；
  - 每个功能（FR）在 `<工作区>/features/FR-xxx_<名称>/` 独立目录下维护 `prototype.html`（基于 `Nova-proto` `<cad-*>` Web Components 组件库，0 裸 HTML，缺失组件标 `status="draft"` 并汇总至 `Missing_Components.md`）与内聚规格 `spec.md`（内聚入口、带 ①②③ 标号的交互卡、业务规则 BR 与验收标准 AC）；
  - 通过 `scripts/assemble_prd.py` 将 `00_需求总览.md` 与各分片 `spec.md` 一键合龙为完整 PRD。
- **双重主体解耦**：严格区分操作 AI 的**产品经理（PM）**与使用 ZWCAD 的**CAD 终端设计师**，严禁将人机协作过程元话语写入 PRD。
- **Python 侧纯标准库**：`scripts/*.py` 仅使用 Python 标准库（Python 3.10+），命令一律在**技能仓库根目录**执行，工作区与文件路径以绝对路径显式传入。
- **测试**：`python -B -m unittest discover -s scripts -p "test_*.py"`。改动脚本、模板或文档后均需执行回归测试验证。
- **模板纯洁与规范隔离**：`assets/prd-template.md` 纯粹是字段骨架，严禁包含工具脚本名称（如 `*.py`）或规范要求；所有规范写在 `references/*.md`，模板只写超链接指针。

## 脚本速查

| 脚本 | 职责 | 关键参数 |
|---|---|---|
| `assemble_prd.py` | 审计各 FR 的 `prototype.html` 组件覆盖率（拦截裸 HTML、提取 `draft` 组件至 `Missing_Components.md`）并合龙生成完整 PRD | `--workspace` 必填，`--output`、`--overview` |
| `validate_prd.py` | 稿件结构、占位、本地图片、竞品名禁用與交互卡覆盖率校验 | `--profile {template,draft,existing}`、`--source`、`--image-policy` |
| `validate_links.py` | 条目定义引用、锚点跳转校验（Markdown 或 Confluence Storage） | `--format {markdown,storage}`、`--profile {template,draft,existing}` |
| `validate_delivery.py` | Confluence 组合交付校验 | `--workspace` 必填，Storage 正文跑两遍（提交稿 + 服务端回读） |
| `convert_to_storage.py` | Markdown 转 Confluence Storage 格式 | `--output` 必填，`--layout {floating,inline}` |
| `fetch_snapshot.py` / `build_snapshot.py` | 在线抓取或离线对账建 Confluence/Jira 快照 | `--page-id`、`--workspace` |
| `render_mermaid.py` | Mermaid 流程图渲染为哈希命名 PNG | `--output-dir`、`--force` |
| `lookup_term.py` | 界面串按字典精确查表 | `--mapping`、`--terms`/`--terms-file` |
