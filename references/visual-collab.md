# 可编辑图表（Excalidraw 场景）

## 生成可编辑场景文件

```bash
python scripts/story_map_to_excalidraw.py --data <绝对路径.json> --output <绝对路径.excalidraw>
```

- 输入契约见 [JSON 结构](../assets/story-map-schema.md)。
- 布局与卡片高度由脚本算（文字按容器宽度预先换行），所以卡片不会重叠；不要改用“先画元素再调坐标”的方式生成。
- 产物在 [excalidraw.com](https://excalidraw.com)（File → Open）或 Excalidraw 桌面版里直接打开即可编辑。
- emoji 默认保留：浏览器渲染正常、观感更好；只有需要跨机像素级一致时才加 `--strip-emoji`。按 [JSON 结构 · 内容边界](../assets/story-map-schema.md#内容边界)，emoji 只做状态提示，别让它承担语义。
- 源文件按 [成稿与交付](delivery.md) 放 `.assets/`，渲染出的图片放 `.assets/images/`。

## 出图：命令行 SVG/PNG

```bash
python scripts/render_story_map_vector.py --data <绝对路径.json> --output <绝对路径.svg> --format svg
python scripts/render_story_map_vector.py --data <绝对路径.json> --output <绝对路径.png> --format png --scale 2
```

- SVG 由脚本纯 Python 序列化，秒级、矢量、体积小，进正文与 Confluence 首选。
- PNG 走浏览器光栅化：把 SVG 画到 canvas 再 `toBlob`，支持 `--scale`（默认 2），约 3 秒，完整不裁边——**不是页面截图**。
- 在 excalidraw.com 或桌面版里改过 `.excalidraw` 后，也可以直接用它的 Export 出图（PNG/SVG 都支持、可选 scale）。
- **不要用浏览器截图**（`--screenshot`）：窗口尺寸与缩放不可靠，容易把图底部裁掉。

## 让 AI 直接改 `.excalidraw`

`.excalidraw` 就是 JSON（`type`、`version`、`elements`、`appState`、`files`），可以直接读写，但四条不能破：

1. **矩形与文字成对**：矩形的 `boundElements` 指向文字的 id，文字用 `containerId` 指回矩形；只改一边会让文字脱框。
2. **改文案要改两处**：文字的 `text`（含换行）与 `originalText` 同时改，并按新行数更新高度，坐标跟着容器重新居中。
3. **id 与版本**：新增元素 id 必须唯一；改动后 `version` 自增、`versionNonce` 与 `seed` 换新值，否则应用可能忽略本次改动。
4. **改布局要成对移动**：容器和文字的 `x`/`y`/`width`/`height` 一起改，文字不会自动跟随容器。

## 边界

- 图上的 FR 编号与活动划分必须是正文已确认的；没确认的先回正文解决，不能先画进图再补正文（判据见 [JSON 结构 · 内容边界](../assets/story-map-schema.md#内容边界)）。
- 交付形态（图片落点、命名、正文引用方式）归 [成稿与交付](delivery.md)，此处只写指针。
- 在官方页面上做的改动不在工作区里：要留档就导回 `.assets/`，不要假设可回溯。
