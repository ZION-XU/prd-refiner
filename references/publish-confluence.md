# Confluence 写入

仅在用户明确要求新建、修改、追加、发布或同步到 Confluence 时读取。仅提供来源页面不授权写入。

## 1. 目标与更新策略

- **新建**：核对站点、空间、父页面路径及标题。存在同名页时核实后再操作。
- **单章修改**：优先使用 `confluence_update_page_section`，`heading_text` 精确匹配标题，`new_content` 从标题下一行开始，仅包含替换正文，使用 Storage 格式。
- **全文修改**：基于最新 Storage 合并授权片段后提交，保留范围外正文、宏、附件与历史；提交前核对远端版本防止并发覆盖。

## 2. Storage 格式转换与原生锚点

将本地 Markdown 转换为符合规范的 Storage XML 格式（提交时 `content_format=storage`）：

```bash
python scripts/convert_to_storage.py <Markdown绝对路径> --output <输出XML绝对路径>
```

转换脚本自动处理以下工程契约：
- **布局封装**：自动加载 [布局骨架](../assets/confluence-toc.xml)，将前置信息与正文分别嵌入双栏浮动目录与单栏全宽主体；
- **定义锚点**：每个 FR、BR、AC、NFR、DEC、RK、SRC 条目在定义处插入小写编号锚点：
  ```xml
  <ac:structured-macro ac:name="anchor"><ac:parameter ac:name="">fr-001</ac:parameter></ac:structured-macro>
  ```
- **同页引用**：自动转换为原生同页链接跳转：
  ```xml
  <ac:link ac:anchor="fr-001"><ac:plain-text-link-body><![CDATA[直线计数（FR-001）]]></ac:plain-text-link-body></ac:link>
  ```
- **LaTeX 符号降级**：自动将 `$\ge$`、`$\le$`、`$\to$`、`$\pm$` 等伪数学 LaTeX 语法清洗为原生 Unicode 符号（`≥`、`≤`、`→`、`±`），杜绝页面公式渲染乱码；
- **XML 语法清洗**：自动转义表格及正文中的非 HTML 尖括号（如 `<全部其他值>`），并调用 ElementTree 验证 XML 合法性。

## 3. 图片与图表规范

- **普通图片与流程图资产（推荐）**：引用的本地图片须为可显示的图片（源文件先导出，见 [成稿与交付](delivery.md) §1）。业务流程图、架构图等图表推荐由宿主环境（Host Harness / 插件工具 / 外部生成器）预先绘制并直接落盘为图片（PNG/SVG）至 `<工作区>/.assets/images/`，正文以标准 Markdown 图片语法引用；上传至目标页面附件后在正文中以附件名引用：`<ac:image><ri:attachment ri:filename="图片名.png"/></ac:image>`；严禁保留本地路径或临时 URL。
- **Mermaid 源码围栏（兼容备用）**：若正文包含 ```mermaid 代码块，执行渲染脚本生成 PNG 并上传附件：
  ```bash
  python scripts/render_mermaid.py <Markdown路径>
  ```
  正文对应位置替换为附件引用 `<ac:image><ri:attachment ri:filename="mermaid-<哈希>.png"/></ac:image>`。Confluence 正文不得保留 Mermaid 源码围栏或 SVG 宏。

## 4. 目录与排版布局

- **默认全宽 + 右上浮动折叠目录**：新完整稿复用 [布局骨架](../assets/confluence-toc.xml)：
  - 文首 `two_right_sidebar`：左格仅放文档信息与修订表（不含目录）；右格放包含 `zwFloatingTocRight` 类的浮动折叠目录。
  - 后续 `single`：放全宽正文。正文不保留任何手写目录或 `[TOC]` 标记。
  - **禁令**：使用浮动目录时，正文严禁包含 `code` 或 `noformat` 宏（会导致目录遮挡失效）；长代码改用文本排版或附件展示。
- 用户明确要求正文目录（`--layout inline`）或双栏时遵循其要求。

## 5. 交付校验与回读

提交前及回读 Storage 后，执行组合交付检查：

```bash
python scripts/validate_delivery.py <Storage文件> --workspace <工作区根目录> --markdown <已保存Markdown>
```

| 场景 | 对应参数 | 说明 |
|---|---|---|
| **仅远程交付** | `--remote-only`（省略 `--markdown`） | 用户明确不交付本地稿 |
| **正文内联目录** | `--layout inline` | 用户指定正文目录而非浮动折叠目录 |
| **外部图片 / 位置回退** | `--image-policy external` / `--reference-policy location` | 外部图床或环境不支持锚点时使用 |

写入完成后必须回读实际页面，核对版本递增、授权范围 diff 及图片/锚点显示。
