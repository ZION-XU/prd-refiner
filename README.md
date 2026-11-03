# PRD Refiner

[![tests](https://github.com/ZION-XU/prd-refiner/actions/workflows/tests.yml/badge.svg)](https://github.com/ZION-XU/prd-refiner/actions/workflows/tests.yml)

中望 CAD 需求探讨、**Nova-Proto (`<cad-*>`) 原型设计**与**高信息密度 PRD** 编写辅助工具。

## 核心特点

1. **按需协作与深度场景思考**：
   - 按需开展工作：只探讨方案、只画原型、只改某段文档或推进完整 PRD 均可；
   - 探讨功能时从设计师真实场景、下一步动作与数据来源出发，识别旧做法痛点并给出更简捷的交互方案（见 `references/brainstorm.md`）。
2. **Nova-Proto (`<cad-*>`) 纯粹界面原型**：
   - 本地 HTML 原型通过 `figma-components-web` MCP 使用从公司 Figma 组件库转换的 `<cad-*>` Web Components 官方组件与图标构建；
   - 遇到组件库缺失的控件，标记 `status="draft"` 并自动汇总至 `Missing_Components.md` 供 UI 设计师补齐；
   - 原型与 PRD 正文分工明确：原型展示界面布局与常规控件，**PRD 正文不重复罗列常规自明控件，只写特殊逻辑、跨控件联动、CAD 底层边界与量化验收标准**。
3. **支持单文件维护与多会话分片并发**：
   - 轻量需求或已有单文件 PRD 直接就地维护 `<需求名>.md`；
   - 大型多模块需求支持按 `00_需求总览.md` + `features/FR-xxx_<名称>/{prototype.html, spec.md}` 分片并行推进，并通过 `scripts/assemble_prd.py` 一键合龙。

## 目录结构

```text
prd-refiner/
├─ SKILL.md                 入口：协作方式、核心要求、文件存放位置、参考文档与脚本工具箱
├─ README.md                仓库说明与维护验证
├─ AGENTS.md                仓库维护契约与脚本速查
├─ references/              按需查阅的参考指南
│  ├─ brainstorm.md         头脑风暴：拆解大需求、深挖真实场景、一次一问与备选方案对比
│  ├─ interaction-design.md 原型规范：配合 figma-components-web MCP 构建 <cad-*> 原型、缺件标记与重点规格提炼
│  ├─ prd-standard.md       内容规范：高信息密度原则、CAD 防漏清单、编号引用与流程图
│  ├─ delivery.md           交付规范：单文件与分片双模式、合龙脚本、版本状态与静态校验
│  ├─ downstream-review.md  成稿自检：研发 (C++/Qt5)／品质／交互／产品化四角度排查清单
│  ├─ prd-benchmark.md      竞品调研：区分事实与推论、CAD 对比维度与表格格式
│  ├─ snapshot.md           远程快照：Confluence/Jira 本地不可变快照抓取与对账
│  └─ publish-confluence.md 平台发布：Storage 格式转换、浮动目录布局与回读校验
├─ assets/                  模板、组件库运行时、版式参照与多语言字典
│  ├─ prd-template.md       1~7 章 PRD 骨架（含分片合龙插槽）
│  ├─ nova-proto/           内置 Nova-Proto Web Components 运行时 (cad-design-tokens.css, cad-components.js)
│  ├─ help-template.md      帮助初稿骨架
│  ├─ confluence-toc.xml    Confluence 全宽 + 右上浮动目录布局骨架
│  └─ help/                 帮助版式样例 (help-demo) 与多语言字典 (multilanguage-mapping.txt)
└─ scripts/                 纯标准库 Python 工具与回归单测
   ├─ assemble_prd.py       分片合龙 + prototype.html 组件覆盖率检查 + Missing_Components 提取
   ├─ validate_prd.py       稿件结构、占位、本地图片、禁用词与交互卡覆盖率校验
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
