# PRD Refiner

中望 CAD 需求探讨、**Nova-Proto (`<cad-*>`) 桌面端原型设计**与**高信息密度 PRD** 编写辅助工具。

## 核心特点

1. **按需协作与深度场景思考**：
   - 按需开展工作：只探讨方案、只画原型、只改某段文档或推进完整 PRD 均可；
   - 探讨功能时从设计师真实场景、下一步动作与数据来源出发，识别旧做法痛点并给出更简捷的交互方案（见 `references/brainstorm.md`）。
2. **Nova-Proto (`<cad-*>`) 纯粹桌面端界面原型**：
   - 本地 HTML 原型通过 `figma-components-web` MCP 使用从公司 Figma 组件库转换的 `<cad-*>` Web Components 官方组件与图标构建，呈现紧凑硬朗的桌面端 CAD 软件质感；
   - 遇到组件库缺失的控件，标记 `status="draft"` 并自动汇总至 `Missing_Components.md` 供 UI 设计师补齐；
   - 原型与 PRD 正文分工明确：原型展示界面布局与常规控件，**PRD 正文不重复罗列常规自明控件，只写特殊逻辑、跨控件联动、CAD 业务规则与环境边界及量化验收标准**。
3. **支持单文件维护与多会话分片并发**：
   - 轻量需求或已有单文件 PRD 直接就地维护 `<需求名>.md`；
   - 大型多模块需求支持按 `00_需求总览.md` + `features/FR-xxx_<名称>/{prototype.html, spec.md}` 分片并行推进，并通过 `scripts/assemble_prd.py` 一键合龙。

## 推荐使用建议（多会话分治，避免上下文膨胀）

编写中大型 PRD（数万至数十万字）时，若在单一会话中完成所有模块的讨论、原型与正文，不断膨胀的上下文会稀释 Skill 提示词的约束力。无需记忆多个子技能，推荐**按“1 个总览 + N 个单功能 + 1 个合龙”开启多个独立会话，每次新会话启动 `prd-refiner`**，以本地工作区文件作为跨会话记忆：

1. **会话 1：定方向与拆模块（总览会话）**
   - **做什么**：聊清业务背景、痛点与边界，将大需求拆解为独立的 `FR-001`、`FR-002` 等功能块，生成 `00_需求总览.md`（及按需产出 `<需求名>_竞品分析.md`）。
   - **开场示例**：`用 prd-refiner，我们要做 [需求名称]，先探讨整体方向和功能模块拆解，生成 00_需求总览.md。`
2. **会话 2 ~ N：单功能深挖（一功能一会话，支持多窗口同时进行）**
   - **做什么**：每个会话只负责一个 `FR-xxx`，在单个会话内闭环完成该功能的**场景讨论 → `<cad-*>` 原型设计（`prototype.html`）→ 规格提炼（`spec.md`）**。
   - **为什么好**：单会话上下文短小精悍，Skill 规范不会淹没；不同会话各自读写 `features/FR-xxx_<名称>/` 独立目录，多窗口并行互不冲突。
   - **开场示例**：`用 prd-refiner，参考工作区的 00_需求总览.md，我们来设计 FR-001 [功能名] 的详细方案、原型和 spec。`
3. **收尾会话：合龙、自检与交付**
   - **做什么**：新开一个干净会话，调用 `assemble_prd.py` 将总览与各 `FR` 分片合龙为完整 PRD，统一审视第 4~7 章全局内容（系统变量、性能、待决项），执行校验脚本并发布 Confluence。
   - **开场示例**：`用 prd-refiner，所有 FR 分片已完成，请合龙生成完整 PRD 并进行成稿校验。`

> **轻量需求**：若只是单点小功能或几千字的常规修改，直接在 1 个会话内按单文件模式维护 `<需求名>.md` 即可，无需拆分。

## 目录结构

```text
prd-refiner/
├─ SKILL.md                 入口：协作方式、核心要求、文件存放位置、参考文档与脚本工具箱
├─ README.md                仓库说明
├─ AGENTS.md                仓库维护契约与脚本速查
├─ references/              按需查阅的参考指南
│  ├─ brainstorm.md         头脑风暴：拆解大需求、深挖真实场景、一次一问与备选方案对比
│  ├─ interaction-design.md 原型规范：配合 figma-components-web MCP 构建桌面端 <cad-*> 原型、缺件标记与重点规格提炼
│  ├─ prd-standard.md       内容规范：高信息密度原则、CAD 防漏清单、编号引用与流程图
│  ├─ delivery.md           交付规范：单文件与分片双模式、合龙脚本、版本状态与基础校验
│  ├─ downstream-review.md  成稿自检：研发／品质／交互／产品化四角度排查清单
│  ├─ prd-benchmark.md      竞品调研：区分事实与推论、CAD 对比维度与表格格式
│  ├─ snapshot.md           远程快照：Confluence/Jira 本地不可变快照抓取与对账
│  └─ publish-confluence.md 平台发布：Storage 格式转换、浮动目录布局与回读校验
├─ assets/                  模板、组件库运行时、版式参照与多语言字典
│  ├─ prd-template.md       1~7 章 PRD 骨架（含分片合龙插槽）
│  ├─ nova-proto/           内置 Nova-Proto Web Components 运行时 (cad-design-tokens.css, cad-components.js)
│  ├─ help-template.md      帮助初稿骨架
│  ├─ confluence-toc.xml    Confluence 全宽 + 右上浮动目录布局骨架
│  └─ help/                 帮助版式样例 (help-demo) 与多语言字典 (multilanguage-mapping.txt)
└─ scripts/                 纯标准库 Python 辅助工具
   ├─ assemble_prd.py       分片合龙 + prototype.html 组件覆盖率检查 + Missing_Components 提取
   ├─ validate_prd.py       稿件核心章节、占位符、重号与本地图片存在性校验
   ├─ validate_links.py     条目单一定义与 #anchor 锚点跳转校验
   ├─ validate_delivery.py  Confluence 组合交付校验
   ├─ convert_to_storage.py Markdown 转 Confluence Storage 格式
   ├─ fetch_snapshot.py     在线抓取远程快照
   ├─ build_snapshot.py     离线对账生成快照
   ├─ render_mermaid.py     Mermaid 流程图渲染为本地哈希 PNG
   └─ lookup_term.py        帮助界面串按字典精确查表
```
