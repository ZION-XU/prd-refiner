# PRD Refiner

辅助中望 CAD 产品人员编写、检查和优化 PRD 初版。Skill 只补充通用 Agent 容易遗漏的图像证据、团队输出约定和 Confluence 写入细节；普通审稿、歧义分析和讨论由 Agent 按任务处理。

## 安装与使用

将本目录复制或链接到宿主支持的 Skill 目录，通过 `$prd-refiner` 或宿主等价方式显式调用。开发副本建议链接主线，避免漂移。Python 3.10+ 用于标准库校验器；本地资料任务无需企业账号，远程能力依赖宿主已有工具。

```text
$prd-refiner 一起优化这份 PRD，先讨论关键问题。
$prd-refiner 根据这些资料直接出初版，未知标明。
$prd-refiner 只检查歧义和遗漏，不改文件。
$prd-refiner 修改 FR-002，保持其他功能并检查相关验收。
```

完整稿按统一模板交付工作区 Markdown；探讨结论、竞品分析与澄清决策按需独立落盘根目录供用户查阅及跨会话流转。来源快照、原图、Mermaid 渲染图、转换稿、Storage、差异与校验结果等机器文件统一扁平放入 `.assets/`。Confluence 来源先下载正文与引用图片形成完整本地快照并查看画面；写回时使用 Storage、浮动折叠目录、原生锚点和附件图片。用户指定目的地或配套要求时遵循其选择。

## 文件与加载

- [SKILL.md](SKILL.md)：按任务加载真正需要的约束，不附通用审稿步骤。
- [内容约定](references/prd-standard.md)与 [模板](assets/prd-template.md)：每次调用本 Skill 处理 PRD 内容时，在首次分析前同步读取，作为编写、检查和局部修改的共同标准；一句话需求也一样。前者规定依据、状态和团队特有边界，后者承载输出框架与字段编写提示。只使用相关维度，检查或片段修改不扩展成完整稿。
- [探索与简报](references/brainstorm.md)：新建需求、核心重构或需求立项时读取，先分级任务重量（Spike／Bounded／Architectural）再推演，候选代价与裁决沉淀到 `<需求名>_需求探讨.md`。
- [交互澄清](references/clarify.md)：成稿前消灭隐形假设时读取，按决策前沿组织提问，一轮问完当前前沿且每题带推荐。
- [竞品对标](references/prd-benchmark.md)：给出方案选项或需要竞品行为、行业公约事实时读取，按证据分级取证并落到 `<需求名>_竞品分析.md` 的对标矩阵。
- [下游审查清单](references/downstream-review.md)：成稿前或文稿检查时按需加载对照排查，消除研发与测试下游断点，不做多角色扮演。
- [交付规范](references/delivery.md)：成稿保存与交付检查时读取。
- [来源快照](references/snapshot.md)：Confluence 页面或远程来源下载封装时读取。
- [原型规范](references/prototype-analysis.md)：涉及图片／原型分析时读取。
- [Confluence 规范](references/publish-confluence.md)：仅明确写入平台时读取，复用 [布局骨架](assets/confluence-toc.xml)。
- `scripts/`：结构、引用及组合交付检查、Mermaid PNG 渲染与回归测试；执行无需通读源码。
- [AGENTS.md](AGENTS.md)：维护说明；`agents/openai.yaml`：宿主元数据。

## 维护验证

```text
python -B -m unittest discover -s scripts -p "test_*.py"
```

文稿校验命令、降级条件与检查边界见交付规范。静态测试不证明需求正确或宿主对话行为。改动后核对三条路由：所有 PRD 内容任务先读内容约定和模板；Confluence 来源检查需要图片；写入 Confluence 需要平台格式与图片映射。业务资料、生成文稿和分析材料存放仓库外。
