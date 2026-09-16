# Confluence 写入

仅明确要求新建、修改、追加、发布或同步时读取。仅提供来源页面不授权写入。普通本地交付与只读分析不加载本文件。

## 目标与范围

已有明确目标和授权时直接执行。缺少目标或范围时先准备能确定的正文；能读取候选目标时再给出拟改差异，随后澄清缺失信息。目标未确定时不声称已核对差异。

- **新建**：核对站点、空间、父页面路径及标题。用户已明确指定时直接执行；需要代选位置时展示真实父级路径、链接和拟建标题，等待确认。存在同名页时先辨明是否为目标，不擅自覆盖或创建重复页；中间层级和独立记录页须有对应授权。
- **修改**：读取指定页面正文、位置和当前版本，展示实际链接与变更范围。局部修改／追加保留其余正文、宏、附件引用和历史。整页替换须有对具体页面和范围的明确授权；“优化／同步”本身不代表全文替换。
- 单章修改时，宿主提供 `confluence_update_page_section` 则先从原始正文核对目标标题的准确文字和唯一性，再用 `heading_text` 指定标题；`new_content` 仅放标题下的替换正文，不重复放标题。需要保留原生宏或结构时使用其 Storage 格式。标题匹配不唯一或工具不可用时，基于最新原始 Storage 合并授权片段后提交完整正文，保留范围外表示，不整页往返转换 Markdown。改标题、移父级、删除附件或子页不包含在正文修改内。
- 提交前再核对目标与最新版本，记录版本说明；并发变更须重新读取，原授权范围仍明确且不丢他人内容时才合并。响应不确定先只读确认是否成功，不盲重试或另选目标。
- 修改后回读实际版本并核对前后差异，不假定版本固定加一。缺少 diff 工具时对照前后 Storage；不删历史或删页重建。

用户可先自行建页再提供地址，页内已有内容仍按修改规则保护。目标／范围未明前不创建、改写、移动页面或上传附件。

## 提交格式与引用

按 [交付规范](delivery.md)准备本地稿（明确仅远程除外），检查最终待提交的 Storage，再提交同一份正文。使用 `content_format=storage` 或宿主等价参数；不能假定转换器会正确生成原生锚点。接口无法提交 Storage 时保留稿件并报告限制。工具的 `content_file` 可能指服务端路径，未核实共享路径时使用其支持的正文参数。

每个定义使用小写稳定编号作原生锚点，引用用原生同页链接，两者完全对应。锚点在唯一完整定义处，不在索引处；FR、BR、AC、DEC 等适用类型都要检查。示例：

```xml
<ac:structured-macro ac:name="anchor" ac:schema-version="1">
  <ac:parameter ac:name="">fr-001</ac:parameter>
</ac:structured-macro>
<h3>直线计数（FR-001）</h3>
<p><ac:link ac:anchor="fr-001"><ac:plain-text-link-body><![CDATA[直线计数（FR-001）]]></ac:plain-text-link-body></ac:link></p>
```

表格定义的锚点放对应单元格。多条引用逐项带名称；局部更新保留范围外旧锚点及有效链接，必要时在授权定义处加稳定别名。修复本次范围内的错误或重复目标，范围外问题单独报告。确实无法跳转时按内容及交付规范标注准确位置和限制。

## 图片与 Mermaid 门禁

提交前枚举本地 Markdown 中的全部图片引用和 Mermaid 代码块，逐项形成“本地来源 → 本地图片文件 → Confluence 附件名 → Storage 引用”的映射。普通图片上传或复用内容一致的现有附件；Storage 使用实际附件名，不保留本机路径、临时 URL 或仅文件名文本。

每个 Mermaid 代码块先按正文内容计算 SHA-256 前 12 位。写回 Confluence 只使用 `mermaid-<哈希>.png`，不使用 SVG 附件；目标站点只读页面不能稳定以内嵌图片显示 SVG。运行 `python scripts/render_mermaid.py <Markdown路径>`，由工具调用 Mermaid CLI 和本机 Edge／Chrome／Chromium，将源码直接渲染为白底高清 PNG 并保存到 `.assets/<需求名>/images/`；首次缺少 Mermaid CLI 时，工具通过 `npx` 获取固定版本。JSON 报告只有整体为 `complete` 且每项为 `rendered` 或 `reused` 才可继续。随后上传目标页面，在对应位置改为 `<ac:image><ri:attachment ri:filename="mermaid-<哈希>.png"/></ac:image>`。本地 Markdown 可保留 Mermaid 源码，Confluence 正文不得保留 Mermaid 围栏、SVG 替代物、代码宏或未上传的占位图。无法渲染、上传或建立逐图映射时保留本地稿并报告发布未完成，不能提交缺图页面后报告成功。

## 目录与排版

默认全宽正文＋右上浮动折叠原生目录。新完整稿复用 [布局骨架](../assets/confluence-toc.xml)：

- 文首 `two_right_sidebar` 左格放文档信息／修订表，右格放整个 `div.zwFloatingTocRight → expand → rich-text-body → toc`。
- 后续 `single` 放全宽正文。用 Storage 片段替换两个占位，文首为空用 `<p><br/></p>`；已有布局原位合并，不嵌套新布局。
- 浮动类包裹整个折叠组，不添加 `position`、`top`、`right`、`bottom`、`left` 等内联定位或尺寸补丁；右侧原生格定起始位置。中望站点必须保留骨架中的 `<div class="zwFloatingTocRight" style="background-color: #ffffff; z-index: 1000;">`：白色不透明背景防止正文透显，`z-index: 1000` 防止正文图片覆盖目录。提交前及回读后均检查这两个声明仍存在；新站点需另行核对。旧页仅在布局迁移已授权时清理多余样式。
- `toc` 的 minLevel/maxLevel 对应实际标题层级，排除“目录”自身；移除旧静态目录时保留相邻正文。

`zwFloatingTocRight` 是中望站点样式，非 Confluence 通用能力。新站点先核对支持，缺失时说明依赖并提供替代方案，不自行修改全局／空间 CSS。用户明确选择正文目录或全文双栏时遵循；局部修改旧页不自动迁移目录。全文双栏不在当前组合检查支持范围内，应报告静态布局未验证，不能冒用 floating 或 inline 声称通过。

使用浮动折叠目录时，Storage 正文不得含 `code`／`noformat` 宏；实测两者会遮挡目录。流程、状态和长代码改用原生排版、已上传的渲染图片或附件，短代码可行内显示。普通图片在上述 `z-index` 条件下允许使用并核对显示。正文目录等非浮动布局不套用此禁令；Mermaid 的渲染与附件门禁适用于所有布局。

故事地图保持活动与故事的二维关系及功能引用；不假定独立 HTML 的 CSS 或脚本在编辑后仍可用。

表格保持表头、行列和换行。图片优先复用有效附件；新增图片上传后引用实际名称，例如 `<ac:image><ri:attachment ri:filename="图.png"/></ac:image>`，跨页附件带真实页面上下文。XML 正文及属性正确转义，不重复转义。

## 回读

新建核对页面 ID、位置与正文；修改核对实际版本、授权范围内差异及范围外内容保留。对最终待提交和回读 Storage 运行交付规范中的组合检查；局部旧缺陷与本轮变更分别报告。

另核对两种格式的正文、表格、版本和附件；编号集合相同不证明语义相同。能查看页面时检查范围、索引、规则、验收和表格目标的实际跳转，以及目录折叠、滚动遮挡和图片。无法查看时明确“静态检查通过，点击和浮动效果未验证”。

格式参考：[Storage](https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html)、[版本比较](https://confluence.atlassian.com/doc/page-history-and-page-comparison-views-139379.html)。站点样式依据：[实现说明](https://confluence.zwcad.com/pages/viewpage.action?pageId=110925610)、[使用说明](https://confluence.zwcad.com/pages/viewpage.action?pageId=190089634)；无需每次重新访问已知格式说明。
