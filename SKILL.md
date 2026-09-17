---
name: prd-refiner
description: 辅助中望 CAD 产品人员编写、优化和检查 PRD；处理含原型图片的资料，并按团队格式交付本地文稿或 Confluence 页面。仅在明确点名 prd-refiner（含 $prd-refiner 或 /prd-refiner）时启动。
---

# PRD Refiner

按用户任务处理 PRD；以下仅规定团队、资料和平台特有约束。

## 先读共同规范

- 每次显式调用本 Skill 处理 PRD 内容时，在分析资料或给出检查意见前，同时读取 [唯一模板](assets/prd-template.md)和 [内容约定](references/prd-standard.md)；已在本任务上下文读过则复用。检查或片段修改只处理用户范围，模板字段和示例不构成本期要求。

## 按需取证

- **Confluence 页面作为来源时**，即使用户只问“哪里需要优化”，读取并遵循 [来源快照](references/snapshot.md)。
- 涉及图片、界面原型或视觉资料时，读取并遵循 [原型分析](references/prototype-analysis.md)。

## 审查与缺口发现

- 只检查任务、实质优化或交付完整 PRD 前，结合规范基准，读取并遵循 [下游视角审查](references/downstream-review.md)。
- 资料或原型已确证的问题直接修正；将规范缺失与各视角下游风险合并去重，梳理出关键决断。

## 产品澄清

- 若确有必须由产品决定的缺口，将关键事项合并，使用宿主原生提问工具一次性澄清；未收到的回答不算确认。用户要求先出稿时保留未决。

## 交付与写入

- 输出完整本地稿时按模板成稿，并读取 [交付](references/delivery.md)处理文件、来源图片、编号链接、版本和校验；片段任务只交付片段。来源页不是默认写入目标。
- 用户明确要求写入 Confluence 时读取并遵循 [平台写入](references/publish-confluence.md)。用户指定其他布局或交付方式时遵循其要求。
