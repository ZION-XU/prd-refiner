# 二维用户故事地图 JSON 结构

`scripts/render_story_map.py` 的输入契约。准备 JSON 时按本文件填，无需通读源码。

```bash
python scripts/render_story_map.py --data <绝对路径.json> --output <绝对路径.png>
```

- `--output` 省略时默认写入 `<json 所在目录>/.assets/images/story-map.png`；建议显式传入以遵守 [成稿与交付](../references/delivery.md) §1 的落盘公约。
- 卡片内容全部做 HTML 转义，`&`、`<`、`>` 可直接写入正文。
- 依赖本机 Chrome / Edge / Chromium 做无头渲染；找不到时脚本会输出一份独立 HTML 并以非零码退出，需人工打开截图或改用轻量流程图（见 [内容约定](../references/prd-standard.md) §4）。

## 顶层字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `title` | 否 | 地图标题，默认「二维用户故事地图」 |
| `badge` | 否 | 标题右侧标签（版本号等） |
| `core_value` | 否 | 页眉「核心价值」，取自第 1 章业务目标 |
| `role` | 否 | 页眉「核心角色」，取自第 1 章用户与角色 |
| `activities` | **是** | 横向主干用户活动数组，顺序即从左到右的先后关系 |
| `releases` | **是** | 纵向阶段切片数组，自上而下按优先级／价值排序 |

## `activities[]`（横向主干）

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 建议 | 活动编号，如 `ACT-1`；缺省时显示为 `STAGE 01` 形式 |
| `name` | **是** | 活动名称，如「发现服务」 |
| `desc` | 否 | 一句话说明该活动做什么 |

`id` 与 `name` 都可以作为 `stories[].activity` 的取值（见下）。

## `releases[]`（纵向阶段切片）

| 字段 | 必填 | 说明 |
|---|---|---|
| `theme` | 否 | 只能是 `mvp`、`next`、`future` 三者之一，决定泳道与卡片的配色；缺省为 `mvp` |
| `badge` | 否 | 泳道标签，如 `MVP Release`；缺省显示 `Release` |
| `title` | 否 | 阶段名称，如「第 1 阶段」 |
| `desc` | 否 | 阶段目标或范围 |
| `stories` | **是** | 该阶段的用户故事卡片数组 |

## `releases[].stories[]`（卡片）

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 建议 | 故事编号，如 `US-001` |
| `title` | **是** | 卡片主标题 |
| `activity` | **是** | 归属哪个活动：填 `activities[]` 的下标（从 0 开始）、或该活动的 `id`／`name`；无法识别时归入第一列 |
| `desc` | 否 | 卡片补充说明 |
| `fr` | 否 | 关联的功能编号，如 `FR-001`；建议填写以便与正文互查 |
| `tag` | 否 | 卡片底部高亮标签（优先级、状态等） |

## 最小可用示例

```json
{
  "title": "服务发布工具 用户故事地图",
  "badge": "V1.0",
  "core_value": "把发布流程从人工拼命令收敛为可复现的一条龙",
  "role": "GIS 工程师",
  "activities": [
    { "id": "ACT-1", "name": "发现服务", "desc": "查找与定位可用服务" },
    { "id": "ACT-2", "name": "加载服务", "desc": "解析图层与数据源" }
  ],
  "releases": [
    {
      "theme": "mvp",
      "badge": "MVP Release",
      "title": "第 1 阶段：核心连通",
      "desc": "打通从发现到渲染的最短路径",
      "stories": [
        {
          "id": "US-001",
          "activity": "ACT-1",
          "fr": "FR-001",
          "title": "按关键字检索服务",
          "desc": "支持输入名称或关键字过滤服务列表",
          "tag": "P0"
        },
        {
          "id": "US-002",
          "activity": 1,
          "fr": "FR-002",
          "title": "渲染图层",
          "desc": "将要素添加到当前图面",
          "tag": "P0"
        }
      ]
    },
    {
      "theme": "next",
      "badge": "Next Release",
      "title": "第 2 阶段：复用与留痕",
      "desc": "补齐历史记录与批量能力",
      "stories": [
        {
          "id": "US-003",
          "activity": "发现服务",
          "fr": "FR-003",
          "title": "最近使用",
          "desc": "记忆常用服务入口"
        }
      ]
    }
  ]
}
```

## 内容边界

- 故事地图只呈现**已在正文确认**的活动划分、阶段归属与条目索引；未决的归属与优先级按 [内容约定](../references/prd-standard.md) §4 登记为 DEC，不得先画进地图再补正文。
- 图中不得出现正文没有的 FR 编号；每个 `fr` 值都应能在主稿中找到对应定义。
