# PRD Refiner

辅助中望 CAD 产品人员编写、检查和优化 PRD 初版。先审查资料，保留已明确且未发现实质问题的要求；仅对需要产品决定的问题提问，无此类问题即可成稿。支持直接出稿、只检查、精简和局部修改。

## 安装与使用

将本目录复制或链接到宿主支持的 Skill 目录，通过 `$prd-refiner` 或宿主等价方式显式调用。开发副本建议链接主线，避免漂移。Python 3.10+ 用于标准库校验器；本地资料任务无需企业账号，远程能力依赖宿主已有工具。

```text
$prd-refiner 一起优化这份 PRD，先讨论关键问题。
$prd-refiner 根据这些资料直接出初版，未知标明。
$prd-refiner 只检查歧义和遗漏，不改文件。
$prd-refiner 修改 FR-002，保持其他功能并检查相关验收。
```

完整稿按统一模板交付工作区 Markdown；实际提出过产品澄清问题时配套决策记录。默认只有这两类文档需要用户阅读，来源快照、图片、Mermaid 渲染图、转换稿、Storage、差异与校验结果等生成文件统一放入 `.assets/<需求名>/`。只检查不改稿，只要片段时不扩写全文。Confluence 来源先下载正文与引用图片形成完整本地快照；写回时将普通图片和 Mermaid 图逐项上传并改为附件引用。用户指定目的地或配套要求时遵循其选择。

## 文件与加载

- [SKILL.md](SKILL.md)：对话节奏、修改边界、读取时机。
- [内容规范](references/prd-standard.md)：首次分析读取；依据、规则、验收和内容复核。
- [模板](assets/prd-template.md)与 [交付规范](references/delivery.md)：成稿、保存与检查时读取。
- [图片规范](references/prototype-analysis.md)：涉及图片／原型时读取。
- [Confluence 规范](references/publish-confluence.md)：仅明确写入平台时读取，复用 [布局骨架](assets/confluence-toc.xml)。
- `scripts/`：结构、引用及组合交付检查、Mermaid PNG 渲染与回归测试；执行无需通读源码。
- [AGENTS.md](AGENTS.md)：维护说明；`agents/openai.yaml`：宿主元数据。

## 维护验证

```text
python -B -m unittest discover -s scripts -p "test_*.py"
```

文稿校验命令、降级条件与检查边界见交付规范。静态测试不证明需求正确或宿主对话行为。改动后应用合成资料验证共同优化、直接出稿、只检查、局部修改、未决保留及相应交付；实际宿主验证与模拟结果分别记录。业务资料、生成文稿和分析材料存放仓库外。
