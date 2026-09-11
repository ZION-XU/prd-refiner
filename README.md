# PRD Refiner

面向中望 CAD 产品人员的 Agent Skill：编写 PRD 初版，检查、深化、精简或局部修改已有稿，帮助产品把内容交给团队继续讨论。

编写和优化必须使用 PRD 模板：模板规定框架，Skill 辅助整理、澄清和优化内容。旧稿会映射到 PRD 模板；已符合模板的稿件在框架内继续修改。仅检查任务报告问题，不改稿。

仓库只维护一份 [PRD 模板](assets/prd-template.md)。已有 PRD 是输入文稿，不代表另一套模板；`template`、`draft`、`existing` 是校验模式。模板内保留供人和 AI 使用的填写提示，出稿时清除；提问、工具和文件处理规则由 Skill 维护。

资料充分时直接出稿；有关键缺口时才澄清；用户可以先出稿或保留待讨论事项。初版不代表正式评审通过。团队在企业微信文档中的定稿、审批，以及 Confluence/Jira 录入不属于本 Skill，无需配置企业 MCP。

## 宿主安装与配置

本仓库是一个标准的独立 Agent Skill，无需安装脚本或依赖编译，直接放置或链接到对应 Agent 宿主的 Skill 目录即可生效：

- **全局配置**：将本仓库目录软链接（符号链接 / Junction）或复制到所用 Agent 宿主的全局 Skill 目录下，例如：
  - Antigravity / Gemini CLI：`~/.gemini/antigravity/skills/prd-refiner`
  - Claude Code：`~/.claude/skills/prd-refiner`
  - OpenAI Codex / 其他支持 Skill 规范的宿主：对应的全局 skills 目录
- **项目/工作区配置**：若仅在特定项目中使用，可直接将本仓库放置或链接至该项目根目录下的 `.agents/skills/prd-refiner`（或 `.agent/skills/prd-refiner`）。

开发与使用时建议使用目录软链接指向同一份源文件，避免副本漂移。

## 使用

通过宿主支持的方式调用（例如显式调用 `$prd-refiner` 或 `/prd-refiner`），例如：

```text
$prd-refiner 根据这些资料写一份初版，不能确定的内容标明。
$prd-refiner 我只有一个想法：统计图纸里的设备。帮我厘清任务、比较必要的方案，再逐步写成 PRD。
$prd-refiner 只检查这份 PRD 的歧义和遗漏，不改文件。
$prd-refiner 精简这份 PRD，保留原有规则和数值。
$prd-refiner 按这条变更修改 FR-002，保持其他功能，检查相关验收。
```

本轮通常输出 `prd.md`，也可按需求名或版本另存；源稿默认保留。用户核对后可带着明确未决事项进入团队讨论。必要图片随文稿保存，不强制多份需求附件。

## 用旧 PRD 实测

直接提供旧稿和优化目的，无须额外要求迁移模板：

```text
$prd-refiner 优化这份旧 PRD，保留有效规则、数值、来源与必要图片；缺口先指出，不能确定的内容标明，按 PRD 模板另存优化稿，分别说明结构调整和内容变更。
```

新稿编写和旧稿优化都检验模板与 Skill 的配合。局部修改也使用模板框架，但其他功能的含义保持。保留原稿、实际问答、输出和人工核对记录，便于发现实际遗漏、错误补充及意外改动；真实需求与输出放在仓库外。

## 维护入口

- [SKILL.md](SKILL.md)：路由、决策及出稿规则。
- [内容标准](references/prd-standard.md)、[模板](assets/prd-template.md)：共用规则与输出结构。
- [工作流](references/workflow.md)：检查、澄清、局部修改和接续。
- [需求探索](references/discover.md)：把简短想法还原为任务、问题、基本约束和候选方向。
- [竞品分析](references/competitor-analysis.md)：按需查证与归纳，区分观察、启发和本产品决定。
- [澄清方法](references/clarify.md)：依赖追问、假设与反例检验，回答后回写和收敛。
- [内容细化](references/specify.md)：从场景展开规则、相关分支和可判断的验收。
- [内容检查](references/review.md)：十二方面按需扫描及四类角色的具体检查动作。
- [原型规范](references/prototype-analysis.md)：图文证据与可读能力边界。
- [结构校验器](scripts/validate_prd.py)：`template`、`draft`、`existing` 三种只读检查；通过不代表需求正确。

## 验证与维护

Python 3.10 及以上可运行标准库校验与回归：

```text
python scripts/validate_prd.py <文稿路径> --profile template
python -B -m unittest discover -s scripts -p test_validate_prd.py
```

新编和优化初版均使用 `--profile template`，按模板组织的未完成工作稿使用 `--profile draft`；`--profile existing` 仅诊断输入旧稿，不检查 PRD 模板框架，不能用于判定优化输出合格。脚本通过只说明已检查的结构，不证明业务正确或正式评审通过。

本版实际宿主安装验证仍待完成；元信息检查、脚本回归和手工或隔离模拟不能替代它。安装后应验证显式调用、充分资料直接出稿、只检查不改源稿、局部修改和本地结果可打开；本轮补充的稀疏想法探索、竞品证据处理、依赖追问与回答回写，也需真实调用验证。无需配置 MCP 或企业账号。

仓库仅维护 Skill 核心、模板、必要参考、校验及测试。版本历史由 Git 维护；不保留历史方案、企业系统配置或生成的文稿。
