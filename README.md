# PRD Refiner

[![tests](https://github.com/ZION-XU/prd-refiner/actions/workflows/tests.yml/badge.svg)](https://github.com/ZION-XU/prd-refiner/actions/workflows/tests.yml)

中望 CAD 需求推演、**Nova-Proto (`<cad-*>`) 原型驱动**与**多会话分片并发** PRD 交付搭档。

## 核心架构（v2.0）

针对桌面工业 CAD 软件需求周期长（跨数周、数十个会话）、交互状态复杂（50% 以上工作量在原型设计）以及多人机对话易产生上下文污染的工程现实，本 Skill 采用三大核心机制：

1. **分片并发工作区（Feature Sharding）**：
   - 全局背景、范围、Mermaid 业务总体流程与功能清单索引维护在 `00_需求总览.md`；
   - 每个功能（FR）独立存放在 `features/FR-xxx_<名称>/` 目录下（包含 `prototype.html` 与内聚规格 `spec.md`），支持同时开启多个会话窗口并行打磨不同功能，互不覆盖、互不串味；
   - 交付时通过 `scripts/assemble_prd.py` 一键合龙生成完整 `<需求名>.md`。
2. **Nova-Proto (`<cad-*>`) 原型即真值（Prototype-as-SSOT）**：
   - 本地 HTML 原型严格使用从公司 Figma 组件库 1:1 转换的 `<cad-*>` Web Components 组件库构建，**零裸 HTML 容忍度**；
   - 遇到组件库缺失的控件，显式标记 `status="draft"` 并自动汇总至 `Missing_Components.md` 提单反哺 UI 设计师；
   - PRD 的功能规格（含带 ①②③ 标号的状态走查卡、内聚业务规则 `BR` 与验收标准 `AC`）直接从定稿的 `prototype.html` 与确认的 CAD 内核契约中提炼，**彻底杜绝将 PM 与 AI 的聊天过程元话语写入正式 PRD**。
3. **ZWCAD 领域防漏内核**：
   - 内置 CAD 三要素公约（命令/别名/静默模式、系统变量与作用域、锁定/冻结图层与块/Xref 边界）、命令行状态机、ESC 取消回滚与 Undo 分组检查单。

## 目录结构

```text
prd-refiner/
├─ SKILL.md                 入口：核心工作流、硬约束、内容地图与工具箱
├─ README.md                架构说明、安装与维护验证
├─ AGENTS.md                仓库维护契约与脚本速查
├─ references/              模块化规范（按需选读）
│  ├─ prd-standard.md       内容规范：主体解耦与元话语隔离、CAD 防漏清单、内聚编号与流程图
│  ├─ interaction-design.md 原型规范：Nova-Proto <cad-*> 白名单、缺件提单、标号截图与 spec 提炼
│  ├─ delivery.md           交付规范：分片目录、合龙脚本、版本状态与静态校验
│  ├─ brainstorm.md         探索方法：跨会话分片状态感知、第一性归零四问、原型内嵌洞察
│  ├─ clarify.md            澄清方法：决策前沿、外部事实自查 vs 业务事实问 PM
│  ├─ prd-benchmark.md      对标方法：三级证据、CAD 对标维度与对标矩阵
│  ├─ downstream-review.md  下游审查：研发 (C++/Qt5)／品质／交互／产品化四视角消缺
│  ├─ snapshot.md           快照支撑：Confluence/Jira 不可变本地快照与对账
│  └─ publish-confluence.md 平台发布：Storage 转换、浮动目录布局与回读校验
├─ assets/                  骨架、版式参照与多语言字典
│  ├─ prd-template.md       1~7 章高内聚 PRD 骨架（含分片合龙插槽）
│  ├─ help-template.md      帮助初稿骨架
│  ├─ confluence-toc.xml    Confluence 全宽 + 右上浮动目录布局骨架
│  └─ help/                 帮助版式样例 (help-demo) 与多语言字典 (multilanguage-mapping.txt)
└─ scripts/                 纯标准库 Python 工具与回归单测
   ├─ assemble_prd.py       分片合龙 + prototype.html 组件覆盖率审计 + Missing_Components 提取
   ├─ validate_prd.py       稿件结构、占位、本地图片、竞品名禁用与交互卡覆盖率校验
   ├─ validate_links.py     条目单一定义与锚点跳转校验
   ├─ validate_delivery.py  Confluence 组合交付校验
   ├─ convert_to_storage.py Markdown 转 Confluence Storage 格式
   ├─ fetch_snapshot.py     在线抓取远程快照
   ├─ build_snapshot.py     离线对账生成快照
   ├─ render_mermaid.py     Mermaid 流程图渲染为本地哈希 PNG
   ├─ lookup_term.py        帮助界面串按字典精确查表
   └─ test_*.py             全套回归测试
```

## 维护验证

在仓库根目录执行回归测试：

```bash
python -B -m unittest discover -s scripts -p "test_*.py"
```
