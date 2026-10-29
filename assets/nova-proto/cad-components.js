/**
 * ====================================================================
 * Nova CAD/BIM Web Components 核心库 (cad-components.js)
 * 单源真理源: Figma 53 Pages BIM 标准组件库
 * 架构机制: L1 官方核心组件 + L2 局部变体 + L3 PM草稿反哺防御机制
 * 运行方式: 原生 Web Components (Custom Elements + Shadow DOM)，零编译依赖
 * ====================================================================
 */

// 内嵌组件库全景清册 (支持 file:// 协议直接双击打开页面，零 CORS 阻塞)
window.NOVA_MANIFEST = {
  "project": "Nova CAD/BIM Design System",
  "source_file_key": "mtY1cdLoClLSdbo1noAryL",
  "last_synced": "2026-10-28 17:51:49",
  "components": {
    "button": {
      "name": "按钮 Button",
      "tag": "cad-button",
      "qt_class": "QPushButton",
      "category": "1. 通用基础",
      "page_id": "252:4",
      "status": "synced",
      "total_variants": 544,
      "dimensions": [
        "size",
        "图标",
        "尺寸",
        "数量",
        "焦点",
        "状态",
        "种类",
        "类型"
      ],
      "component_sets": [
        {
          "id": "260:229",
          "name": "按钮",
          "variants": 511
        },
        {
          "id": "326:2795",
          "name": "按钮组合",
          "variants": 33
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "input": {
      "name": "输入框 Input",
      "tag": "cad-input",
      "qt_class": "QLineEdit",
      "category": "3. 数据录入",
      "page_id": "252:14",
      "status": "synced",
      "total_variants": 387,
      "dimensions": [
        "内容",
        "单位",
        "占比",
        "填充",
        "尺寸",
        "状态",
        "禁用",
        "箭头",
        "类型",
        "聚焦"
      ],
      "component_sets": [
        {
          "id": "380:2224",
          "name": "input 基础输入框",
          "variants": 24
        },
        {
          "id": "483:4900",
          "name": "input-Angle  角度输入框",
          "variants": 12
        },
        {
          "id": "713:12746",
          "name": "input-color 颜色输入框",
          "variants": 10
        },
        {
          "id": "483:2707",
          "name": "search-box 搜索框",
          "variants": 30
        },
        {
          "id": "483:3925",
          "name": "Input-Range区间输入框",
          "variants": 12
        },
        {
          "id": "483:3976",
          "name": "元素/Range区间值",
          "variants": 20
        },
        {
          "id": "7036:463",
          "name": "元素/前后缀",
          "variants": 120
        },
        {
          "id": "483:7254",
          "name": "Textarea 多行文本",
          "variants": 12
        },
        {
          "id": "3135:7106",
          "name": "input-slider 滑块输入框",
          "variants": 10
        },
        {
          "id": "3135:7157",
          "name": "元素/slider-bar2",
          "variants": 10
        },
        {
          "id": "6564:2391",
          "name": "input-column 数值输入框",
          "variants": 48
        },
        {
          "id": "6743:12605",
          "name": "元素/数值输入框/箭头",
          "variants": 7
        },
        {
          "id": "7037:641",
          "name": "前后缀输入框",
          "variants": 72
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "checkbox": {
      "name": "复选框 Checkbox",
      "tag": "cad-checkbox",
      "qt_class": "QCheckBox",
      "category": "3. 数据录入",
      "page_id": "252:30",
      "status": "synced",
      "total_variants": 56,
      "dimensions": [
        "半选",
        "已选",
        "数量",
        "焦点",
        "状态",
        "纵向",
        "说明"
      ],
      "component_sets": [
        {
          "id": "372:2319",
          "name": "Checkbox-Input",
          "variants": 14
        },
        {
          "id": "372:2402",
          "name": "Checkbox",
          "variants": 28
        },
        {
          "id": "379:2424",
          "name": "Checkbox-group",
          "variants": 14
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "radio": {
      "name": "单选框 Radio",
      "tag": "cad-radio",
      "qt_class": "QRadioButton",
      "category": "3. 数据录入",
      "page_id": "252:19",
      "status": "synced",
      "total_variants": 44,
      "dimensions": [
        "已选",
        "数量",
        "焦点",
        "状态",
        "纵向",
        "说明"
      ],
      "component_sets": [
        {
          "id": "328:2173",
          "name": "Radio-Input",
          "variants": 10
        },
        {
          "id": "328:2196",
          "name": "Radio",
          "variants": 20
        },
        {
          "id": "328:2365",
          "name": "Radio-Group",
          "variants": 14
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "select": {
      "name": "选择器 Select",
      "tag": "cad-select",
      "qt_class": "QComboBox",
      "category": "3. 数据录入",
      "page_id": "252:52",
      "status": "synced",
      "total_variants": 120,
      "dimensions": [
        "交互",
        "关闭",
        "填充",
        "尺寸",
        "数量",
        "显示选项",
        "更多",
        "状态",
        "禁用",
        "类型"
      ],
      "component_sets": [
        {
          "id": "483:5106",
          "name": "select 选择器",
          "variants": 92
        },
        {
          "id": "509:4006",
          "name": "tag",
          "variants": 16
        },
        {
          "id": "509:4055",
          "name": "tag-group",
          "variants": 12
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "switch": {
      "name": "开关 Switch",
      "tag": "cad-switch",
      "qt_class": "QCheckBox (Switch style)",
      "category": "3. 数据录入",
      "page_id": "252:31",
      "status": "synced",
      "total_variants": 32,
      "dimensions": [
        "size",
        "尺寸",
        "开启",
        "焦点",
        "禁用"
      ],
      "component_sets": [
        {
          "id": "328:2542",
          "name": "Switch-input",
          "variants": 16
        },
        {
          "id": "502:3240",
          "name": "Switch-group",
          "variants": 16
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "slider": {
      "name": "滑块 Slider",
      "tag": "cad-slider",
      "qt_class": "QSlider",
      "category": "3. 数据录入",
      "page_id": "252:33",
      "status": "synced",
      "total_variants": 28,
      "dimensions": [
        "占比",
        "双滑标",
        "数值框",
        "状态",
        "禁用"
      ],
      "component_sets": [
        {
          "id": "512:7327",
          "name": "元素/slider-bar",
          "variants": 4
        },
        {
          "id": "512:8181",
          "name": "Slider 滑块",
          "variants": 24
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "tabs": {
      "name": "标签页 Tabs",
      "tag": "cad-tabs",
      "qt_class": "QTabWidget",
      "category": "2. 导航菜单",
      "page_id": "252:37",
      "status": "synced",
      "total_variants": 137,
      "dimensions": [
        "下划线",
        "关闭",
        "尺寸",
        "悬停",
        "数量",
        "状态",
        "禁用",
        "类型",
        "选中"
      ],
      "component_sets": [
        {
          "id": "543:8587",
          "name": "元素/标签页",
          "variants": 8
        },
        {
          "id": "597:2658",
          "name": "元素/分割线视图",
          "variants": 4
        },
        {
          "id": "597:2920",
          "name": "元素/纵向标签页",
          "variants": 4
        },
        {
          "id": "589:8737",
          "name": "元素/选项卡",
          "variants": 8
        },
        {
          "id": "593:11450",
          "name": "元素/滑动选项卡",
          "variants": 28
        },
        {
          "id": "589:8495",
          "name": "标签页",
          "variants": 16
        },
        {
          "id": "589:8815",
          "name": "选项卡",
          "variants": 16
        },
        {
          "id": "593:11743",
          "name": "滑动选项卡",
          "variants": 14
        },
        {
          "id": "597:2706",
          "name": "分割线视图",
          "variants": 8
        },
        {
          "id": "597:2961",
          "name": "纵向标签页",
          "variants": 7
        },
        {
          "id": "780:29330",
          "name": "元素/视图",
          "variants": 4
        },
        {
          "id": "801:10827",
          "name": "视图",
          "variants": 8
        },
        {
          "id": "4463:44386",
          "name": "元素/视图2",
          "variants": 8
        },
        {
          "id": "4473:45319",
          "name": "视图2",
          "variants": 4
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "typography": {
      "name": "字体 Typography",
      "tag": "cad-typography",
      "qt_class": "QLabel",
      "category": "1. 通用基础",
      "page_id": "252:20",
      "status": "synced",
      "total_variants": 8,
      "dimensions": [
        "大小",
        "类型"
      ],
      "component_sets": [
        {
          "id": "257:437",
          "name": "标题",
          "variants": 2
        },
        {
          "id": "257:448",
          "name": "内容",
          "variants": 6
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "divider": {
      "name": "分割线 Divider",
      "tag": "cad-divider",
      "qt_class": "QFrame (HLine/VLine)",
      "category": "1. 通用基础",
      "page_id": "252:21",
      "status": "synced",
      "total_variants": 8,
      "dimensions": [
        "方向",
        "类型",
        "虚线"
      ],
      "component_sets": [
        {
          "id": "260:137",
          "name": "分割线",
          "variants": 8
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "scrollbar": {
      "name": "滚动条 Scrollbar",
      "tag": "cad-scrollbar",
      "qt_class": "QScrollBar",
      "category": "1. 通用基础",
      "page_id": "252:22",
      "status": "synced",
      "total_variants": 4,
      "dimensions": [
        "大小",
        "类型"
      ],
      "component_sets": [
        {
          "id": "260:35",
          "name": "纵向",
          "variants": 4
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "link": {
      "name": "链接 Link",
      "tag": "cad-link",
      "qt_class": "QLabel (Hyperlink)",
      "category": "1. 通用基础",
      "page_id": "252:5",
      "status": "synced",
      "total_variants": 16,
      "dimensions": [
        "尺寸",
        "焦点",
        "状态"
      ],
      "component_sets": [
        {
          "id": "294:4066",
          "name": "link",
          "variants": 16
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "icon": {
      "name": "图标 icon",
      "tag": "cad-icon",
      "qt_class": "QIcon",
      "category": "2. 导航菜单",
      "page_id": "252:3",
      "status": "synced",
      "total_variants": 2,
      "dimensions": [
        "size"
      ],
      "component_sets": [
        {
          "id": "257:367",
          "name": "Icon-Wrapper",
          "variants": 2
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "menu": {
      "name": "菜单 Menu",
      "tag": "cad-menu",
      "qt_class": "QMenu",
      "category": "2. 导航菜单",
      "page_id": "252:8",
      "status": "synced",
      "total_variants": 9,
      "dimensions": [
        "图标类型",
        "展开",
        "状态"
      ],
      "component_sets": [
        {
          "id": "294:5411",
          "name": "1级菜单",
          "variants": 2
        },
        {
          "id": "294:5440",
          "name": "2级菜单",
          "variants": 4
        },
        {
          "id": "294:6668",
          "name": "菜单组合",
          "variants": 3
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "dropdown": {
      "name": "下拉菜单 Dropdown",
      "tag": "cad-dropdown",
      "qt_class": "QToolButton / QMenu",
      "category": "2. 导航菜单",
      "page_id": "252:12",
      "status": "synced",
      "total_variants": 190,
      "dimensions": [
        "全选",
        "半选",
        "图标大小",
        "已选",
        "悬停",
        "悬停/按下",
        "悬停/点击",
        "数量",
        "显示图标",
        "显示说明",
        "禁用",
        "类型"
      ],
      "component_sets": [
        {
          "id": "509:5079",
          "name": "dropdown/menu-item",
          "variants": 18
        },
        {
          "id": "2709:26111",
          "name": "dropdown/selectall",
          "variants": 7
        },
        {
          "id": "509:5496",
          "name": "dropdown-menu",
          "variants": 153
        },
        {
          "id": "511:3862",
          "name": "dropdown/trigger1",
          "variants": 9
        },
        {
          "id": "511:5083",
          "name": "dropdown/menu-item-group",
          "variants": 3
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "color_picker": {
      "name": "颜色选择器 Color Picker",
      "tag": "cad-color-picker",
      "qt_class": "QColorDialog",
      "category": "3. 数据录入",
      "page_id": "252:53",
      "status": "synced",
      "total_variants": 4,
      "dimensions": [
        "更多",
        "类型"
      ],
      "component_sets": [
        {
          "id": "518:10157",
          "name": "颜色选择器Color Picker",
          "variants": 4
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "tree_select": {
      "name": "树选择 TreeSelect",
      "tag": "cad-tree-select",
      "qt_class": "QTreeWidget (Popup)",
      "category": "3. 数据录入",
      "page_id": "252:39",
      "status": "synced",
      "total_variants": 524,
      "dimensions": [
        "子级数量",
        "子集数量",
        "层级",
        "展开",
        "已选",
        "显示图标",
        "显示箭头",
        "根数量",
        "状态",
        "类型",
        "选中"
      ],
      "component_sets": [
        {
          "id": "599:3769",
          "name": "元素/树选择/选项",
          "variants": 384
        },
        {
          "id": "604:379",
          "name": "元素/下拉树/3level",
          "variants": 36
        },
        {
          "id": "604:5658",
          "name": "元素/下拉树/2level",
          "variants": 36
        },
        {
          "id": "604:9454",
          "name": "元素/下拉树/1level",
          "variants": 36
        },
        {
          "id": "4459:38926",
          "name": "下拉树 TreeSelect",
          "variants": 32
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "material_select": {
      "name": "材质选择器 Material Select",
      "tag": "cad-material-select",
      "qt_class": "QWidget (Material)",
      "category": "3. 数据录入",
      "page_id": "252:54",
      "status": "synced",
      "total_variants": 12,
      "dimensions": [
        "填充",
        "悬停",
        "状态",
        "禁用",
        "选中"
      ],
      "component_sets": [
        {
          "id": "3779:1770",
          "name": "材质选择器",
          "variants": 12
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "picker": {
      "name": "拾取 Picker",
      "tag": "cad-picker",
      "qt_class": "QWidget (CAD Picker)",
      "category": "3. 数据录入",
      "page_id": "252:36",
      "status": "synced",
      "total_variants": 24,
      "dimensions": [
        "填充",
        "状态",
        "类型"
      ],
      "component_sets": [
        {
          "id": "6451:56183",
          "name": "拾取",
          "variants": 24
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "file_loader": {
      "name": "载入文件 File Loader",
      "tag": "cad-file-loader",
      "qt_class": "QFileDialog",
      "category": "3. 数据录入",
      "page_id": "6451:56655",
      "status": "synced",
      "total_variants": 24,
      "dimensions": [
        "图标位置",
        "填充",
        "状态",
        "类型"
      ],
      "component_sets": [
        {
          "id": "6451:56656",
          "name": "载入",
          "variants": 24
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "picture": {
      "name": "图片 Picture",
      "tag": "cad-picture",
      "qt_class": "QLabel (Pixmap)",
      "category": "3. 数据录入",
      "page_id": "252:38",
      "status": "synced",
      "total_variants": 52,
      "dimensions": [
        "填充",
        "尺寸",
        "形态",
        "形状",
        "悬停",
        "状态",
        "禁用",
        "行数",
        "选中"
      ],
      "component_sets": [
        {
          "id": "599:3098",
          "name": "图片选择器",
          "variants": 12
        },
        {
          "id": "725:21579",
          "name": "元素/图片卡片",
          "variants": 10
        },
        {
          "id": "725:21841",
          "name": "图片列表",
          "variants": 30
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "form": {
      "name": "表单 Form",
      "tag": "cad-form",
      "qt_class": "QFormLayout",
      "category": "3. 数据录入",
      "page_id": "252:35",
      "status": "synced",
      "total_variants": 359,
      "dimensions": [
        "交互",
        "分割线",
        "双滑标",
        "填充",
        "多选",
        "大小",
        "字数",
        "尺寸",
        "展开",
        "文本对齐",
        "样式",
        "状态",
        "类型",
        "纵向",
        "背景"
      ],
      "component_sets": [
        {
          "id": "524:8223",
          "name": "label",
          "variants": 6
        },
        {
          "id": "531:4914",
          "name": "Form Item/基础输入框",
          "variants": 12
        },
        {
          "id": "3135:7536",
          "name": "Form Item/滑块输入框",
          "variants": 10
        },
        {
          "id": "713:16422",
          "name": "Form Item/颜色输入框",
          "variants": 10
        },
        {
          "id": "654:32979",
          "name": "Form Item/图片",
          "variants": 12
        },
        {
          "id": "3779:7366",
          "name": "Form Item/材质",
          "variants": 12
        },
        {
          "id": "541:9012",
          "name": "Form Item/拾取",
          "variants": 24
        },
        {
          "id": "2944:35742",
          "name": "Form Item/添加",
          "variants": 24
        },
        {
          "id": "2944:37644",
          "name": "Form Item/载入",
          "variants": 24
        },
        {
          "id": "2944:39203",
          "name": "Form Item/编辑",
          "variants": 24
        },
        {
          "id": "2944:41465",
          "name": "Form Item/计算器",
          "variants": 24
        },
        {
          "id": "541:6509",
          "name": "Form Item/选择器-24",
          "variants": 48
        },
        {
          "id": "3322:14537",
          "name": "Form Item/选择器-20",
          "variants": 48
        },
        {
          "id": "539:6957",
          "name": "Form Item/单选框",
          "variants": 2
        },
        {
          "id": "539:8130",
          "name": "Form Item/滑块",
          "variants": 2
        },
        {
          "id": "539:7525",
          "name": "Form Item/复选框",
          "variants": 2
        },
        {
          "id": "541:8950",
          "name": "Form Item/链接",
          "variants": 2
        },
        {
          "id": "539:7948",
          "name": "Form Item/开关",
          "variants": 3
        },
        {
          "id": "539:6769",
          "name": "Form Item/多行文本",
          "variants": 12
        },
        {
          "id": "531:5907",
          "name": "Form Item/角度输入框",
          "variants": 12
        },
        {
          "id": "531:6104",
          "name": "Form Item/数值输入框",
          "variants": 12
        },
        {
          "id": "538:10438",
          "name": "Form Item/区间输入框",
          "variants": 12
        },
        {
          "id": "539:6394",
          "name": "Form Item/搜索框",
          "variants": 10
        },
        {
          "id": "541:18051",
          "name": "分组标题",
          "variants": 8
        },
        {
          "id": "542:8575",
          "name": "模块标题",
          "variants": 2
        },
        {
          "id": "5536:47287",
          "name": "展开收起分组标题",
          "variants": 2
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "tree": {
      "name": "树形控件 Tree",
      "tag": "cad-tree",
      "qt_class": "QTreeWidget",
      "category": "3. 数据录入",
      "page_id": "5454:66767",
      "status": "synced",
      "total_variants": 528,
      "dimensions": [
        "子级数量",
        "子集数量",
        "层级",
        "展开",
        "已选",
        "显示图标",
        "显示箭头",
        "树图标",
        "根数量",
        "状态",
        "类型"
      ],
      "component_sets": [
        {
          "id": "5454:66768",
          "name": "元素/树型控件/选项",
          "variants": 384
        },
        {
          "id": "5454:68306",
          "name": "元素/树型控件/3level",
          "variants": 36
        },
        {
          "id": "5454:68537",
          "name": "元素/树型控件/2level",
          "variants": 36
        },
        {
          "id": "5454:68754",
          "name": "元素/树型控件/1level",
          "variants": 36
        },
        {
          "id": "5454:68971",
          "name": "元素/树形控件",
          "variants": 32
        },
        {
          "id": "5499:54085",
          "name": "树形控件Tree",
          "variants": 4
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "table": {
      "name": "表格 Table",
      "tag": "cad-table",
      "qt_class": "QTableWidget",
      "category": "3. 数据录入",
      "page_id": "252:41",
      "status": "synced",
      "total_variants": 722,
      "dimensions": [
        "子级数量",
        "子集数量",
        "尺寸",
        "层级",
        "展开",
        "悬停",
        "按钮数量",
        "数量",
        "文本对齐",
        "显示为空",
        "暂无数据",
        "标题类型",
        "树列表",
        "类型",
        "编辑",
        "行高",
        "选中",
        "默认显示"
      ],
      "component_sets": [
        {
          "id": "606:8652",
          "name": "元素/text",
          "variants": 18
        },
        {
          "id": "6910:32233",
          "name": "元素/Tag",
          "variants": 12
        },
        {
          "id": "6906:24339",
          "name": "元素/编辑",
          "variants": 60
        },
        {
          "id": "609:12529",
          "name": "元素/tree/层级",
          "variants": 288
        },
        {
          "id": "609:9198",
          "name": "元素/checkbox",
          "variants": 18
        },
        {
          "id": "609:9289",
          "name": "元素/radio",
          "variants": 18
        },
        {
          "id": "609:9573",
          "name": "元素/switch",
          "variants": 18
        },
        {
          "id": "609:9987",
          "name": "元素/button",
          "variants": 24
        },
        {
          "id": "7481:27371",
          "name": "元素/button",
          "variants": 72
        },
        {
          "id": "609:8940",
          "name": "元素/link",
          "variants": 18
        },
        {
          "id": "606:9099",
          "name": "元素/header",
          "variants": 30
        },
        {
          "id": "609:15031",
          "name": "列/text",
          "variants": 12
        },
        {
          "id": "6910:25798",
          "name": "列/Edit",
          "variants": 40
        },
        {
          "id": "609:20981",
          "name": "列/tree",
          "variants": 4
        },
        {
          "id": "609:18061",
          "name": "列/button",
          "variants": 4
        },
        {
          "id": "609:17215",
          "name": "列/数值",
          "variants": 12
        },
        {
          "id": "609:15983",
          "name": "列/Number",
          "variants": 4
        },
        {
          "id": "609:16350",
          "name": "列/checkbox",
          "variants": 4
        },
        {
          "id": "609:16673",
          "name": "列/radio",
          "variants": 4
        },
        {
          "id": "609:16900",
          "name": "列/switch",
          "variants": 4
        },
        {
          "id": "6910:33227",
          "name": "列/Tag",
          "variants": 4
        },
        {
          "id": "609:22428",
          "name": "元素/tree/3st",
          "variants": 12
        },
        {
          "id": "609:22780",
          "name": "元素/tree/2nd",
          "variants": 12
        },
        {
          "id": "609:23760",
          "name": "元素/tree/1st",
          "variants": 12
        },
        {
          "id": "611:46865",
          "name": "表格组合",
          "variants": 16
        },
        {
          "id": "7694:32424",
          "name": "元素/表格模块标题",
          "variants": 2
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "tooltip": {
      "name": "文字气泡 Tooltip",
      "tag": "cad-tooltip",
      "qt_class": "QToolTip",
      "category": "4. 数据反馈",
      "page_id": "368:1277",
      "status": "synced",
      "total_variants": 8,
      "dimensions": [
        "箭头位置"
      ],
      "component_sets": [
        {
          "id": "611:59624",
          "name": "Tooltip",
          "variants": 8
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "message": {
      "name": "全局提示 Message",
      "tag": "cad-message",
      "qt_class": "QMessageBox (Toast)",
      "category": "4. 数据反馈",
      "page_id": "252:43",
      "status": "synced",
      "total_variants": 4,
      "dimensions": [
        "类型"
      ],
      "component_sets": [
        {
          "id": "616:64339",
          "name": "Message 全局提示",
          "variants": 4
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "modal": {
      "name": "对话框 Modal",
      "tag": "cad-dialog",
      "qt_class": "QDialog",
      "category": "4. 数据反馈",
      "page_id": "252:45",
      "status": "synced",
      "total_variants": 8,
      "dimensions": [
        "尺寸",
        "类型"
      ],
      "component_sets": [
        {
          "id": "327:2318",
          "name": "对话框",
          "variants": 6
        },
        {
          "id": "611:61456",
          "name": "元素",
          "variants": 2
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "sweetalert": {
      "name": "弹窗提示 SweetAlert",
      "tag": "cad-alert",
      "qt_class": "QMessageBox",
      "category": "4. 数据反馈",
      "page_id": "252:44",
      "status": "synced",
      "total_variants": 5,
      "dimensions": [
        "多行",
        "类型"
      ],
      "component_sets": [
        {
          "id": "615:64052",
          "name": "     弹窗提示 SweetAlert ",
          "variants": 5
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "panel": {
      "name": "面板 Panel",
      "tag": "cad-panel",
      "qt_class": "QDockWidget",
      "category": "4. 数据反馈",
      "page_id": "851:7915",
      "status": "synced",
      "total_variants": 24,
      "dimensions": [
        "右分割线",
        "左分割线",
        "悬停",
        "数量",
        "标签",
        "状态",
        "禁用",
        "类型",
        "选中"
      ],
      "component_sets": [
        {
          "id": "851:7916",
          "name": "面板组合",
          "variants": 6
        },
        {
          "id": "851:7965",
          "name": "元素/面板标题",
          "variants": 2
        },
        {
          "id": "851:8384",
          "name": "元素/面版标签",
          "variants": 11
        },
        {
          "id": "851:8488",
          "name": "元素/标签组合",
          "variants": 5
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "popover": {
      "name": "气泡卡片 Popover",
      "tag": "cad-popover",
      "qt_class": "QWidget (Popup)",
      "category": "4. 数据反馈",
      "page_id": "252:46",
      "status": "synced",
      "total_variants": 20,
      "dimensions": [
        "文字内容",
        "箭头位置"
      ],
      "component_sets": [
        {
          "id": "615:61783",
          "name": "Popover",
          "variants": 20
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "popconfirm": {
      "name": "气泡确认框 Popconfirm",
      "tag": "cad-popconfirm",
      "qt_class": "QMessageBox",
      "category": "4. 数据反馈",
      "page_id": "615:61944",
      "status": "synced",
      "total_variants": 32,
      "dimensions": [
        "箭头位置",
        "类型"
      ],
      "component_sets": [
        {
          "id": "615:61945",
          "name": "     气泡确认框 Popconfirm",
          "variants": 32
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "progress": {
      "name": "进度条 Bar",
      "tag": "cad-progress",
      "qt_class": "QProgressBar",
      "category": "4. 数据反馈",
      "page_id": "253:55",
      "status": "synced",
      "total_variants": 132,
      "dimensions": [
        "占比",
        "尺寸",
        "直角"
      ],
      "component_sets": [
        {
          "id": "616:64670",
          "name": "元素/Scrubber",
          "variants": 66
        },
        {
          "id": "616:64975",
          "name": "Progress",
          "variants": 66
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "composite_input": {
      "name": "单选+图片+输入",
      "tag": "cad-composite-input",
      "qt_class": "QWidget",
      "category": "5. 业务场景",
      "page_id": "253:56",
      "status": "synced",
      "total_variants": 20,
      "dimensions": [
        "数字",
        "高亮"
      ],
      "component_sets": [
        {
          "id": "731:40563",
          "name": "元素/图片输入",
          "variants": 20
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "wall_tool": {
      "name": "绘制墙体",
      "tag": "cad-wall-tool",
      "qt_class": "QWidget",
      "category": "5. 业务场景",
      "page_id": "252:48",
      "status": "synced",
      "total_variants": 2,
      "dimensions": [
        "显示填充"
      ],
      "component_sets": [
        {
          "id": "661:2859",
          "name": "材质选择",
          "variants": 2
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "family_mgr": {
      "name": "族库管理",
      "tag": "cad-family-mgr",
      "qt_class": "QWidget",
      "category": "5. 业务场景",
      "page_id": "253:57",
      "status": "synced",
      "total_variants": 0,
      "dimensions": [],
      "component_sets": [],
      "updated_at": "2026-10-28 17:32:22"
    },
    "axis_grid": {
      "name": "绘制轴网",
      "tag": "cad-axis-grid",
      "qt_class": "QWidget",
      "category": "5. 业务场景",
      "page_id": "253:58",
      "status": "synced",
      "total_variants": 0,
      "dimensions": [],
      "component_sets": [],
      "updated_at": "2026-10-28 17:32:22"
    },
    "door_tool": {
      "name": "门",
      "tag": "cad-door-tool",
      "qt_class": "QWidget",
      "category": "5. 业务场景",
      "page_id": "253:59",
      "status": "synced",
      "total_variants": 0,
      "dimensions": [],
      "component_sets": [],
      "updated_at": "2026-10-28 17:32:22"
    },
    "stair_tool": {
      "name": "双跑楼梯",
      "tag": "cad-stair-tool",
      "qt_class": "QWidget",
      "category": "5. 业务场景",
      "page_id": "843:3972",
      "status": "synced",
      "total_variants": 0,
      "dimensions": [],
      "component_sets": [],
      "updated_at": "2026-10-28 17:32:22"
    },
    "options_dialog": {
      "name": "ZWCAD选项",
      "tag": "cad-options-dialog",
      "qt_class": "QDialog",
      "category": "5. 业务场景",
      "page_id": "843:3979",
      "status": "synced",
      "total_variants": 0,
      "dimensions": [],
      "component_sets": [],
      "updated_at": "2026-10-28 17:32:22"
    },
    "tag": {
      "name": "标签 Tag",
      "tag": "cad-tag",
      "qt_class": "QLabel (Tag)",
      "category": "1. 通用基础",
      "page_id": "6906:18142",
      "status": "synced",
      "total_variants": 48,
      "dimensions": [
        "尺寸",
        "形状",
        "类型",
        "颜色"
      ],
      "component_sets": [
        {
          "id": "6906:19794",
          "name": "标签 Tag",
          "variants": 48
        }
      ],
      "updated_at": "2026-10-28 17:32:21"
    },
    "alert_banner": {
      "name": "警告提示 Alert",
      "tag": "cad-alert-banner",
      "qt_class": "QFrame (AlertBanner)",
      "category": "4. 数据反馈",
      "page_id": "6921:42395",
      "status": "synced",
      "total_variants": 10,
      "dimensions": [
        "标题",
        "类型"
      ],
      "component_sets": [
        {
          "id": "6921:42396",
          "name": "Alert 警告提示",
          "variants": 10
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "filter": {
      "name": "筛选 Filter",
      "tag": "cad-filter",
      "qt_class": "QWidget (FilterBar)",
      "category": "4. 数据反馈",
      "page_id": "7477:26492",
      "status": "synced",
      "total_variants": 6,
      "dimensions": [
        "数量",
        "选中"
      ],
      "component_sets": [
        {
          "id": "7478:27255",
          "name": "元素/tag",
          "variants": 2
        },
        {
          "id": "7480:27350",
          "name": "元素/小标题",
          "variants": 4
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "quick_nav": {
      "name": "快速导航 QuickNav",
      "tag": "cad-quick-nav",
      "qt_class": "QToolBar (QuickAccess)",
      "category": "5. 业务场景",
      "page_id": "1712:473",
      "status": "synced",
      "total_variants": 6,
      "dimensions": [
        "类型"
      ],
      "component_sets": [
        {
          "id": "4023:38999",
          "name": "CAD快速导航栏",
          "variants": 3
        },
        {
          "id": "2344:28620",
          "name": "BIM 快速导航栏",
          "variants": 3
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "ribbon": {
      "name": "功能区 Ribbon",
      "tag": "cad-ribbon",
      "qt_class": "QRibbonBar",
      "category": "5. 业务场景",
      "page_id": "1461:34231",
      "status": "synced",
      "total_variants": 0,
      "dimensions": [],
      "component_sets": [],
      "updated_at": "2026-10-28 17:32:22"
    },
    "status_bar": {
      "name": "状态栏 StatusBar",
      "tag": "cad-status-bar",
      "qt_class": "QStatusBar",
      "category": "5. 业务场景",
      "page_id": "2342:27138",
      "status": "synced",
      "total_variants": 6,
      "dimensions": [
        "类型"
      ],
      "component_sets": [
        {
          "id": "4023:37133",
          "name": "CAD全局状态栏",
          "variants": 2
        },
        {
          "id": "2344:28021",
          "name": "BIM全局状态栏",
          "variants": 2
        },
        {
          "id": "4461:44250",
          "name": "BIM视图状态栏",
          "variants": 2
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "project_browser": {
      "name": "项目浏览器 ProjectBrowser",
      "tag": "cad-project-browser",
      "qt_class": "QDockWidget (ProjectTree)",
      "category": "5. 业务场景",
      "page_id": "6376:55263",
      "status": "synced",
      "total_variants": 0,
      "dimensions": [],
      "component_sets": [],
      "updated_at": "2026-10-28 17:32:22"
    },
    "property_panel": {
      "name": "属性面板 PropertyPanel",
      "tag": "cad-property-panel",
      "qt_class": "QDockWidget (PropertyGrid)",
      "category": "5. 业务场景",
      "page_id": "7462:11469",
      "status": "synced",
      "total_variants": 0,
      "dimensions": [],
      "component_sets": [],
      "updated_at": "2026-10-28 17:32:22"
    },
    "command_tool": {
      "name": "命令工具 CommandTool",
      "tag": "cad-command-tool",
      "qt_class": "QWidget (CommandBar)",
      "category": "5. 业务场景",
      "page_id": "7823:839",
      "status": "synced",
      "total_variants": 20,
      "dimensions": [
        "展开",
        "状态",
        "类型"
      ],
      "component_sets": [
        {
          "id": "7823:1026",
          "name": "元素/工具",
          "variants": 10
        },
        {
          "id": "7823:1072",
          "name": "元素/标题",
          "variants": 6
        },
        {
          "id": "7823:1101",
          "name": "工具栏",
          "variants": 4
        }
      ],
      "updated_at": "2026-10-28 17:32:22"
    },
    "main_toolbar": {
      "name": "主工具栏 MainToolbar",
      "tag": "cad-main-toolbar",
      "qt_class": "QToolBar",
      "category": "5. 业务场景",
      "page_id": "7930:2104",
      "status": "synced",
      "total_variants": 0,
      "dimensions": [],
      "component_sets": [],
      "updated_at": "2026-10-28 17:32:22"
    }
  },
  "prototypes_audit": {
    "table_create_prototype.html": {
      "audited_at": "2026-10-28 17:51:49",
      "file_name": "table_create_prototype.html",
      "total_interactive_elements": 31,
      "official_components_count": 31,
      "draft_components_count": 0,
      "raw_elements_count": 0,
      "coverage_rate": "100.0%",
      "official_rate": "100.0%",
      "draft_rate": "0.0%",
      "breakdown": {
        "official": [
          "cad-dialog",
          "cad-form-group",
          "cad-select",
          "cad-button",
          "cad-icon",
          "cad-form-group",
          "cad-radio",
          "cad-radio",
          "cad-select",
          "cad-button",
          "cad-icon",
          "cad-radio",
          "cad-form-group",
          "cad-checkbox",
          "cad-table",
          "cad-form-group",
          "cad-radio",
          "cad-radio",
          "cad-form-group",
          "cad-icon",
          "cad-input",
          "cad-input",
          "cad-divider",
          "cad-icon",
          "cad-input",
          "cad-input",
          "cad-form-group",
          "cad-select",
          "cad-select",
          "cad-select",
          "cad-alert"
        ],
        "draft": [],
        "raw": []
      }
    }
  }
};

// 通用草稿角标渲染辅助
function renderDraftBadge(isDraft, tooltip = "PM自造草稿组件 (待反哺入库 Figma)") {
  if (!isDraft) return '';
  return `
    <span class="cad-draft-badge" title="${tooltip}">
      草稿
    </span>
  `;
}

const COMMON_DRAFT_STYLE = `
  .cad-draft-badge {
    position: absolute;
    top: -6px;
    right: -8px;
    background: var(--cad-color-draft, #8B5CF6);
    color: #FFFFFF;
    font-size: 9px;
    padding: 1px 4px;
    border-radius: 4px;
    line-height: 1.1;
    font-weight: bold;
    pointer-events: auto;
    cursor: help;
    box-shadow: 0 1px 3px rgba(139, 92, 246, 0.4);
    z-index: 100;
  }
`;

/**
 * --------------------------------------------------------------------
 * 1. <cad-button> 按钮组件 (映射自 Figma ComponentSet 260:229)
 * --------------------------------------------------------------------
 */
class CadButton extends HTMLElement {
  static get observedAttributes() {
    return ['type', 'size', 'disabled', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback(name, oldVal, newVal) {
    if (oldVal !== newVal) this.render();
  }

  render() {
    const type = this.getAttribute('type') || 'secondary'; // 'primary' | 'secondary' | 'text'
    const size = this.getAttribute('size') || 'small';      // 'small' | 'large'
    const disabled = this.hasAttribute('disabled');
    const isDraft = this.getAttribute('status') === 'draft';

    const height = size === 'large' ? 'var(--cad-height-large, 32px)' : 'var(--cad-height-small, 24px)';
    const padding = size === 'large' ? 'var(--cad-padding-large, 4px 12px)' : 'var(--cad-padding-small, 2px 8px)';

    let bg = 'var(--cad-color-bg-white, #FFFFFF)';
    let color = 'var(--cad-color-text-main, #1F2329)';
    let border = '1px solid var(--cad-color-border-default, #E3E5E7)';
    let hoverBg = 'var(--cad-color-bg-hover, #F2F4F6)';
    let activeBg = 'var(--cad-color-bg-active, #E5E7EB)';

    if (type === 'primary') {
      bg = disabled ? 'var(--cad-color-primary-disabled, #BFD3FE)' : 'var(--cad-color-primary, #266EFF)';
      color = 'var(--cad-color-text-white, #FFFFFF)';
      border = '1px solid transparent';
      hoverBg = 'var(--cad-color-primary-hover, #4785FF)';
      activeBg = 'var(--cad-color-primary-active, #1D58DB)';
    } else if (type === 'text') {
      bg = 'transparent';
      border = '1px solid transparent';
      color = disabled ? 'var(--cad-color-text-placeholder, #A6A9AD)' : 'var(--cad-color-text-main, #1F2329)';
      hoverBg = 'var(--cad-color-bg-hover, #F2F4F6)';
    } else if (disabled) {
      bg = 'var(--cad-color-bg-disabled, #F5F7FA)';
      color = 'var(--cad-color-text-placeholder, #A6A9AD)';
      border = '1px solid var(--cad-color-border-default, #E3E5E7)';
    }

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          vertical-align: middle;
          position: relative;
        }
        button {
          all: unset;
          box-sizing: border-box;
          width: 100%;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: var(--cad-gap-sm, 6px);
          height: ${height};
          padding: ${padding};
          font-size: var(--cad-font-size-base, 12px);
          font-family: var(--cad-font-family, sans-serif);
          font-weight: 500;
          color: ${color};
          background: ${bg};
          border: ${border};
          border-radius: var(--cad-radius-base, 4px);
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          user-select: none;
          transition: background 0.15s, border-color 0.15s, opacity 0.15s;
          white-space: nowrap;
        }
        button:hover:not(:disabled) {
          background: ${hoverBg};
        }
        button:active:not(:disabled) {
          background: ${activeBg};
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <button ${disabled ? 'disabled' : ''}>
        <slot></slot>
      </button>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-button', CadButton);

/**
 * --------------------------------------------------------------------
 * 2. <cad-input> 文本与数字输入框 (映射自 Figma ComponentSet 380:2224)
 * --------------------------------------------------------------------
 */
class CadInput extends HTMLElement {
  static get observedAttributes() {
    return ['value', 'placeholder', 'type', 'size', 'disabled', 'status', 'prefix-label', 'suffix-label', 'min', 'max', 'step'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback(name, oldVal, newVal) {
    if (oldVal === newVal) return;
    if (name === 'value') {
      const inp = this.shadowRoot ? this.shadowRoot.querySelector('input') : null;
      if (inp && inp.value !== (newVal || '')) {
        inp.value = newVal || '';
      }
      return; // 输入时不重建 DOM，保持焦点与输入法状态
    }
    this.render();
  }

  get value() {
    const inp = this.shadowRoot ? this.shadowRoot.querySelector('input') : null;
    return inp ? inp.value : (this.getAttribute('value') || '');
  }

  set value(val) {
    this.setAttribute('value', val);
    const inp = this.shadowRoot ? this.shadowRoot.querySelector('input') : null;
    if (inp && inp.value !== String(val)) {
      inp.value = val;
    }
  }

  render() {
    const val = this.getAttribute('value') || '';
    const placeholder = this.getAttribute('placeholder') || '';
    const type = this.getAttribute('type') || 'text';
    const size = this.getAttribute('size') || 'small';
    const disabled = this.hasAttribute('disabled');
    const isDraft = this.getAttribute('status') === 'draft';
    const prefix = this.getAttribute('prefix-label') || '';
    const suffix = this.getAttribute('suffix-label') || '';
    const min = this.getAttribute('min');
    const max = this.getAttribute('max');
    const step = this.getAttribute('step') || '1';

    const height = size === 'large' ? 'var(--cad-height-large, 32px)' : 'var(--cad-height-small, 24px)';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          vertical-align: middle;
          position: relative;
          width: 100%;
        }
        .input-wrapper {
          box-sizing: border-box;
          display: flex;
          align-items: center;
          height: ${height};
          background: ${disabled ? 'var(--cad-color-bg-disabled, #F5F7FA)' : 'var(--cad-color-bg-white, #FFFFFF)'};
          border: 1px solid var(--cad-color-border-default, #E3E5E7);
          border-radius: var(--cad-radius-base, 4px);
          padding: ${type === 'number' ? '0 0 0 6px' : '0 6px'};
          gap: 4px;
          overflow: hidden;
          transition: border-color 0.15s, box-shadow 0.15s;
        }
        .input-wrapper:hover:not(.disabled) {
          border-color: var(--cad-color-border-hover, #C0C4CC);
        }
        .input-wrapper.focus {
          border-color: var(--cad-color-primary, #266EFF);
          box-shadow: 0 0 0 1px var(--cad-color-primary, #266EFF);
        }
        input {
          all: unset;
          flex: 1;
          height: 100%;
          font-size: var(--cad-font-size-base, 12px);
          font-family: var(--cad-font-family, sans-serif);
          color: ${disabled ? 'var(--cad-color-text-placeholder, #A6A9AD)' : 'var(--cad-color-text-main, #1F2329)'};
          min-width: 0;
        }
        input::-webkit-outer-spin-button,
        input::-webkit-inner-spin-button {
          -webkit-appearance: none;
          margin: 0;
        }
        input::placeholder {
          color: var(--cad-color-text-placeholder, #A6A9AD);
        }
        .affix {
          font-size: 11px;
          color: var(--cad-color-text-secondary, #8A8D91);
          user-select: none;
          white-space: nowrap;
        }
        .spinners {
          display: flex;
          flex-direction: column;
          width: 18px;
          height: 100%;
          border-left: 1px solid var(--cad-color-border-default, #E3E5E7);
          background: ${disabled ? '#F5F7FA' : '#F8F9FA'};
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          flex-shrink: 0;
        }
        .spin-btn {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 7px;
          line-height: 1;
          color: ${disabled ? '#C0C4CC' : '#1F2329'};
          user-select: none;
        }
        .spin-btn.up {
          border-bottom: 1px solid var(--cad-color-border-default, #E3E5E7);
        }
        .spin-btn:hover {
          background: ${disabled ? 'transparent' : '#ECEEF1'};
          color: ${disabled ? '#C0C4CC' : 'var(--cad-color-primary, #266EFF)'};
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="input-wrapper ${disabled ? 'disabled' : ''}">
        ${prefix ? `<span class="affix">${prefix}</span>` : ''}
        <input 
          type="${type}" 
          value="${val}" 
          placeholder="${placeholder}" 
          ${disabled ? 'disabled' : ''}
          ${min !== null ? `min="${min}"` : ''}
          ${max !== null ? `max="${max}"` : ''}
          step="${step}"
        />
        ${suffix ? `<span class="affix">${suffix}</span>` : ''}
        ${type === 'number' ? `
          <div class="spinners">
            <span class="spin-btn up">▲</span>
            <span class="spin-btn down">▼</span>
          </div>
        ` : ''}
      </div>
      ${renderDraftBadge(isDraft)}
    `;

    const wrapper = this.shadowRoot.querySelector('.input-wrapper');
    const inputEl = this.shadowRoot.querySelector('input');

    inputEl.addEventListener('focus', () => wrapper.classList.add('focus'));
    inputEl.addEventListener('blur', () => wrapper.classList.remove('focus'));
    inputEl.addEventListener('input', (e) => {
      e.stopPropagation();
      this.setAttribute('value', e.target.value);
      this.dispatchEvent(new CustomEvent('input', { detail: { value: e.target.value }, bubbles: true, composed: true }));
      this.dispatchEvent(new CustomEvent('change', { detail: { value: e.target.value }, bubbles: true, composed: true }));
    });

    const up = this.shadowRoot.querySelector('.spin-btn.up');
    const down = this.shadowRoot.querySelector('.spin-btn.down');
    if (up && down && !disabled) {
      up.addEventListener('click', () => {
        let n = parseFloat(inputEl.value || 0) + parseFloat(step);
        if (max !== null && n > parseFloat(max)) n = parseFloat(max);
        inputEl.value = n;
        inputEl.dispatchEvent(new Event('input'));
      });
      down.addEventListener('click', () => {
        let n = parseFloat(inputEl.value || 0) - parseFloat(step);
        if (min !== null && n < parseFloat(min)) n = parseFloat(min);
        inputEl.value = n;
        inputEl.dispatchEvent(new Event('input'));
      });
    }
  }
}
customElements.define('cad-input', CadInput);

/**
 * --------------------------------------------------------------------
 * 3. <cad-checkbox> 复选框 (映射自 Figma ComponentSet 372:2402)
 * --------------------------------------------------------------------
 */
class CadCheckbox extends HTMLElement {
  static get observedAttributes() {
    return ['checked', 'disabled', 'status', 'indeterminate'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback(name, oldVal, newVal) {
    if (oldVal !== newVal) this.render();
  }

  get checked() {
    return this.hasAttribute('checked');
  }

  set checked(val) {
    if (val) this.setAttribute('checked', '');
    else this.removeAttribute('checked');
  }

  render() {
    const checked = this.hasAttribute('checked');
    const disabled = this.hasAttribute('disabled');
    const indeterminate = this.hasAttribute('indeterminate');
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          align-items: center;
          vertical-align: middle;
          position: relative;
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          user-select: none;
          gap: var(--cad-gap-sm, 6px);
          font-size: var(--cad-font-size-base, 12px);
          font-family: var(--cad-font-family, sans-serif);
          color: ${disabled ? 'var(--cad-color-text-placeholder, #A6A9AD)' : 'var(--cad-color-text-main, #1F2329)'};
        }
        .box {
          width: 14px;
          height: 14px;
          border-radius: var(--cad-radius-small, 2px);
          border: 1px solid ${checked || indeterminate ? 'var(--cad-color-primary, #266EFF)' : 'var(--cad-color-border-default, #E3E5E7)'};
          background: ${checked || indeterminate ? (disabled ? 'var(--cad-color-primary-disabled, #BFD3FE)' : 'var(--cad-color-primary, #266EFF)') : (disabled ? 'var(--cad-color-bg-disabled, #F5F7FA)' : '#FFFFFF')};
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.15s;
          box-sizing: border-box;
        }
        :host(:hover:not([disabled])) .box {
          border-color: var(--cad-color-primary, #266EFF);
        }
        .check-icon {
          width: 9px;
          height: 9px;
          fill: none;
          stroke: #FFFFFF;
          stroke-width: 2;
          stroke-linecap: round;
          stroke-linejoin: round;
          display: ${checked ? 'block' : 'none'};
        }
        .indeterminate-bar {
          width: 8px;
          height: 2px;
          background: #FFFFFF;
          display: ${indeterminate && !checked ? 'block' : 'none'};
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="box">
        <svg class="check-icon" viewBox="0 0 12 12">
          <polyline points="2 6 5 9 10 3"></polyline>
        </svg>
        <div class="indeterminate-bar"></div>
      </div>
      <span><slot></slot></span>
      ${renderDraftBadge(isDraft)}
    `;

    this.onclick = (e) => {
      if (disabled) return;
      this.checked = !this.checked;
      this.removeAttribute('indeterminate');
      this.dispatchEvent(new CustomEvent('change', { detail: { checked: this.checked }, bubbles: true, composed: true }));
    };
  }
}
customElements.define('cad-checkbox', CadCheckbox);

/**
 * --------------------------------------------------------------------
 * 4. <cad-radio> 单选框 (映射自 Figma ComponentSet 328:2196)
 * --------------------------------------------------------------------
 */
class CadRadio extends HTMLElement {
  static get observedAttributes() {
    return ['checked', 'disabled', 'status', 'name', 'value'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback(name, oldVal, newVal) {
    if (oldVal !== newVal) this.render();
  }

  get checked() {
    return this.hasAttribute('checked');
  }

  set checked(val) {
    if (val) this.setAttribute('checked', '');
    else this.removeAttribute('checked');
  }

  render() {
    const checked = this.hasAttribute('checked');
    const disabled = this.hasAttribute('disabled');
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          align-items: center;
          vertical-align: middle;
          position: relative;
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          user-select: none;
          gap: var(--cad-gap-sm, 6px);
          font-size: var(--cad-font-size-base, 12px);
          font-family: var(--cad-font-family, sans-serif);
          color: ${disabled ? 'var(--cad-color-text-placeholder, #A6A9AD)' : 'var(--cad-color-text-main, #1F2329)'};
        }
        .circle {
          width: 14px;
          height: 14px;
          border-radius: 50%;
          border: 1px solid ${checked ? 'var(--cad-color-primary, #266EFF)' : '#8C8C8C'};
          background: ${checked ? (disabled ? 'var(--cad-color-primary-disabled, #BFD3FE)' : 'var(--cad-color-primary, #266EFF)') : '#FFFFFF'};
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.15s;
          box-sizing: border-box;
          flex-shrink: 0;
        }
        :host(:hover:not([disabled])) .circle {
          border-color: var(--cad-color-primary, #266EFF);
        }
        .dot {
          width: 5px;
          height: 5px;
          border-radius: 50%;
          background: #FFFFFF;
          display: ${checked ? 'block' : 'none'};
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="circle">
        <div class="dot"></div>
      </div>
      <span><slot></slot></span>
      ${renderDraftBadge(isDraft)}
    `;

    this.onclick = () => {
      if (disabled || this.checked) return;
      const name = this.getAttribute('name');
      if (name) {
        document.querySelectorAll(`cad-radio[name="${name}"]`).forEach(r => {
          if (r !== this) r.removeAttribute('checked');
        });
      }
      this.checked = true;
      this.dispatchEvent(new CustomEvent('change', { detail: { value: this.getAttribute('value'), checked: true }, bubbles: true, composed: true }));
    };
  }
}
customElements.define('cad-radio', CadRadio);

/**
 * --------------------------------------------------------------------
 * 5. <cad-select> 下拉选择器 (映射自 Figma ComponentSet 483:5106)
 * --------------------------------------------------------------------
 */
class CadSelect extends HTMLElement {
  static get observedAttributes() {
    return ['value', 'placeholder', 'disabled', 'status', 'size'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback(name, oldVal, newVal) {
    if (oldVal === newVal) return;
    if (name === 'value') {
      const sel = this.shadowRoot ? this.shadowRoot.querySelector('select') : null;
      if (sel && sel.value !== newVal) sel.value = newVal;
      return;
    }
    this.render();
  }

  get value() {
    const sel = this.shadowRoot ? this.shadowRoot.querySelector('select') : null;
    return sel ? sel.value : (this.getAttribute('value') || '');
  }

  set value(val) {
    this.setAttribute('value', val);
    const sel = this.shadowRoot ? this.shadowRoot.querySelector('select') : null;
    if (sel) sel.value = val;
  }

  render() {
    const val = this.getAttribute('value') || '';
    const disabled = this.hasAttribute('disabled');
    const isDraft = this.getAttribute('status') === 'draft';
    const size = this.getAttribute('size') || 'small';
    const height = size === 'large' ? 'var(--cad-height-large, 32px)' : 'var(--cad-height-small, 24px)';
    // 将 Light DOM 中的 <option> 同步至内部原生 <select>
    const optionsHtml = this.innerHTML;

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          vertical-align: middle;
          position: relative;
          width: 100%;
        }
        select {
          width: 100%;
          height: ${height};
          box-sizing: border-box;
          background: ${disabled ? 'var(--cad-color-bg-disabled, #F5F7FA)' : '#FFFFFF'};
          color: ${disabled ? 'var(--cad-color-text-placeholder, #A6A9AD)' : 'var(--cad-color-text-main, #1F2329)'};
          border: 1px solid var(--cad-color-border-default, #E3E5E7);
          border-radius: var(--cad-radius-base, 4px);
          padding: 0 22px 0 8px;
          font-size: var(--cad-font-size-base, 12px);
          font-family: var(--cad-font-family, sans-serif);
          appearance: none;
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          outline: none;
          transition: border-color 0.15s;
        }
        select:hover:not(:disabled) {
          border-color: var(--cad-color-border-hover, #C0C4CC);
        }
        select:focus {
          border-color: var(--cad-color-primary, #266EFF);
        }
        .arrow {
          position: absolute;
          right: 7px;
          top: 50%;
          transform: translateY(-50%);
          pointer-events: none;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <select ${disabled ? 'disabled' : ''}>
        ${optionsHtml}
      </select>
      <span class="arrow">
        <svg width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M1 1L5 5L9 1" stroke="${disabled ? '#C0C4CC' : '#606266'}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </span>
      ${renderDraftBadge(isDraft)}
    `;

    const sel = this.shadowRoot.querySelector('select');
    if (val) sel.value = val;
    sel.addEventListener('change', (e) => {
      e.stopPropagation();
      this.setAttribute('value', e.target.value);
      this.dispatchEvent(new CustomEvent('change', { detail: { value: e.target.value }, bubbles: true, composed: true }));
    });
  }
}
customElements.define('cad-select', CadSelect);

/**
 * --------------------------------------------------------------------
 * 6. <cad-switch> 开关切换器 (映射自 Figma ComponentSet 252:31)
 * --------------------------------------------------------------------
 */
class CadSwitch extends HTMLElement {
  static get observedAttributes() {
    return ['checked', 'disabled', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback(name, oldVal, newVal) {
    if (oldVal !== newVal) this.render();
  }

  get checked() {
    return this.hasAttribute('checked');
  }

  set checked(val) {
    if (val) this.setAttribute('checked', '');
    else this.removeAttribute('checked');
  }

  render() {
    const checked = this.hasAttribute('checked');
    const disabled = this.hasAttribute('disabled');
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          align-items: center;
          vertical-align: middle;
          position: relative;
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          user-select: none;
          gap: 6px;
        }
        .track {
          width: 32px;
          height: 18px;
          border-radius: 9px;
          background: ${checked ? (disabled ? 'var(--cad-color-primary-disabled, #BFD3FE)' : 'var(--cad-color-primary, #266EFF)') : '#DCDFE6'};
          position: relative;
          transition: background 0.2s;
        }
        .thumb {
          width: 14px;
          height: 14px;
          border-radius: 50%;
          background: #FFFFFF;
          position: absolute;
          top: 2px;
          left: ${checked ? '16px' : '2px'};
          transition: left 0.2s;
          box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="track">
        <div class="thumb"></div>
      </div>
      <span><slot></slot></span>
      ${renderDraftBadge(isDraft)}
    `;

    this.onclick = () => {
      if (disabled) return;
      this.checked = !this.checked;
      this.dispatchEvent(new CustomEvent('change', { detail: { checked: this.checked }, bubbles: true, composed: true }));
    };
  }
}
customElements.define('cad-switch', CadSwitch);

/**
 * --------------------------------------------------------------------
 * 7. <cad-table-viewport> CAD 视口表格实时智能预览器 (Level 3 PM 自造草稿组件)
 * --------------------------------------------------------------------
 */
class CadTableViewport extends HTMLElement {
  static get observedAttributes() {
    return ['cols', 'rows', 'title-text', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback(name, oldVal, newVal) {
    if (oldVal !== newVal) this.render();
  }

  render() {
    const isDraft = this.getAttribute('status') === 'draft' || !this.hasAttribute('status');
    const cols = parseInt(this.getAttribute('cols') || '4', 10);
    const rows = parseInt(this.getAttribute('rows') || '5', 10);
    const title = this.getAttribute('title-text') || 'CAD 表格图元实时视口';

    let tableHtml = `<tr><td colspan="${cols}" class="cell-title">${title}</td></tr>`;
    tableHtml += `<tr>`;
    for (let c = 1; c <= cols; c++) {
      tableHtml += `<td class="cell-header">表头 ${c}</td>`;
    }
    tableHtml += `</tr>`;

    for (let r = 1; r <= Math.min(rows, 10); r++) {
      tableHtml += `<tr>`;
      for (let c = 1; c <= cols; c++) {
        tableHtml += `<td class="cell-data">数据</td>`;
      }
      tableHtml += `</tr>`;
    }

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          position: relative;
          width: 100%;
          border-radius: 4px;
          overflow: hidden;
        }
        .viewport {
          background-color: #18191c;
          background-image: 
            linear-gradient(to right, rgba(255,255,255,0.04) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255,255,255,0.04) 1px, transparent 1px);
          background-size: 16px 16px;
          min-height: 240px;
          padding: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
          box-sizing: border-box;
        }
        .cad-grid-table {
          border-collapse: collapse;
          color: #E2E8F0;
          font-family: var(--cad-font-family, sans-serif);
          font-size: 11px;
          box-shadow: 0 4px 16px rgba(0,0,0,0.5);
          background: rgba(30, 32, 38, 0.95);
        }
        .cad-grid-table td {
          border: 1px solid #4A5568;
          padding: 4px 8px;
          text-align: center;
          min-width: 48px;
        }
        .cell-title {
          background: #2B6CB0;
          color: #FFFFFF;
          font-weight: bold;
          font-size: 12px;
          letter-spacing: 0.5px;
        }
        .cell-header {
          background: #2D3748;
          color: #CBD5E0;
          font-weight: 500;
        }
        .cell-data {
          color: #A0AEC0;
        }
        .viewport-footer {
          position: absolute;
          bottom: 6px;
          right: 10px;
          font-size: 10px;
          color: #718096;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="viewport">
        <table class="cad-grid-table">
          ${tableHtml}
        </table>
        <div class="viewport-footer">视口网格: 16mm | 列: ${cols} | 行: ${rows}</div>
      </div>
      ${renderDraftBadge(isDraft, "PM自造草稿组件: CAD视口表格实时智能预览器 (待反哺 Figma 入库)")}
    `;
  }
}
customElements.define('cad-table-viewport', CadTableViewport);

/**
 * --------------------------------------------------------------------
 * 8. <cad-file-picker-input> 文件路径拾取复合组件 (Level 3 PM 自造草稿组件)
 * --------------------------------------------------------------------
 */
class CadFilePickerInput extends HTMLElement {
  static get observedAttributes() {
    return ['value', 'placeholder', 'button-text', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback(name, oldVal, newVal) {
    if (oldVal !== newVal) this.render();
  }

  get value() {
    return this.getAttribute('value') || '';
  }

  set value(val) {
    this.setAttribute('value', val);
  }

  render() {
    const isDraft = this.getAttribute('status') === 'draft' || !this.hasAttribute('status');
    const val = this.getAttribute('value') || '';
    const btnText = this.getAttribute('button-text') || '浏览...';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: flex;
          align-items: center;
          gap: 6px;
          width: 100%;
          position: relative;
        }
        .input-box {
          flex: 1;
          height: var(--cad-height-small, 24px);
          background: var(--cad-color-bg-white, #FFFFFF);
          border: 1px solid var(--cad-color-border-default, #E3E5E7);
          border-radius: var(--cad-radius-base, 4px);
          padding: 0 8px;
          font-size: var(--cad-font-size-base, 12px);
          font-family: var(--cad-font-family, sans-serif);
          color: var(--cad-color-text-main, #1F2329);
          outline: none;
          box-sizing: border-box;
        }
        button {
          height: var(--cad-height-small, 24px);
          padding: 2px 10px;
          background: var(--cad-color-bg-white, #FFFFFF);
          border: 1px solid var(--cad-color-border-default, #E3E5E7);
          border-radius: var(--cad-radius-base, 4px);
          font-size: var(--cad-font-size-base, 12px);
          color: var(--cad-color-text-main, #1F2329);
          cursor: pointer;
          white-space: nowrap;
          transition: background 0.15s;
        }
        button:hover {
          background: var(--cad-color-bg-hover, #F2F4F6);
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <input type="text" class="input-box" value="${val}" readonly />
      <button type="button">${btnText}</button>
      ${renderDraftBadge(isDraft, "PM自造草稿组件: CAD文件路径拾取复合组件 (待反哺 Figma 入库)")}
    `;

    const btn = this.shadowRoot.querySelector('button');
    btn.onclick = () => {
      this.dispatchEvent(new CustomEvent('pick-click', { bubbles: true, composed: true }));
    };
  }
}
customElements.define('cad-file-picker-input', CadFilePickerInput);

/**
 * --------------------------------------------------------------------
 * 9. <cad-alert> 弹窗提示 SweetAlert (映射自 Figma Page 252:44 / ComponentSet 615:64052)
 *    1:1 像素级复刻 Figma 原始矢量 SVG 图标、阴影、字重与间距
 * --------------------------------------------------------------------
 */
const CAD_ALERT_SVGS = {
  info: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9.93652 1.31348C14.769 1.31348 18.6865 5.23098 18.6865 10.0635C18.6865 14.896 14.769 18.8135 9.93652 18.8135C5.10403 18.8135 1.18652 14.896 1.18652 10.0635C1.18652 5.23098 5.10403 1.31348 9.93652 1.31348ZM9.93652 8.36209C10.3392 8.36209 10.6657 8.68855 10.6657 9.09125V14.1954C10.6657 14.5981 10.3392 14.9246 9.93652 14.9246C9.53382 14.9246 9.20736 14.5981 9.20736 14.1954V9.09125C9.20736 8.68855 9.53382 8.36209 9.93652 8.36209ZM9.93652 5.20237C10.4735 5.20237 10.9087 5.63764 10.9087 6.17459C10.9087 6.71153 10.4735 7.14681 9.93652 7.14681C9.39958 7.14681 8.9643 6.71153 8.9643 6.17459C8.9643 5.63764 9.39958 5.20237 9.93652 5.20237Z" fill-rule="evenodd" clip-rule="evenodd" fill="#266EFF"/></svg>`,
  success: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9.93774 1.31226C14.7702 1.31226 18.6877 5.22976 18.6877 10.0623C18.6877 14.8947 14.7702 18.8123 9.93774 18.8123C5.10525 18.8123 1.18774 14.8947 1.18774 10.0623C1.18774 5.22976 5.10525 1.31226 9.93774 1.31226ZM13.9543 7.35913C13.6696 7.07447 13.2078 7.07441 12.9231 7.35913L8.45337 11.8269L6.5647 9.93726L6.46313 9.85229C6.17902 9.65571 5.78647 9.68435 5.53345 9.93726C5.24869 10.222 5.24869 10.6837 5.53345 10.9685L7.9397 13.3748L8.04028 13.4587C8.32433 13.6555 8.71684 13.6275 8.96997 13.3748L13.9543 8.39038L14.0393 8.28979C14.2362 8.00561 14.2075 7.61225 13.9543 7.35913Z" fill="#00B42A"/></svg>`,
  warning: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9.93652 1.31348C14.769 1.31348 18.6865 5.23098 18.6865 10.0635C18.6865 14.896 14.769 18.8135 9.93652 18.8135C5.10403 18.8135 1.18652 14.896 1.18652 10.0635C1.18652 5.23098 5.10403 1.31348 9.93652 1.31348ZM9.93652 12.9801C10.4735 12.9801 10.9087 13.4154 10.9087 13.9524C10.9087 14.4893 10.4735 14.9246 9.93652 14.9246C9.39958 14.9246 8.9643 14.4893 8.9643 13.9524C8.9643 13.4154 9.39958 12.9801 9.93652 12.9801ZM9.93652 5.20237C10.3392 5.20237 10.6657 5.52882 10.6657 5.93153V11.0357C10.6657 11.4384 10.3392 11.7649 9.93652 11.7649C9.53382 11.7649 9.20736 11.4384 9.20736 11.0357V5.93153C9.20736 5.52882 9.53382 5.20237 9.93652 5.20237Z" fill-rule="evenodd" clip-rule="evenodd" fill="#F98A00"/></svg>`,
  danger: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 1.25C14.8325 1.25 18.75 5.16751 18.75 10C18.75 14.8325 14.8325 18.75 10 18.75C5.16751 18.75 1.25 14.8325 1.25 10C1.25 5.16751 5.16751 1.25 10 1.25ZM6.56767 6.56775C6.28291 6.85251 6.28291 7.31419 6.56767 7.59895L8.97376 10.0049L6.53487 12.4462C6.28338 12.7326 6.29431 13.169 6.56767 13.4424C6.85244 13.7271 7.31411 13.7271 7.59888 13.4424L10.0048 11.0362L12.4461 13.4753C12.7325 13.7268 13.169 13.7157 13.4424 13.4424C13.7271 13.1576 13.7271 12.696 13.4424 12.4112L11.0361 10.0049L13.4751 7.56395C13.7266 7.27754 13.7157 6.84111 13.4424 6.56775C13.1576 6.28299 12.6959 6.28299 12.4111 6.56775L10.0048 8.97384L7.56387 6.53495L7.52731 6.50487C7.24137 6.28481 6.82965 6.30578 6.56767 6.56775Z" fill-rule="evenodd" clip-rule="evenodd" fill="#EF4A4A"/></svg>`,
  close: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3.5 3.49999L12.5 12.5" stroke-linecap="round" stroke="#606266"/><path d="M3.49999 12.5L12.5 3.5" stroke-linecap="round" stroke="#606266"/></svg>`
};

const CAD_ALERT_DEFAULT_TITLES = {
  info: '普通消息',
  success: '成功通知',
  warning: '警告通知',
  danger: '危险通知'
};

const CAD_ALERT_MULTILINE_DEFAULT = `场地特殊地貌处理（A030205）采暖（A0404）、样板房（A050502）、销售区域临时绿化（A050504）、检测费（A0506）、室内水电工程（A0601）、消防工程（A0602）、电梯工程（A0604）、采暖（A0404）、样板房（A050502）、销售区域临时绿化（A050504）、检测费（A0506）、室内水电工程（A0601）、消防工程（A0602）、电梯工程（A0604）、采暖（A0404）、样板房（A050502）、销售区域临时绿化（A050504）、检测费（A0506）、室内水电工程（A0601）、消防工程（A0602）、电梯工程（A0604）、人防设备工程（A0606）科目的产品
人防设备工程（A0606）科目的产品（A0604）、人防设备工程（A0606）科目的产品、人防设备工程（A0606）科目的产品
人防设备工程（A0606）科目的产品（A0604）、人防设备工程（A0606）科目的产品、人防设备工程（A0606）科目的产品
人防设备工程（A0606）科目的产品（A0604）、人防设备工程（A0606）科目的产品`;

class CadAlert extends HTMLElement {
  static get observedAttributes() {
    return ['type', 'title', 'description', 'multiline', 'confirm-text', 'cancel-text', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback(name, oldVal, newVal) {
    if (oldVal !== newVal) this.render();
  }

  render() {
    let rawType = (this.getAttribute('type') || 'info').toLowerCase();
    // 兼容沙箱通用 primary/secondary/text 映射与中文名
    const typeMap = {
      'primary': 'info', 'default': 'info', '普通': 'info', 'info': 'info',
      'secondary': 'warning', '警告': 'warning', 'warning': 'warning',
      'success': 'success', '成功': 'success',
      'danger': 'danger', 'error': 'danger', 'text': 'danger', '危险': 'danger'
    };
    const alertType = typeMap[rawType] || 'info';
    const isMultiline = this.hasAttribute('multiline') && this.getAttribute('multiline') !== 'false';
    const isDraft = this.getAttribute('status') === 'draft';

    const titleText = this.getAttribute('title') || CAD_ALERT_DEFAULT_TITLES[alertType] || '普通消息';
    const defaultDesc = isMultiline ? CAD_ALERT_MULTILINE_DEFAULT : '这是一条消息通知';
    const descText = this.getAttribute('description') || (this.textContent && this.textContent.trim() ? this.textContent.trim() : defaultDesc);
    const confirmText = this.getAttribute('confirm-text') || '确定';
    const cancelText = this.getAttribute('cancel-text') || '取消';

    const iconSvg = CAD_ALERT_SVGS[alertType] || CAD_ALERT_SVGS.info;

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          position: relative;
          width: 360px;
          font-family: var(--cad-font-family, "Microsoft YaHei", "PingFang SC", sans-serif);
          box-sizing: border-box;
        }
        .sweetalert-card {
          width: 360px;
          min-height: ${isMultiline ? '546px' : '116px'};
          background: #FFFFFF;
          border-radius: 8px;
          box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.10);
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          box-sizing: border-box;
          position: relative;
          padding-bottom: ${isMultiline ? '6px' : '0px'};
        }
        .top-section {
          width: 360px;
          padding: 12px;
          box-sizing: border-box;
          display: flex;
          flex-direction: row;
          align-items: flex-start;
          gap: 10px;
          position: relative;
        }
        .frame-2 {
          width: 336px;
          display: flex;
          flex-direction: row;
          align-items: flex-start;
          gap: 4px;
        }
        .icon-wrapper {
          width: 20px;
          height: 20px;
          flex-shrink: 0;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .frame-1 {
          width: 312px;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .title-row {
          width: 312px;
          height: 20px;
          display: flex;
          align-items: center;
        }
        .title-text {
          font-size: 13px;
          line-height: 18px;
          font-weight: 700;
          color: #1F2329;
          margin: 0;
        }
        .desc-text {
          width: 312px;
          font-size: ${isMultiline ? '13px' : '12px'};
          line-height: ${isMultiline ? '22px' : '16px'};
          font-weight: 400;
          color: ${isMultiline ? '#666666' : '#8A8D91'};
          margin: 0;
          white-space: pre-wrap;
          word-break: break-all;
        }
        .close-btn {
          position: absolute;
          top: 14px;
          right: 12px;
          width: 16px;
          height: 16px;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          border-radius: 3px;
          transition: background 0.15s;
        }
        .close-btn:hover {
          background: rgba(0, 0, 0, 0.05);
        }
        .bottom-section {
          width: 360px;
          height: 48px;
          padding: 12px;
          box-sizing: border-box;
          display: flex;
          justify-content: flex-end;
          align-items: center;
        }
        .btn-group {
          display: flex;
          align-items: center;
          gap: 8px;
          height: 24px;
        }
        .btn {
          all: unset;
          box-sizing: border-box;
          width: 56px;
          height: 24px;
          padding: 2px 8px;
          border-radius: 4px;
          font-size: 12px;
          line-height: 16px;
          font-weight: 400;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          user-select: none;
          transition: background 0.15s, border-color 0.15s;
        }
        .btn-primary {
          background: #266EFF;
          color: #FFFFFF;
        }
        .btn-primary:hover {
          background: #4785FF;
        }
        .btn-secondary {
          background: #FFFFFF;
          color: #1F2329;
          border: 1px solid #E3E5E7;
        }
        .btn-secondary:hover {
          background: #F2F4F6;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="sweetalert-card">
        <div class="top-section">
          <div class="frame-2">
            <div class="icon-wrapper">${iconSvg}</div>
            <div class="frame-1">
              <div class="title-row">
                <span class="title-text">${titleText}</span>
              </div>
              <div class="desc-text">${descText}</div>
            </div>
          </div>
          <div class="close-btn" title="关闭">${CAD_ALERT_SVGS.close}</div>
        </div>
        <div class="bottom-section">
          <div class="btn-group">
            <button class="btn btn-primary" type="button">${confirmText}</button>
            <button class="btn btn-secondary" type="button">${cancelText}</button>
          </div>
        </div>
      </div>
      ${renderDraftBadge(isDraft)}
    `;

    this.shadowRoot.querySelector('.close-btn').onclick = () => {
      this.dispatchEvent(new CustomEvent('close', { bubbles: true, composed: true }));
    };
    this.shadowRoot.querySelector('.btn-primary').onclick = () => {
      this.dispatchEvent(new CustomEvent('confirm', { bubbles: true, composed: true }));
    };
    this.shadowRoot.querySelector('.btn-secondary').onclick = () => {
      this.dispatchEvent(new CustomEvent('cancel', { bubbles: true, composed: true }));
    };
  }
}
customElements.define('cad-alert', CadAlert);

/**
 * --------------------------------------------------------------------
 * 10. <cad-icon> 全局矢量图标组件 (映射自 Figma Page 252:3 图标 icon)
 * --------------------------------------------------------------------
 */
const CAD_ICON_PATHS = {
  edit: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M9.8 3.2L12.8 6.2M2.5 13.5H5.5L13 6C13.4 5.6 13.4 5 13 4.6L11.4 3C11 2.6 10.4 2.6 10 3L2.5 10.5V13.5Z" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  link: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M6.5 9.5L9.5 6.5M5.5 7.5L3.8 9.2C2.7 10.3 2.7 12 3.8 13.1C4.9 14.2 6.6 14.2 7.7 13.1L9.4 11.4M7.5 5.5L9.2 3.8C10.3 2.7 12 2.7 13.1 3.8C14.2 4.9 14.2 6.6 13.1 7.7L11.4 9.4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>`,
  help: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6.5" stroke="currentColor" stroke-width="1.1"/><path d="M6.5 6.3C6.5 5.4 7.2 4.8 8.1 4.8C8.9 4.8 9.6 5.4 9.6 6.2C9.6 6.9 9.1 7.3 8.5 7.7C8.1 8 8 8.3 8 8.9" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/><circle cx="8" cy="11.2" r="0.75" fill="currentColor"/></svg>`,
  close: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3.5 3.5L12.5 12.5M3.5 12.5L12.5 3.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>`,
  columns: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="2" y="2.5" width="12" height="11" rx="1" stroke="currentColor" stroke-width="1.2"/><line x1="6" y1="2.5" x2="6" y2="13.5" stroke="currentColor" stroke-width="1.2"/><line x1="10" y1="2.5" x2="10" y2="13.5" stroke="currentColor" stroke-width="1.2"/></svg>`,
  rows: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="2" y="2.5" width="12" height="11" rx="1" stroke="currentColor" stroke-width="1.2"/><line x1="2" y1="6.2" x2="14" y2="6.2" stroke="currentColor" stroke-width="1.2"/><line x1="2" y1="9.8" x2="14" y2="9.8" stroke="currentColor" stroke-width="1.2"/></svg>`,
  file_blank: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M4 2H9.5L12.5 5V13.5C12.5 13.8 12.3 14 12 14H4C3.7 14 3.5 13.8 3.5 13.5V2.5C3.5 2.2 3.7 2 4 2Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/><path d="M9.5 2V5H12.5" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/><line x1="5.5" y1="8" x2="10.5" y2="8" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/><line x1="5.5" y1="10.5" x2="10.5" y2="10.5" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/></svg>`,
  folder_import: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 4C2 3.45 2.45 3 3 3H6.2L7.7 4.5H13C13.55 4.5 14 4.95 14 5.5V12.5C14 13.05 13.55 13.5 13 13.5H3C2.45 13.5 2 13.05 2 12.5V4Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/><path d="M8 7V11M8 11L6.3 9.3M8 11L9.7 9.3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  data_extract: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="2" y="2.5" width="12" height="11" rx="1.5" stroke="currentColor" stroke-width="1.2"/><line x1="5" y1="10.5" x2="5" y2="7.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><line x1="8" y1="10.5" x2="8" y2="5.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><line x1="11" y1="10.5" x2="11" y2="8.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>`,
  zoom_fit: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2.5 5.5V3C2.5 2.7 2.7 2.5 3 2.5H5.5M10.5 2.5H13C13.3 2.5 13.5 2.7 13.5 3V5.5M13.5 10.5V13C13.5 13.3 13.3 13.5 13 13.5H10.5M5.5 13.5H3C2.7 13.5 2.5 13.3 2.5 13V10.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/><rect x="5.5" y="5.5" width="5" height="5" rx="0.5" stroke="currentColor" stroke-width="1.1"/></svg>`,
  zoom_1to1: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="7.2" cy="7.2" r="4.7" stroke="currentColor" stroke-width="1.2"/><path d="M10.8 10.8L13.5 13.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/><path d="M5.7 5.5V8.9M8.7 5.5V8.9M7.2 6.5V6.6M7.2 8.0V8.1" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>`,
  pick: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="4.5" stroke="currentColor" stroke-width="1.2"/><line x1="8" y1="1.5" x2="8" y2="4.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/><line x1="8" y1="11.5" x2="8" y2="14.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/><line x1="1.5" y1="8" x2="4.5" y2="8" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/><line x1="11.5" y1="8" x2="14.5" y2="8" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>`,
  folder: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 4.2C2 3.65 2.45 3.2 3 3.2H6.2L7.7 4.7H13C13.55 4.7 14 5.15 14 5.7V12.2C14 12.75 13.55 13.2 13 13.2H3C2.45 13.2 2 12.75 2 12.2V4.2Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>`
};

class CadIcon extends HTMLElement {
  static get observedAttributes() {
    return ['name', 'size', 'color'];
  }
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() { this.render(); }
  attributeChangedCallback(n, o, v) { if (o !== v) this.render(); }
  render() {
    const name = this.getAttribute('name') || 'edit';
    const size = this.getAttribute('size') || '16px';
    const color = this.getAttribute('color') || 'inherit';
    const svg = CAD_ICON_PATHS[name] || CAD_ICON_PATHS.edit;
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: ${size};
          height: ${size};
          color: ${color};
          vertical-align: middle;
          flex-shrink: 0;
        }
        svg { width: 100%; height: 100%; display: block; }
      </style>
      ${svg}
    `;
  }
}
customElements.define('cad-icon', CadIcon);

/**
 * --------------------------------------------------------------------
 * 11. <cad-divider> 分割线组件 (映射自 Figma Page 252:21 / Node 260:137)
 * --------------------------------------------------------------------
 */
class CadDivider extends HTMLElement {
  static get observedAttributes() {
    return ['direction', 'dashed', 'type'];
  }
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() { this.render(); }
  attributeChangedCallback(n, o, v) { if (o !== v) this.render(); }
  render() {
    const dir = this.getAttribute('direction') || 'horizontal';
    const dashed = this.hasAttribute('dashed') && this.getAttribute('dashed') !== 'false';
    const type = this.getAttribute('type') || 'divider'; // 'divider' (#EBECEE) | 'border' (#E4E5E7)
    const color = type === 'border' ? '#E4E5E7' : '#EBECEE';
    const style = dashed ? 'dashed' : 'solid';
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: ${dir === 'vertical' ? 'inline-block' : 'block'};
          width: ${dir === 'vertical' ? '1px' : '100%'};
          height: ${dir === 'vertical' ? '100%' : '1px'};
          margin: ${dir === 'vertical' ? '0 8px' : '6px 0'};
          border-top: ${dir === 'horizontal' ? `1px ${style} ${color}` : 'none'};
          border-left: ${dir === 'vertical' ? `1px ${style} ${color}` : 'none'};
          box-sizing: border-box;
        }
      </style>
    `;
  }
}
customElements.define('cad-divider', CadDivider);

/**
 * --------------------------------------------------------------------
 * 12. <cad-form-group> 表单无框分组组件 (映射自 Figma Page 252:35 Node 541:18087 & Page 843:3979 Node 2748:38502)
 *     默认态 (对话框内常规分组): 背景=false (透明无灰底), collapsible=false (无折叠箭头, 仅左侧 3×12px #266EFF 蓝条 + 12px 粗体标题)
 *     折叠面板态 (属性面板长列表): 可传 bg="true" collapsible="true" 开启灰底与右侧折叠箭头
 * --------------------------------------------------------------------
 */
class CadFormGroup extends HTMLElement {
  static get observedAttributes() {
    return ['title', 'bg', 'collapsible', 'collapsed', 'size'];
  }
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() { this.render(); }
  attributeChangedCallback(n, o, v) { if (o !== v) this.render(); }
  render() {
    const title = this.getAttribute('title') || '分组标题';
    const hasBg = this.getAttribute('bg') === 'true';
    const collapsible = this.getAttribute('collapsible') === 'true';
    const collapsed = collapsible && this.hasAttribute('collapsed') && this.getAttribute('collapsed') !== 'false';
    const size = this.getAttribute('size') || 'medium'; // 'medium' (24px) | 'large' (36px)
    const headerHeight = size === 'large' ? '36px' : '24px';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          width: 100%;
          font-family: var(--cad-font-family, "Microsoft YaHei", sans-serif);
          box-sizing: border-box;
        }
        .group-header {
          height: ${headerHeight};
          background: ${hasBg ? '#F6F7F9' : 'transparent'};
          border-radius: 4px;
          padding: ${hasBg ? '2px 8px 2px 6px' : '2px 4px 2px 0'};
          display: flex;
          align-items: center;
          gap: 6px;
          cursor: ${collapsible ? 'pointer' : 'default'};
          user-select: none;
          box-sizing: border-box;
        }
        .blue-bar {
          width: 3px;
          height: 12px;
          background: #266EFF;
          border-radius: 3px;
          flex-shrink: 0;
        }
        .title-wrap {
          flex: 1;
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 12px;
          line-height: 16px;
          font-weight: 700;
          color: #202327;
        }
        .chevron {
          width: 16px;
          height: 16px;
          display: ${collapsible ? 'flex' : 'none'};
          align-items: center;
          justify-content: center;
          transition: transform 0.15s;
          transform: rotate(${collapsed ? '-90deg' : '0deg'});
        }
        .group-body {
          display: ${collapsed ? 'none' : 'flex'};
          flex-direction: column;
          gap: 8px;
          padding: 6px 4px 4px 9px;
          box-sizing: border-box;
        }
      </style>
      <div class="group-header">
        <span class="blue-bar"></span>
        <div class="title-wrap">
          <span>${title}</span>
          <slot name="header-extra"></slot>
        </div>
        <span class="chevron">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M5 6.5L8 9.5L11 6.5" stroke="#606266" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </span>
      </div>
      <div class="group-body">
        <slot></slot>
      </div>
    `;

    if (collapsible) {
      this.shadowRoot.querySelector('.group-header').onclick = (e) => {
        // 若点击的是 slot 内的复选框等控件，不触发折叠
        if (e.target !== this.shadowRoot.querySelector('.group-header') && e.target.slot === 'header-extra') return;
        if (collapsed) this.removeAttribute('collapsed');
        else this.setAttribute('collapsed', '');
      };
    }
  }
}
customElements.define('cad-form-group', CadFormGroup);

/**
 * --------------------------------------------------------------------
 * 13. <cad-dialog> 模态对话框容器组件 (映射自 Figma Page 252:45 对话框 Modal Node 327:2318 / 611:61456)
 *     100% 遵循 Vela/Nova 规范：无左上角软件Logo，顶栏 36px (左 14px 粗体标题 + 12px 灰副标题，右 帮助? + 关闭×)，
 *     底栏 44px (右对齐 确定 #266EFF + 取消 #FFFFFF + 可选 帮助 #FFFFFF)
 * --------------------------------------------------------------------
 */
class CadDialog extends HTMLElement {
  static get observedAttributes() {
    return ['title', 'subtitle', 'width', 'confirm-text', 'cancel-text', 'help-text', 'show-help', 'show-footer-help'];
  }
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() { this.render(); }
  attributeChangedCallback(n, o, v) { if (o !== v) this.render(); }
  render() {
    const title = this.getAttribute('title') || '标题';
    const subtitle = this.getAttribute('subtitle') || '';
    const width = this.getAttribute('width') || '720px';
    const confirmText = this.getAttribute('confirm-text') || '确定';
    const cancelText = this.getAttribute('cancel-text') || '取消';
    const helpText = this.getAttribute('help-text') || '帮助';
    const showHelp = this.getAttribute('show-help') !== 'false';
    const showFooterHelp = this.getAttribute('show-footer-help') === 'true';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          width: ${width};
          font-family: var(--cad-font-family, "Microsoft YaHei", sans-serif);
          box-sizing: border-box;
        }
        .modal-shell {
          width: 100%;
          background: #FFFFFF;
          border: 1px solid #E4E5E7;
          border-radius: 8px;
          box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.10);
          display: flex;
          flex-direction: column;
          overflow: hidden;
          box-sizing: border-box;
        }
        .modal-header {
          height: 36px;
          padding: 10px 8px 10px 12px;
          border-bottom: 1px solid #EBECEE;
          display: flex;
          align-items: center;
          justify-content: space-between;
          box-sizing: border-box;
          background: #FFFFFF;
        }
        .header-left {
          display: flex;
          align-items: center;
          gap: 12px;
          min-width: 0;
        }
        .header-title {
          font-size: 14px;
          line-height: 20px;
          font-weight: 700;
          color: #202327;
          white-space: nowrap;
        }
        .header-subtitle {
          font-size: 12px;
          line-height: 16px;
          font-weight: 400;
          color: #8A8D91;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .header-actions {
          display: flex;
          align-items: center;
          gap: 2px;
        }
        .icon-btn {
          width: 24px;
          height: 24px;
          border-radius: 4px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #606266;
          cursor: pointer;
          transition: background 0.15s;
        }
        .icon-btn:hover {
          background: #F2F4F6;
          color: #202327;
        }
        .modal-body {
          padding: 12px;
          background: #FFFFFF;
          box-sizing: border-box;
          flex: 1;
        }
        .modal-footer {
          height: 44px;
          padding: 10px 12px 10px 12px;
          border-top: 1px solid #EBECEE;
          display: flex;
          align-items: center;
          justify-content: space-between;
          background: #FFFFFF;
          box-sizing: border-box;
        }
        .footer-left {
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .footer-right {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-left: auto;
        }
        .btn {
          all: unset;
          box-sizing: border-box;
          min-width: 56px;
          height: 24px;
          padding: 2px 10px;
          border-radius: 4px;
          font-size: 12px;
          line-height: 16px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          user-select: none;
          transition: background 0.15s;
        }
        .btn-primary {
          background: #266EFF;
          color: #FFFFFF;
        }
        .btn-primary:hover {
          background: #4785FF;
        }
        .btn-secondary {
          background: #FFFFFF;
          color: #202327;
          border: 1px solid #E4E5E7;
        }
        .btn-secondary:hover {
          background: #F2F4F6;
        }
      </style>
      <div class="modal-shell">
        <div class="modal-header">
          <div class="header-left">
            <span class="header-title">${title}</span>
            ${subtitle ? `<span class="header-subtitle">${subtitle}</span>` : ''}
          </div>
          <div class="header-actions">
            ${showHelp ? `<div class="icon-btn btn-help" title="帮助">${CAD_ICON_PATHS.help}</div>` : ''}
            <div class="icon-btn btn-close" title="关闭">${CAD_ICON_PATHS.close}</div>
          </div>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div class="modal-footer">
          <div class="footer-left">
            <slot name="footer-left"></slot>
          </div>
          <div class="footer-right">
            <button type="button" class="btn btn-primary">${confirmText}</button>
            <button type="button" class="btn btn-secondary btn-cancel">${cancelText}</button>
            ${showFooterHelp ? `<button type="button" class="btn btn-secondary btn-footer-help">${helpText}</button>` : ''}
          </div>
        </div>
      </div>
    `;

    const helpBtn = this.shadowRoot.querySelector('.btn-help');
    if (helpBtn) helpBtn.onclick = () => this.dispatchEvent(new CustomEvent('help', { bubbles: true, composed: true }));
    const footerHelpBtn = this.shadowRoot.querySelector('.btn-footer-help');
    if (footerHelpBtn) footerHelpBtn.onclick = () => this.dispatchEvent(new CustomEvent('help', { bubbles: true, composed: true }));
    this.shadowRoot.querySelector('.btn-close').onclick = () => this.dispatchEvent(new CustomEvent('close', { bubbles: true, composed: true }));
    this.shadowRoot.querySelector('.btn-primary').onclick = () => this.dispatchEvent(new CustomEvent('confirm', { bubbles: true, composed: true }));
    this.shadowRoot.querySelector('.btn-cancel').onclick = () => this.dispatchEvent(new CustomEvent('cancel', { bubbles: true, composed: true }));
  }
}
customElements.define('cad-dialog', CadDialog);

/**
 * --------------------------------------------------------------------
 * 14. <cad-table> 标准表格组件 (映射自 Figma Page 252:41 表格 Table Node 606:9099 / 606:8652 / 611:46865)
 *     100% 遵循 Vela/Nova 规范：表头 #F6F7F9 / 24px 行高，边框 #EBECEE，数据行 #FFFFFF (悬停 #F2F3F5 / 选中 #EBF3FF)
 *     支持单元层级结构 (Title 主标题行 / Header 列表头行 / Data 数据行 / Summary 汇总底行)、滚轮缩放与 3 大数据源模式
 * --------------------------------------------------------------------
 */
class CadTable extends HTMLElement {
  static get observedAttributes() {
    return [
      'cols', 'rows', 'col-width', 'row-height',
      'show-title', 'show-header', 'show-summary',
      'title-text', 'mode', 'zoom', 'row1-style', 'row2-style', 'row-other-style', 'empty'
    ];
  }
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() {
    this.render();
  }
  attributeChangedCallback(n, o, v) {
    if (o !== v) this.render();
  }
  render() {
    const isEmpty = this.hasAttribute('empty') && this.getAttribute('empty') !== 'false';
    const cols = Math.max(1, Math.min(10, parseInt(this.getAttribute('cols') || '4', 10)));
    const rows = Math.max(1, Math.min(15, parseInt(this.getAttribute('rows') || '5', 10)));
    const colWidthVal = parseFloat(this.getAttribute('col-width') || '50.0');
    const rowHeightVal = parseFloat(this.getAttribute('row-height') || '8.0');
    const zoom = Math.max(50, Math.min(180, parseInt(this.getAttribute('zoom') || '100', 10)));
    const mode = this.getAttribute('mode') || 'blank'; // 'blank' | 'import' | 'extract'

    // 兼容旧版属性与新版结构化布尔属性
    const hasLegacy = this.hasAttribute('row1-style') || this.hasAttribute('row2-style');
    const showTitle = hasLegacy
      ? (this.getAttribute('row1-style') === '标题')
      : (this.getAttribute('show-title') !== 'false');
    const showHeader = hasLegacy
      ? (this.getAttribute('row2-style') === '表头')
      : (this.getAttribute('show-header') !== 'false');
    const showSummary = this.getAttribute('show-summary') === 'true';
    const titleText = this.getAttribute('title-text') || (
      mode === 'import' ? '工程材料 BOM 清单 (Excel 导入)' :
      mode === 'extract' ? '图面图块属性统计表 (数据提取)' : '主 标 题'
    );

    // 针对三种模式生成示例表头与单元格内容
    const importHeaders = ['序号', '构件编码', '材料名称', '规格型号', '单位', '数量', '备注', '单价'];
    const importRows = [
      ['01', 'C-101', 'HRB400螺纹钢', 'Φ22mm', 't', '14.5', '主梁配筋', '4120'],
      ['02', 'C-102', '商品混凝土', 'C35抗渗P6', 'm³', '128.0', '地下室底板', '460'],
      ['03', 'M-201', '断桥铝合金窗', '1800×1500', '樘', '36', 'Low-E中空', '1380'],
      ['04', 'M-202', '防火钢质门', 'FM甲1221', '樘', '12', '疏散楼梯间', '1650'],
      ['05', 'P-301', '热镀锌钢管', 'DN100', 'm', '240.0', '消防立管', '85']
    ];
    const extractHeaders = ['图块名称', '图层 (Layer)', '构件类别', '标高', '统计数量', '长度(mm)', '面积(m²)', '状态'];
    const extractRows = [
      ['ZW_DOOR_SINGLE', 'A-DOOR', '单扇平开门', '±0.000', '24', '900', '1.89', '已校验'],
      ['ZW_WIN_STD', 'A-GLAZ', '标准推拉窗', '+3.200', '48', '1500', '2.25', '已校验'],
      ['ZW_COL_RECT', 'S-COLS', '矩形钢筋砼柱', '±0.000', '32', '600', '0.36', '已校验'],
      ['ZW_BEAM_MAIN', 'S-BEAM', '框架主梁 KL1', '+3.200', '64', '7200', '1.80', '已校验'],
      ['ZW_EQUIP_PUMP', 'M-PUMP', '离心水泵机组', '-4.500', '4', '1200', '1.44', '已校验']
    ];

    let rowsHtml = '';
    if (!isEmpty) {
      // 顶部列标尺 (A, B, C, D...)
      let colLetters = `<th class="idx-corner">#</th>`;
      for (let c = 0; c < cols; c++) {
        const letter = String.fromCharCode(65 + c);
        colLetters += `<th class="col-ruler">${letter} <span class="ruler-dim">(${colWidthVal.toFixed(0)})</span></th>`;
      }
      rowsHtml += `<tr class="row-ruler">${colLetters}</tr>`;

      let rowIdx = 1;
      // 1. 主标题行 (Title)
      if (showTitle) {
        rowsHtml += `
          <tr class="row-title">
            <td class="idx-cell">${rowIdx++}</td>
            <td colspan="${cols}" class="title-cell">${titleText}</td>
          </tr>
        `;
      }

      // 2. 列表头行 (Header)
      if (showHeader) {
        let hCells = `<td class="idx-cell">${rowIdx++}</td>`;
        for (let c = 0; c < cols; c++) {
          const hText = mode === 'import' ? (importHeaders[c] || `列 ${c+1}`) :
                        mode === 'extract' ? (extractHeaders[c] || `属性 ${c+1}`) : `表头 ${c+1}`;
          hCells += `<td>${hText}</td>`;
        }
        rowsHtml += `<tr class="row-header">${hCells}</tr>`;
      }

      // 3. 数据行 (Data)
      for (let r = 0; r < rows; r++) {
        const cls = r === 0 ? 'row-data selected' : 'row-data';
        let dCells = `<td class="idx-cell">${rowIdx++}</td>`;
        for (let c = 0; c < cols; c++) {
          const dText = mode === 'import' ? (importRows[r % importRows.length][c] || '—') :
                        mode === 'extract' ? (extractRows[r % extractRows.length][c] || '—') : '数据';
          dCells += `<td>${dText}</td>`;
        }
        rowsHtml += `<tr class="${cls}">${dCells}</tr>`;
      }

      // 4. 汇总底行 (Summary)
      if (showSummary) {
        let sCells = `<td class="idx-cell">${rowIdx++}</td>`;
        sCells += `<td class="summary-label">汇总</td>`;
        for (let c = 1; c < cols; c++) {
          const sVal = c === cols - 1
            ? (mode === 'import' ? '∑ 220.5' : mode === 'extract' ? '∑ 172 项' : `∑ ${rows} 行`)
            : '—';
          sCells += `<td class="summary-val">${sVal}</td>`;
        }
        rowsHtml += `<tr class="row-summary">${sCells}</tr>`;
      }
    }

    const cellHeight = Math.max(20, Math.min(34, Math.round(rowHeightVal * 2.8)));
    const scaleVal = (zoom / 100).toFixed(2);

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          width: 100%;
          font-family: var(--cad-font-family, "Microsoft YaHei", sans-serif);
          box-sizing: border-box;
        }
        .table-viewport {
          width: 100%;
          min-height: 246px;
          max-height: 266px;
          border: 1px solid #EBECEE;
          border-radius: 4px;
          overflow: auto;
          background: #F6F7F9;
          padding: 10px;
          box-sizing: border-box;
          display: flex;
          align-items: flex-start;
          justify-content: center;
          position: relative;
        }
        .zoom-stage {
          width: 100%;
          transform: scale(${scaleVal});
          transform-origin: top center;
          transition: transform 0.12s ease-out;
        }
        .table-wrap {
          width: 100%;
          border: 1px solid #E4E5E7;
          border-radius: 4px;
          overflow: hidden;
          background: #FFFFFF;
          box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
        }
        table {
          width: 100%;
          border-collapse: collapse;
          font-size: 12px;
          line-height: 16px;
          color: #202327;
        }
        th, td {
          height: ${cellHeight}px;
          padding: 0 6px;
          border-right: 1px solid #EBECEE;
          border-bottom: 1px solid #EBECEE;
          box-sizing: border-box;
          text-align: center;
          white-space: nowrap;
        }
        th:last-child, td:last-child {
          border-right: none;
        }
        tr:last-child td {
          border-bottom: none;
        }
        tr.row-ruler th {
          height: 20px;
          background: #F2F3F5;
          color: #8A8D91;
          font-size: 11px;
          font-weight: 500;
        }
        .ruler-dim {
          font-size: 10px;
          color: #A6A9AD;
          font-weight: 400;
        }
        .idx-corner, .idx-cell {
          width: 26px;
          min-width: 26px;
          max-width: 26px;
          background: #F6F7F9 !important;
          color: #8A8D91 !important;
          font-size: 11px;
          font-weight: 400 !important;
          user-select: none;
        }
        tr.row-title td.title-cell {
          height: 28px;
          background: #F6F7F9;
          font-weight: 700;
          font-size: 13px;
          color: #202327;
          letter-spacing: 1px;
        }
        tr.row-header td {
          height: 24px;
          background: #F6F7F9;
          font-weight: 600;
          color: #202327;
        }
        tr.row-data td {
          background: #FFFFFF;
          color: #202327;
        }
        tr.row-data:hover td {
          background: #F2F3F5;
        }
        tr.row-data.selected td {
          background: #EBF3FF;
          color: #266EFF;
        }
        tr.row-summary td {
          height: 24px;
          background: #F6F7F9;
          font-weight: 600;
          color: #202327;
          border-top: 1px solid #E4E5E7;
        }
        tr.row-summary td.summary-val {
          color: #266EFF;
        }
        .empty-box {
          height: 210px;
          width: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #A6A9AD;
          font-size: 12px;
          background: #FFFFFF;
          border-radius: 4px;
        }
      </style>
      <div class="table-viewport" title="支持鼠标滚轮缩放预览 (50% ~ 180%)">
        ${isEmpty
          ? `<div class="empty-box">暂无预览数据 (已关闭预览)</div>`
          : `<div class="zoom-stage"><div class="table-wrap"><table><tbody>${rowsHtml}</tbody></table></div></div>`
        }
      </div>
    `;

    const vp = this.shadowRoot.querySelector('.table-viewport');
    if (vp) {
      vp.addEventListener('wheel', (e) => {
        e.preventDefault();
        const delta = e.deltaY < 0 ? 10 : -10;
        const nextZoom = Math.max(50, Math.min(180, zoom + delta));
        if (nextZoom !== zoom) {
          this.setAttribute('zoom', String(nextZoom));
          this.dispatchEvent(new CustomEvent('zoom-change', { detail: { zoom: nextZoom }, bubbles: true, composed: true }));
        }
      }, { passive: false });
    }
  }
}
customElements.define('cad-table', CadTable);

/**
 * --------------------------------------------------------------------
 * 15. <cad-tabs> 标签页/视图切换组件 (映射自 Figma Page 252:37 标签页 Tabs Node 801:10827 视图 & 589:8495 标签页)
 *     100% 遵循 Vela/Nova 规范：
 *     - type="segmented" (Node 801:10827 视图): 外框 #F2F3F5 圆角 4px 内边距 2px；选中项 #FFFFFF 圆角 3px + #266EFF 高亮字/图标
 *     - type="line" (Node 589:8495 标签页): 底边 1px #EBECEE，选中项 #266EFF + 底部 2px #266EFF 指示条
 * --------------------------------------------------------------------
 */
class CadTabs extends HTMLElement {
  static get observedAttributes() {
    return ['value', 'type', 'items'];
  }
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() { this.render(); }
  attributeChangedCallback(n, o, v) { if (o !== v) this.render(); }
  get value() { return this.getAttribute('value') || ''; }
  set value(val) { this.setAttribute('value', val); }
  render() {
    const type = this.getAttribute('type') || 'segmented'; // 'segmented' | 'line'
    let items = [];
    try {
      items = JSON.parse(this.getAttribute('items') || '[]');
    } catch (e) {
      items = [];
    }
    const activeVal = this.getAttribute('value') || (items[0] ? items[0].value : '');

    const tabsHtml = items.map((item, idx) => {
      const isSelected = item.value === activeVal;
      const iconHtml = item.icon && CAD_ICON_PATHS[item.icon]
        ? `<span class="tab-icon">${CAD_ICON_PATHS[item.icon]}</span>`
        : '';
      const badgeHtml = item.badge
        ? `<span class="tab-badge">${item.badge}</span>`
        : '';
      const showSep = type === 'segmented' && !isSelected && idx > 0 && items[idx - 1].value !== activeVal;
      return `
        ${showSep ? `<span class="seg-sep"></span>` : ''}
        <button type="button" class="tab-item ${isSelected ? 'selected' : ''}" data-val="${item.value}">
          ${iconHtml}
          <span class="tab-label">${item.label}</span>
          ${badgeHtml}
        </button>
      `;
    }).join('');

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          width: 100%;
          font-family: var(--cad-font-family, "Microsoft YaHei", sans-serif);
          box-sizing: border-box;
        }
        .tabs-nav.segmented {
          display: flex;
          align-items: center;
          height: 30px;
          background: #F2F3F5;
          border-radius: 4px;
          padding: 3px;
          gap: 2px;
          box-sizing: border-box;
        }
        .tabs-nav.segmented .tab-item {
          all: unset;
          flex: 1;
          height: 24px;
          border-radius: 3px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: 6px;
          font-size: 12px;
          line-height: 16px;
          color: #606266;
          cursor: pointer;
          user-select: none;
          transition: background 0.15s, color 0.15s, box-shadow 0.15s;
          box-sizing: border-box;
          padding: 0 10px;
        }
        .tabs-nav.segmented .tab-item:hover:not(.selected) {
          background: #EBECEE;
          color: #202327;
        }
        .tabs-nav.segmented .tab-item.selected {
          background: #FFFFFF;
          color: #266EFF;
          font-weight: 600;
          box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
        }
        .seg-sep {
          width: 1px;
          height: 14px;
          background: #E4E5E7;
          flex-shrink: 0;
        }
        .tabs-nav.line {
          display: flex;
          align-items: center;
          height: 32px;
          border-bottom: 1px solid #EBECEE;
          gap: 24px;
          padding: 0 4px;
          box-sizing: border-box;
        }
        .tabs-nav.line .tab-item {
          all: unset;
          height: 32px;
          display: inline-flex;
          align-items: center;
          gap: 6px;
          font-size: 12px;
          color: #606266;
          cursor: pointer;
          position: relative;
          box-sizing: border-box;
        }
        .tabs-nav.line .tab-item.selected {
          color: #266EFF;
          font-weight: 600;
        }
        .tabs-nav.line .tab-item.selected::after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          height: 2px;
          background: #266EFF;
          border-radius: 1px;
        }
        .tab-icon {
          width: 15px;
          height: 15px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
        }
        .tab-icon svg {
          width: 100%;
          height: 100%;
        }
        .tab-badge {
          font-size: 10px;
          line-height: 14px;
          padding: 0 5px;
          border-radius: 2px;
          background: #EBF3FF;
          color: #266EFF;
          font-weight: 400;
        }
      </style>
      <div class="tabs-nav ${type}">
        ${tabsHtml}
      </div>
    `;

    this.shadowRoot.querySelectorAll('.tab-item').forEach(btn => {
      btn.onclick = () => {
        const val = btn.getAttribute('data-val');
        if (val && val !== activeVal) {
          this.setAttribute('value', val);
          this.dispatchEvent(new CustomEvent('change', { detail: { value: val }, bubbles: true, composed: true }));
        }
      };
    });
  }
}
customElements.define('cad-tabs', CadTabs);

/**
 * --------------------------------------------------------------------
 * 16. <cad-tag> 标准标签组件 (映射自 Figma Page 6906:18142 标签 Tag Node 6906:19794)
 *     100% 遵循 Vela/Nova 规范：Light/Dark 主题，灰 (#EBECEE/#606266)、蓝 (#EBF3FF/#266EFF)、橙 (#FFF7E8/#F98A00)、红 (#FFECE8/#EF4A4A)
 * --------------------------------------------------------------------
 */
class CadTag extends HTMLElement {
  static get observedAttributes() {
    return ['color', 'theme', 'size'];
  }
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() { this.render(); }
  attributeChangedCallback(n, o, v) { if (o !== v) this.render(); }
  render() {
    const color = this.getAttribute('color') || 'blue'; // 'grey' | 'blue' | 'orange' | 'red'
    const theme = this.getAttribute('theme') || 'light'; // 'light' | 'dark'
    const size = this.getAttribute('size') || '24'; // '24' | '20'
    const height = size === '20' ? '20px' : '24px';

    const palette = {
      grey:   { lightBg: '#EBECEE', lightFg: '#606266', darkBg: '#E4E5E7', darkFg: '#202327' },
      blue:   { lightBg: '#EBF3FF', lightFg: '#266EFF', darkBg: '#266EFF', darkFg: '#FFFFFF' },
      orange: { lightBg: '#FFF7E8', lightFg: '#F98A00', darkBg: '#F98A00', darkFg: '#FFFFFF' },
      red:    { lightBg: '#FFECE8', lightFg: '#EF4A4A', darkBg: '#EF4A4A', darkFg: '#FFFFFF' }
    };
    const p = palette[color] || palette.blue;
    const bg = theme === 'dark' ? p.darkBg : p.lightBg;
    const fg = theme === 'dark' ? p.darkFg : p.lightFg;

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          vertical-align: middle;
        }
        .tag-box {
          height: ${height};
          padding: 0 8px;
          background: ${bg};
          color: ${fg};
          border-radius: 3px;
          font-family: var(--cad-font-family, "Microsoft YaHei", sans-serif);
          font-size: 12px;
          line-height: 16px;
          font-weight: 500;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: 4px;
          white-space: nowrap;
          box-sizing: border-box;
        }
      </style>
      <span class="tag-box"><slot></slot></span>
    `;
  }
}
customElements.define('cad-tag', CadTag);

/**
 * --------------------------------------------------------------------
 * 17. <cad-file-loader> 官方载入文件组件 (映射自 Figma Page 6451:56655 载入文件 File Loader Node 6451:56656)
 *     100% 遵循 Vela/Nova 规范：左侧 24px 输入框/选择器 (圆角 4,0,0,4) + 右侧 24×24px 载入图标按钮 (圆角 0,4,4,0)
 * --------------------------------------------------------------------
 */
class CadFileLoader extends HTMLElement {
  static get observedAttributes() {
    return ['value', 'placeholder', 'disabled'];
  }
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() { this.render(); }
  attributeChangedCallback(n, o, v) { if (o !== v) this.render(); }
  get value() { return this.getAttribute('value') || ''; }
  set value(val) { this.setAttribute('value', val); }
  render() {
    const val = this.getAttribute('value') || '';
    const placeholder = this.getAttribute('placeholder') || '选择或载入本地表格文件 (.xlsx / .csv)';
    const disabled = this.hasAttribute('disabled');

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          width: 100%;
          font-family: var(--cad-font-family, "Microsoft YaHei", sans-serif);
          box-sizing: border-box;
        }
        .loader-wrap {
          display: flex;
          align-items: center;
          width: 100%;
          height: 24px;
          box-sizing: border-box;
        }
        .loader-input {
          flex: 1;
          height: 24px;
          padding: 0 8px;
          font-size: 12px;
          color: ${disabled ? '#A6A9AD' : '#202327'};
          background: ${disabled ? '#F2F3F5' : '#FFFFFF'};
          border: 1px solid #E4E5E7;
          border-right: none;
          border-radius: 4px 0 0 4px;
          outline: none;
          box-sizing: border-box;
          min-width: 0;
        }
        .loader-input::placeholder {
          color: #A6A9AD;
        }
        .loader-btn {
          width: 24px;
          height: 24px;
          background: ${disabled ? '#F2F3F5' : '#FFFFFF'};
          border: 1px solid #E4E5E7;
          border-radius: 0 4px 4px 0;
          display: flex;
          align-items: center;
          justify-content: center;
          color: ${disabled ? '#A6A9AD' : '#606266'};
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          box-sizing: border-box;
          flex-shrink: 0;
          transition: background 0.15s, color 0.15s;
        }
        .loader-btn:hover:not(.disabled) {
          background: #F2F3F5;
          color: #266EFF;
        }
      </style>
      <div class="loader-wrap">
        <input class="loader-input" type="text" value="${val}" placeholder="${placeholder}" readonly ${disabled ? 'disabled' : ''} />
        <button type="button" class="loader-btn ${disabled ? 'disabled' : ''}" title="载入本地文件">
          ${CAD_ICON_PATHS.folder}
        </button>
      </div>
    `;

    const btn = this.shadowRoot.querySelector('.loader-btn');
    if (btn && !disabled) {
      btn.onclick = () => {
        this.dispatchEvent(new CustomEvent('load-file', { bubbles: true, composed: true }));
      };
    }
  }
}
customElements.define('cad-file-loader', CadFileLoader);

/**
 * --------------------------------------------------------------------
 * 18. <cad-picker> 官方图面拾取组件 (映射自 Figma Page 252:36 拾取 Picker Node 6451:56183)
 *     100% 遵循 Vela/Nova 规范：左侧 24px 坐标/尺寸回显框 + 右侧 24×24px 十字拾取按钮
 * --------------------------------------------------------------------
 */
class CadPicker extends HTMLElement {
  static get observedAttributes() {
    return ['value', 'placeholder', 'disabled'];
  }
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() { this.render(); }
  attributeChangedCallback(n, o, v) { if (o !== v) this.render(); }
  render() {
    const val = this.getAttribute('value') || '';
    const placeholder = this.getAttribute('placeholder') || '在图面拾取坐标点';
    const disabled = this.hasAttribute('disabled');

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          width: 100%;
          font-family: var(--cad-font-family, "Microsoft YaHei", sans-serif);
          box-sizing: border-box;
        }
        .picker-wrap {
          display: flex;
          align-items: center;
          width: 100%;
          height: 24px;
          box-sizing: border-box;
        }
        .picker-input {
          flex: 1;
          height: 24px;
          padding: 0 8px;
          font-size: 12px;
          color: ${disabled ? '#A6A9AD' : '#202327'};
          background: ${disabled ? '#F2F3F5' : '#FFFFFF'};
          border: 1px solid #E4E5E7;
          border-right: none;
          border-radius: 4px 0 0 4px;
          outline: none;
          box-sizing: border-box;
          min-width: 0;
        }
        .picker-btn {
          width: 24px;
          height: 24px;
          background: ${disabled ? '#F2F3F5' : '#FFFFFF'};
          border: 1px solid #E4E5E7;
          border-radius: 0 4px 4px 0;
          display: flex;
          align-items: center;
          justify-content: center;
          color: ${disabled ? '#A6A9AD' : '#266EFF'};
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          box-sizing: border-box;
          flex-shrink: 0;
          transition: background 0.15s;
        }
        .picker-btn:hover:not(.disabled) {
          background: #EBF3FF;
        }
      </style>
      <div class="picker-wrap">
        <input class="picker-input" type="text" value="${val}" placeholder="${placeholder}" ${disabled ? 'disabled' : ''} />
        <button type="button" class="picker-btn ${disabled ? 'disabled' : ''}" title="图面拾取">
          ${CAD_ICON_PATHS.pick}
        </button>
      </div>
    `;

    const btn = this.shadowRoot.querySelector('.picker-btn');
    if (btn && !disabled) {
      btn.onclick = () => {
        this.dispatchEvent(new CustomEvent('pick', { bubbles: true, composed: true }));
      };
    }
  }
}
customElements.define('cad-picker', CadPicker);

/**
 * --------------------------------------------------------------------
 * 19. <cad-banner> 官方内嵌警告提示条 (映射自 Figma Page 6921:42395 警告提示 Alert Node 6921:42396)
 *     100% 遵循 Vela/Nova 规范：信息 #EBF3FF / 默认 #F6F7F9 / 成功 #E8FFEA / 警告 #FFF7E8，圆角 4px
 * --------------------------------------------------------------------
 */
class CadBanner extends HTMLElement {
  static get observedAttributes() {
    return ['type'];
  }
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() { this.render(); }
  attributeChangedCallback(n, o, v) { if (o !== v) this.render(); }
  render() {
    const type = this.getAttribute('type') || 'info'; // 'default' | 'info' | 'success' | 'warning'
    const bgMap = {
      default: '#F6F7F9',
      info: '#EBF3FF',
      success: '#E8FFEA',
      warning: '#FFF7E8'
    };
    const iconSvg = type === 'warning' ? CAD_ALERT_SVGS.warning :
                    type === 'success' ? CAD_ALERT_SVGS.success : CAD_ALERT_SVGS.info;

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          width: 100%;
          font-family: var(--cad-font-family, "Microsoft YaHei", sans-serif);
          box-sizing: border-box;
        }
        .banner {
          width: 100%;
          min-height: 28px;
          padding: 5px 8px;
          background: ${bgMap[type] || bgMap.info};
          border-radius: 4px;
          display: flex;
          align-items: center;
          gap: 6px;
          box-sizing: border-box;
          font-size: 12px;
          line-height: 16px;
          color: #606266;
        }
        .icon {
          width: 16px;
          height: 16px;
          flex-shrink: 0;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .icon svg {
          width: 15px;
          height: 15px;
        }
      </style>
      <div class="banner">
        <span class="icon">${iconSvg}</span>
        <span><slot></slot></span>
      </div>
    `;
  }
}
customElements.define('cad-banner', CadBanner);

console.log("%c[Nova CAD/BIM]%c Web Components 核心库已装载 (已内嵌 49 类组件清册，支持 file:// 离线直开)", "background:#266EFF;color:#fff;padding:2px 6px;border-radius:3px;", "");
