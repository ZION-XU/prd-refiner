/**
 * ====================================================================
 * Nova CAD/BIM Web Components 核心库 (cad-components.js)
 * 资产来源: Figma 53 Pages BIM 标准组件库 (49+ 核心全景对齐)
 * 架构分级: L1 官方标准 + L2 业务场景 + L3 PM草稿补齐
 * 运行方式: 原生 Web Components (Custom Elements + Shadow DOM) 零依赖
 * 编译器: Nova Incremental Component Compiler v2.0 (具备舱壁熔断隔离)
 * ====================================================================
 */

// 1. 全局自定义元素安全注册守卫（防止重复注册抛错）
if (typeof window !== 'undefined' && window.customElements) {
  const _origDefine = customElements.define.bind(customElements);
  customElements.define = function(name, constructor, options) {
    if (customElements.get(name)) {
      return; // 已经注册，安全跳过
    }
    return _origDefine(name, constructor, options);
  };
}

// 2. 嵌入全景资产清单 (支持 file:// 协议直接双击打开页面，无 CORS 限制)
if (typeof window !== 'undefined') {
  window.NOVA_MANIFEST = {
  "project": "Nova CAD/BIM Design System",
  "source_file_key": "mtY1cdLoClLSdbo1noAryL",
  "last_synced": "2026-10-30 10:04:59",
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
      "updated_at": "2026-10-30 10:04:58"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:58"
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
      "updated_at": "2026-10-30 10:04:58"
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
      "updated_at": "2026-10-30 10:04:58"
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
      "updated_at": "2026-10-30 10:04:58"
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
      "updated_at": "2026-10-30 10:04:58"
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
      "updated_at": "2026-10-30 10:04:58"
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
      "updated_at": "2026-10-30 10:04:58"
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
      "updated_at": "2026-10-30 10:04:58"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:58"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
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
      "updated_at": "2026-10-30 10:04:59"
    }
  },
  "prototypes_audit": {
    "table_create_prototype.html": {
      "audited_at": "2026-10-30 09:26:51",
      "file_name": "table_create_prototype.html",
      "total_interactive_elements": 50,
      "official_components_count": 50,
      "draft_components_count": 0,
      "raw_elements_count": 0,
      "coverage_rate": "100.0%",
      "official_rate": "100.0%",
      "draft_rate": "0.0%",
      "breakdown": {
        "official": [
          "cad-tabs",
          "cad-dialog",
          "cad-form-group",
          "cad-select",
          "cad-button",
          "cad-icon",
          "cad-tabs",
          "cad-form-group",
          "cad-radio",
          "cad-radio",
          "cad-divider",
          "cad-form-group",
          "cad-input",
          "cad-input",
          "cad-input",
          "cad-input",
          "cad-banner",
          "cad-form-group",
          "cad-file-loader",
          "cad-button",
          "cad-select",
          "cad-divider",
          "cad-form-group",
          "cad-radio",
          "cad-radio",
          "cad-input",
          "cad-divider",
          "cad-form-group",
          "cad-checkbox",
          "cad-checkbox",
          "cad-divider",
          "cad-form-group",
          "cad-button",
          "cad-icon",
          "cad-button",
          "cad-icon",
          "cad-dialog",
          "cad-form-group",
          "cad-radio",
          "cad-radio",
          "cad-radio",
          "cad-divider",
          "cad-form-group",
          "cad-select",
          "cad-input",
          "cad-form-group",
          "cad-input",
          "cad-dialog",
          "cad-button",
          "cad-alert"
        ],
        "draft": [],
        "raw": []
      }
    }
  }
};
}

// 3. 通用草稿徽章渲染辅助
function renderDraftBadge(isDraft, tooltip = "PM草稿组件 (待补充 Figma)") {
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

const CAD_ALERT_DEFAULT_TITLES = {
  info: '普通信息',
  success: '成功通知',
  warning: '警告通知',
  error: '危险通知',
  danger: '危险通知'
};

const CAD_ALERT_MULTILINE_DEFAULT = '这是一条重要的多行系统通知与反馈说明。';

const CAD_ALERT_SVGS = {
  info: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M9.93652 1.31348C14.769 1.31348 18.6865 5.23098 18.6865 10.0635C18.6865 14.896 14.769 18.8135 9.93652 18.8135C5.10403 18.8135 1.18652 14.896 1.18652 10.0635C1.18652 5.23098 5.10403 1.31348 9.93652 1.31348Z" fill="#266EFF"/><path d="M9.93652 8.36209C10.3392 8.36209 10.6657 8.68855 10.6657 9.09125V14.1954C10.6657 14.5981 10.3392 14.9246 9.93652 14.9246C9.53382 14.9246 9.20736 14.5981 9.20736 14.1954V9.09125C9.20736 8.68855 9.53382 8.36209 9.93652 8.36209ZM9.93652 5.20237C10.4735 5.20237 10.9087 5.63764 10.9087 6.17459C10.9087 6.71153 10.4735 7.14681 9.93652 7.14681C9.39958 7.14681 8.9643 6.71153 8.9643 6.17459C8.9643 5.63764 9.39958 5.20237 9.93652 5.20237Z" fill="#FFFFFF"/></svg>`,
  success: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M9.93774 1.31226C14.7702 1.31226 18.6877 5.22976 18.6877 10.0623C18.6877 14.8947 14.7702 18.8123 9.93774 18.8123C5.10525 18.8123 1.18774 14.8947 1.18774 10.0623C1.18774 5.22976 5.10525 1.31226 9.93774 1.31226Z" fill="#00B42A"/><path d="M13.9543 7.35913C13.6696 7.07447 13.2078 7.07441 12.9231 7.35913L8.45337 11.8269L6.5647 9.93726L6.46313 9.85229C6.17902 9.65571 5.78647 9.68435 5.53345 9.93726C5.24869 10.222 5.24869 10.6837 5.53345 10.9685L7.9397 13.3748L8.04028 13.4587C8.32433 13.6555 8.71684 13.6275 8.96997 13.3748L13.9543 8.39038L14.0393 8.28979C14.2362 8.00561 14.2075 7.61225 13.9543 7.35913Z" fill="#FFFFFF"/></svg>`,
  warning: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M9.93652 1.31348C14.769 1.31348 18.6865 5.23098 18.6865 10.0635C18.6865 14.896 14.769 18.8135 9.93652 18.8135C5.10403 18.8135 1.18652 14.896 1.18652 10.0635C1.18652 5.23098 5.10403 1.31348 9.93652 1.31348Z" fill="#F98A00"/><path d="M9.93652 12.9801C10.4735 12.9801 10.9087 13.4154 10.9087 13.9524C10.9087 14.4893 10.4735 14.9246 9.93652 14.9246C9.39958 14.9246 8.9643 14.4893 8.9643 13.9524C8.9643 13.4154 9.93652 12.9801 9.93652 12.9801ZM9.93652 5.20237C10.3392 5.20237 10.6657 5.52882 10.6657 5.93153V11.0357C10.6657 11.4384 10.3392 11.7649 9.93652 11.7649C9.53382 11.7649 9.20736 11.4384 9.20736 11.0357V5.93153C9.20736 5.52882 9.53382 5.20237 9.93652 5.20237Z" fill="#FFFFFF"/></svg>`,
  error: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 1.25C14.8325 1.25 18.75 5.16751 18.75 10C18.75 14.8325 14.8325 18.75 10 18.75C5.16751 18.75 1.25 14.8325 1.25 10C1.25 5.16751 5.16751 1.25 10 1.25Z" fill="#EF4A4A"/><path d="M6.56767 6.56775C6.28291 6.85251 6.28291 7.31419 6.56767 7.59895L8.97376 10.0049L6.53487 12.4462C6.28338 12.7326 6.29431 13.169 6.56767 13.4424C6.85244 13.7271 7.31411 13.7271 7.59888 13.4424L10.0048 11.0362L12.4461 13.4753C12.7325 13.7268 13.169 13.7157 13.4424 13.4424C13.7271 13.1576 13.7271 12.696 13.4424 12.4112L11.0361 10.0049L13.4751 7.56395C13.7266 7.27754 13.7157 6.84111 13.4424 6.56775C13.1576 6.28299 12.6959 6.28299 12.4111 6.56775L10.0048 8.97384L7.56387 6.53495L7.52731 6.50487C7.24137 6.28481 6.82965 6.30578 6.56767 6.56775Z" fill="#FFFFFF"/></svg>`,
  danger: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 1.25C14.8325 1.25 18.75 5.16751 18.75 10C18.75 14.8325 14.8325 18.75 10 18.75C5.16751 18.75 1.25 14.8325 1.25 10C1.25 5.16751 5.16751 1.25 10 1.25Z" fill="#EF4A4A"/><path d="M6.56767 6.56775C6.28291 6.85251 6.28291 7.31419 6.56767 7.59895L8.97376 10.0049L6.53487 12.4462C6.28338 12.7326 6.29431 13.169 6.56767 13.4424C6.85244 13.7271 7.31411 13.7271 7.59888 13.4424L10.0048 11.0362L12.4461 13.4753C12.7325 13.7268 13.169 13.7157 13.4424 13.4424C13.7271 13.1576 13.7271 12.696 13.4424 12.4112L11.0361 10.0049L13.4751 7.56395C13.7266 7.27754 13.7157 6.84111 13.4424 6.56775C13.1576 6.28299 12.6959 6.28299 12.4111 6.56775L10.0048 8.97384L7.56387 6.53495L7.52731 6.50487C7.24137 6.28481 6.82965 6.30578 6.56767 6.56775Z" fill="#FFFFFF"/></svg>`,
  close: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3.5 3.5L12.5 12.5M3.5 12.5L12.5 3.5" stroke="#606266" stroke-width="1.3" stroke-linecap="round"/></svg>`
};

if (typeof window !== 'undefined') {
  window.renderDraftBadge = renderDraftBadge;
  window.COMMON_DRAFT_STYLE = COMMON_DRAFT_STYLE;
  window.CAD_ICON_PATHS = CAD_ICON_PATHS;
  window.CAD_ALERT_SVGS = CAD_ALERT_SVGS;
  window.CAD_ALERT_DEFAULT_TITLES = CAD_ALERT_DEFAULT_TITLES;
  window.CAD_ALERT_MULTILINE_DEFAULT = CAD_ALERT_MULTILINE_DEFAULT;
}


// ====================================================================
// Component: <cad-banner> (Key: alert_banner)
// ====================================================================
try {
  (function() {
class CadBanner extends HTMLElement {
  static get observedAttributes() {
    return ['type', 'title', 'closable'];
  }
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() { this.render(); }
  attributeChangedCallback(n, o, v) { if (o !== v) this.render(); }
  render() {
    const type = this.getAttribute('type') || 'info'; // 'default' | 'info' | 'success' | 'warning' | 'danger'
    const title = this.getAttribute('title') || '';
    const closable = this.hasAttribute('closable');

    const bgMap = {
      default: '#F6F7F9',
      info: '#EBF3FF',
      success: '#E8FFEA',
      warning: '#FFF7E8',
      danger: '#FFF1F0'
    };
    const iconSvg = type === 'warning' ? CAD_ALERT_SVGS.warning :
                    type === 'success' ? CAD_ALERT_SVGS.success :
                    type === 'danger' ? CAD_ALERT_SVGS.error : CAD_ALERT_SVGS.info;

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
          padding: 6px 10px;
          background: ${bgMap[type] || bgMap.info};
          border: 1px solid rgba(0,0,0,0.06);
          border-radius: 4px;
          display: flex;
          align-items: flex-start;
          gap: 8px;
          box-sizing: border-box;
          font-size: 12px;
          line-height: 16px;
          color: #303133;
        }
        .icon {
          width: 16px;
          height: 16px;
          flex-shrink: 0;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-top: 1px;
        }
        .icon svg {
          width: 15px;
          height: 15px;
        }
        .body-wrap {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 2px;
        }
        .title {
          font-weight: 600;
          color: #1F2329;
          font-size: 12px;
        }
        .desc {
          color: #606266;
          font-size: 11.5px;
        }
        .close-btn {
          cursor: pointer;
          color: #8A8D91;
          padding: 0 2px;
          font-size: 14px;
          line-height: 14px;
          margin-left: auto;
          transition: color 0.15s;
        }
        .close-btn:hover {
          color: #1F2329;
        }
      </style>
      <div class="banner">
        <span class="icon">${iconSvg}</span>
        <div class="body-wrap">
          ${title ? `<span class="title">${title}</span>` : ''}
          <span class="desc"><slot></slot></span>
        </div>
        ${closable ? `<span class="close-btn" title="关闭">×</span>` : ''}
      </div>
    `;

    const closeEl = this.shadowRoot.querySelector('.close-btn');
    if (closeEl) {
      closeEl.onclick = () => {
        this.style.display = 'none';
        this.dispatchEvent(new CustomEvent('close', { bubbles: true, composed: true }));
      };
    }
  }
}
customElements.define('cad-banner', CadBanner);
    if (typeof window !== 'undefined') window.CadBanner = CadBanner;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-banner> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-axis-grid> (Key: axis_grid)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-axis-grid> 建筑轴网生成定义器 (映射自 Figma AxisGrid Page 253:58)
 * --------------------------------------------------------------------
 */
class CadAxisGrid extends HTMLElement {
  static get observedAttributes() {
    return ['status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const isDraft = this.getAttribute('status') === 'draft';
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: flex;
          gap: 12px;
          padding: 8px;
          background: #F8F9FA;
          border: 1px solid #D0D3D6;
          border-radius: 4px;
          box-sizing: border-box;
          font-size: 12px;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div>开间 (X向): <cad-input size="small" value="4200" suffix-label="mm" style="width:80px;"></cad-input></div>
      <div>进深 (Y向): <cad-input size="small" value="6000" suffix-label="mm" style="width:80px;"></cad-input></div>
      <cad-button size="small" type="primary">正交生成轴网</cad-button>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-axis-grid', CadAxisGrid);

    if (typeof window !== 'undefined') window.CadAxisGrid = CadAxisGrid;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-axis-grid> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-button> (Key: button)
// ====================================================================
try {
  (function() {
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
    const type = this.getAttribute('type') || 'secondary'; // 'primary' | 'secondary' | 'text' | 'danger'
    const size = this.getAttribute('size') || 'small';      // 'mini' (20px) | 'small' (24px) | 'large' (32px)
    const disabled = this.hasAttribute('disabled');
    const isDraft = this.getAttribute('status') === 'draft';

    let height = 'var(--cad-height-small, 24px)';
    let padding = 'var(--cad-padding-small, 2px 8px)';
    let fontSize = 'var(--cad-font-size-base, 12px)';

    if (size === 'large') {
      height = 'var(--cad-height-large, 32px)';
      padding = 'var(--cad-padding-large, 4px 12px)';
      fontSize = '13px';
    } else if (size === 'mini') {
      height = 'var(--cad-height-mini, 20px)';
      padding = '1px 6px';
      fontSize = '11px';
    }

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
    } else if (type === 'danger') {
      bg = disabled ? '#FFA39E' : 'var(--cad-color-danger, #F5222D)';
      color = 'var(--cad-color-text-white, #FFFFFF)';
      border = '1px solid transparent';
      hoverBg = '#FF4D4F';
      activeBg = '#CF1322';
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
          font-size: ${fontSize};
          font-family: var(--cad-font-family, sans-serif);
          font-weight: 500;
          color: ${color};
          background: ${bg};
          border: ${border};
          border-radius: var(--cad-radius-base, 4px);
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          user-select: none;
          transition: background 0.15s, border-color 0.15s, color 0.15s;
          white-space: nowrap;
        }
        button:hover:not([disabled]) {
          background: ${hoverBg};
        }
        button:active:not([disabled]) {
          background: ${activeBg};
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <button type="button" ${disabled ? 'disabled' : ''}>
        <slot></slot>
      </button>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-button', CadButton);
    if (typeof window !== 'undefined') window.CadButton = CadButton;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-button> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-checkbox> (Key: checkbox)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadCheckbox = CadCheckbox;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-checkbox> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-color-picker> (Key: color_picker)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-color-picker> CAD 颜色选择器 (映射自 Figma ColorPicker Page 252:53)
 * --------------------------------------------------------------------
 */
class CadColorPicker extends HTMLElement {
  static get observedAttributes() {
    return ['value', 'disabled', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  get value() {
    return this.getAttribute('value') || 'ByLayer';
  }

  set value(v) {
    this.setAttribute('value', v);
  }

  render() {
    const val = this.getAttribute('value') || 'ByLayer';
    const disabled = this.hasAttribute('disabled');
    const isDraft = this.getAttribute('status') === 'draft';

    const colorMap = {
      'ByLayer': '#FFFFFF',
      'ByBlock': '#FFFFFF',
      'Red': '#FF0000',
      'Yellow': '#FFFF00',
      'Green': '#00FF00',
      'Cyan': '#00FFFF',
      'Blue': '#0000FF',
      'Magenta': '#FF00FF',
      'White': '#FFFFFF'
    };
    const swatchColor = colorMap[val] || (val.startsWith('#') ? val : '#1F2329');

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          align-items: center;
          position: relative;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
          height: var(--cad-height-small, 24px);
        }
        .picker-box {
          display: flex;
          align-items: center;
          gap: 6px;
          height: 100%;
          padding: 2px 6px;
          background: var(--cad-color-bg-white, #FFFFFF);
          border: 1px solid var(--cad-color-border-default, #D0D3D6);
          border-radius: var(--cad-border-radius-base, 4px);
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          opacity: ${disabled ? '0.6' : '1'};
          user-select: none;
        }
        .swatch {
          width: 14px;
          height: 14px;
          border-radius: 2px;
          background: ${swatchColor};
          border: 1px solid rgba(0,0,0,0.2);
          flex-shrink: 0;
        }
        .color-label {
          color: var(--cad-color-text-main, #1F2329);
          min-width: 50px;
        }
        .arrow {
          font-size: 9px;
          color: #8F959E;
        }
        select {
          position: absolute;
          left: 0;
          top: 0;
          width: 100%;
          height: 100%;
          opacity: 0;
          cursor: pointer;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="picker-box">
        <span class="swatch"></span>
        <span class="color-label">${val}</span>
        <span class="arrow">▼</span>
      </div>
      <select ${disabled ? 'disabled' : ''}>
        <option value="ByLayer" ${val==='ByLayer'?'selected':''}>随层 ByLayer</option>
        <option value="ByBlock" ${val==='ByBlock'?'selected':''}>随块 ByBlock</option>
        <option value="Red" ${val==='Red'?'selected':''}>红 1 (Red)</option>
        <option value="Yellow" ${val==='Yellow'?'selected':''}>黄 2 (Yellow)</option>
        <option value="Green" ${val==='Green'?'selected':''}>绿 3 (Green)</option>
        <option value="Cyan" ${val==='Cyan'?'selected':''}>青 4 (Cyan)</option>
        <option value="Blue" ${val==='Blue'?'selected':''}>蓝 5 (Blue)</option>
        <option value="Magenta" ${val==='Magenta'?'selected':''}>洋红 6 (Magenta)</option>
        <option value="White" ${val==='White'?'selected':''}>白 7 (White)</option>
      </select>
      ${renderDraftBadge(isDraft)}
    `;

    this.shadowRoot.querySelector('select').addEventListener('change', (e) => {
      this.setAttribute('value', e.target.value);
      this.dispatchEvent(new CustomEvent('change', { detail: { value: e.target.value } }));
    });
  }
}
customElements.define('cad-color-picker', CadColorPicker);

    if (typeof window !== 'undefined') window.CadColorPicker = CadColorPicker;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-color-picker> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-command-tool> (Key: command_tool)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-command-tool> CAD 命令行输入栏 (映射自 Figma CommandTool Page 7823:839)
 * --------------------------------------------------------------------
 */
class CadCommandTool extends HTMLElement {
  static get observedAttributes() {
    return ['prompt', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const prompt = this.getAttribute('prompt') || '命令:';
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: flex;
          flex-direction: column;
          width: 100%;
          background: #1E1F22;
          color: #D3D5D9;
          border: 1px solid #363B42;
          border-radius: 4px;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Consolas", monospace);
          font-size: 12px;
          padding: 4px 6px;
        }
        .history {
          color: #8F959E;
          line-height: 1.4;
          max-height: 36px;
          overflow: hidden;
        }
        .prompt-line {
          display: flex;
          align-items: center;
          gap: 6px;
          margin-top: 2px;
        }
        .prompt-label {
          color: #266EFF;
          font-weight: bold;
        }
        input {
          flex: 1;
          background: transparent;
          border: none;
          outline: none;
          color: #FFFFFF;
          font-family: inherit;
          font-size: 12px;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="history">正在初始化图形数据库... 完成。<br>输入 TABLE 进入创建表格向导。</div>
      <div class="prompt-line">
        <span class="prompt-label">${prompt}</span>
        <input type="text" placeholder="输入命令或按回车重复上次操作">
      </div>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-command-tool', CadCommandTool);

    if (typeof window !== 'undefined') window.CadCommandTool = CadCommandTool;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-command-tool> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-composite-input> (Key: composite_input)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-composite-input> 单选+图片+输入复合参数行 (映射自 Figma 253:56)
 * --------------------------------------------------------------------
 */
class CadCompositeInput extends HTMLElement {
  static get observedAttributes() {
    return ['label', 'value', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const label = this.getAttribute('label') || '复合参数';
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: flex;
          align-items: center;
          gap: 8px;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: 12px;
        }
        .label {
          width: 80px;
          color: #646A73;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <span class="label">${label}</span>
      <cad-radio name="comp_radio" checked>模式A</cad-radio>
      <cad-input size="small" style="width: 100px;"></cad-input>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-composite-input', CadCompositeInput);

    if (typeof window !== 'undefined') window.CadCompositeInput = CadCompositeInput;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-composite-input> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-divider> (Key: divider)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadDivider = CadDivider;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-divider> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-door-tool> (Key: door_tool)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-door-tool> 门窗构件翻转设置卡 (映射自 Figma DoorTool Page 253:59)
 * --------------------------------------------------------------------
 */
class CadDoorTool extends HTMLElement {
  static get observedAttributes() {
    return ['status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const isDraft = this.getAttribute('status') === 'draft';
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          padding: 4px 8px;
          background: #FFFFFF;
          border: 1px solid #D0D3D6;
          border-radius: 4px;
          box-sizing: border-box;
          font-size: 12px;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <span>🚪 门开向:</span>
      <cad-button size="small">内/外翻转 🔄</cad-button>
      <cad-button size="small">左/右翻转 ↔️</cad-button>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-door-tool', CadDoorTool);

    if (typeof window !== 'undefined') window.CadDoorTool = CadDoorTool;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-door-tool> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-dropdown> (Key: dropdown)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-dropdown> 下拉菜单容器 (映射自 Figma Dropdown Page 252:12)
 * --------------------------------------------------------------------
 */
class CadDropdown extends HTMLElement {
  static get observedAttributes() {
    return ['title', 'disabled', 'placement', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.isOpen = false;
    this._onDocClick = this._onDocClick.bind(this);
  }

  connectedCallback() {
    this.render();
    document.addEventListener('click', this._onDocClick);
  }

  disconnectedCallback() {
    document.removeEventListener('click', this._onDocClick);
  }

  _onDocClick(e) {
    if (!this.contains(e.target)) {
      if (this.isOpen) {
        this.isOpen = false;
        this.updatePopupState();
      }
    }
  }

  attributeChangedCallback() {
    this.render();
  }

  toggle() {
    if (this.hasAttribute('disabled')) return;
    this.isOpen = !this.isOpen;
    this.updatePopupState();
  }

  updatePopupState() {
    const popup = this.shadowRoot.querySelector('.dropdown-popup');
    if (popup) {
      popup.style.display = this.isOpen ? 'block' : 'none';
    }
  }

  render() {
    const title = this.getAttribute('title') || '下拉操作';
    const disabled = this.hasAttribute('disabled');
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          position: relative;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
        }
        .trigger-btn {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          height: var(--cad-height-small, 24px);
          padding: 2px 8px;
          background: var(--cad-color-bg-white, #FFFFFF);
          border: 1px solid var(--cad-color-border-default, #D0D3D6);
          border-radius: var(--cad-border-radius-base, 4px);
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          opacity: ${disabled ? '0.6' : '1'};
          color: var(--cad-color-text-main, #1F2329);
          user-select: none;
        }
        .trigger-btn:hover {
          border-color: ${disabled ? 'var(--cad-color-border-default, #D0D3D6)' : 'var(--cad-color-primary, #266EFF)'};
        }
        .arrow {
          font-size: 10px;
          transition: transform 0.2s;
        }
        .dropdown-popup {
          display: ${this.isOpen ? 'block' : 'none'};
          position: absolute;
          top: calc(100% + 4px);
          left: 0;
          z-index: 1000;
          background: #FFFFFF;
          border: 1px solid var(--cad-color-border-default, #D0D3D6);
          border-radius: 4px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          min-width: 120px;
          padding: 4px 0;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="trigger-btn">
        <slot name="trigger">
          <span>${title}</span>
          <span class="arrow">▼</span>
        </slot>
      </div>
      <div class="dropdown-popup">
        <slot></slot>
      </div>
      ${renderDraftBadge(isDraft)}
    `;

    this.shadowRoot.querySelector('.trigger-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggle();
    });
  }
}
customElements.define('cad-dropdown', CadDropdown);

    if (typeof window !== 'undefined') window.CadDropdown = CadDropdown;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-dropdown> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-family-mgr> (Key: family_mgr)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-family-mgr> 族库管理选择面板 (映射自 Figma FamilyMgr Page 253:57)
 * --------------------------------------------------------------------
 */
class CadFamilyMgr extends HTMLElement {
  static get observedAttributes() {
    return ['status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const isDraft = this.getAttribute('status') === 'draft';
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          padding: 8px;
          background: #FFFFFF;
          border: 1px solid #D0D3D6;
          border-radius: 4px;
          box-sizing: border-box;
          font-size: 12px;
        }
        .bar {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 6px;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="bar">
        <b>BIM 族库分类</b>
        <cad-button size="small" type="primary">载入族...</cad-button>
      </div>
      <cad-tree></cad-tree>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-family-mgr', CadFamilyMgr);

    if (typeof window !== 'undefined') window.CadFamilyMgr = CadFamilyMgr;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-family-mgr> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-file-loader> (Key: file_loader)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadFileLoader = CadFileLoader;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-file-loader> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-file-picker-input> (Key: file_picker_input)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadFilePickerInput = CadFilePickerInput;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-file-picker-input> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-filter> (Key: filter)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-filter> 多条件属性筛选条 (映射自 Figma Filter Page 7477:26492)
 * --------------------------------------------------------------------
 */
class CadFilter extends HTMLElement {
  static get observedAttributes() {
    return ['placeholder', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const placeholder = this.getAttribute('placeholder') || '过滤构件特性或图层...';
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          width: 100%;
          height: var(--cad-height-small, 24px);
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
        }
        .filter-box {
          flex: 1;
          display: flex;
          align-items: center;
          gap: 4px;
          height: 100%;
          padding: 2px 6px;
          background: #FFFFFF;
          border: 1px solid var(--cad-color-border-default, #D0D3D6);
          border-radius: var(--cad-border-radius-base, 4px);
        }
        input {
          border: none;
          outline: none;
          background: transparent;
          width: 100%;
          font-size: 12px;
          color: #1F2329;
        }
        .filter-icon {
          font-size: 11px;
          color: #8F959E;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="filter-box">
        <span class="filter-icon">🔍</span>
        <input type="text" placeholder="${placeholder}">
      </div>
      <slot name="extra"></slot>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-filter', CadFilter);

    if (typeof window !== 'undefined') window.CadFilter = CadFilter;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-filter> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-form> (Key: form)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-form> 表单根容器 (映射自 Figma Form Page 252:35)
 * --------------------------------------------------------------------
 */
class CadForm extends HTMLElement {
  static get observedAttributes() {
    return ['layout', 'label-width', 'disabled', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const layout = this.getAttribute('layout') || 'horizontal'; // 'horizontal' | 'vertical' | 'inline'
    const labelWidth = this.getAttribute('label-width') || '80px';
    const disabled = this.hasAttribute('disabled');
    const isDraft = this.getAttribute('status') === 'draft';

    let displayMode = 'flex';
    let flexDirection = layout === 'vertical' ? 'column' : 'column';
    let gap = '8px';

    if (layout === 'inline') {
      flexDirection = 'row';
      gap = '12px';
    }

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          position: relative;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
          --cad-form-label-width: ${labelWidth};
        }
        form {
          display: ${displayMode};
          flex-direction: ${flexDirection};
          gap: ${gap};
          width: 100%;
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <form onsubmit="return false;">
        <slot></slot>
      </form>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-form', CadForm);

    if (typeof window !== 'undefined') window.CadForm = CadForm;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-form> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-form-group> (Key: form_group)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadFormGroup = CadFormGroup;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-form-group> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-icon> (Key: icon)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadIcon = CadIcon;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-icon> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-input> (Key: input)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadInput = CadInput;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-input> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-link> (Key: link)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-link> 超链接组件 (映射自 Figma Link Page 252:5)
 * --------------------------------------------------------------------
 */
class CadLink extends HTMLElement {
  static get observedAttributes() {
    return ['href', 'target', 'disabled', 'underline', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const href = this.getAttribute('href') || 'javascript:void(0)';
    const target = this.getAttribute('target') || '_self';
    const disabled = this.hasAttribute('disabled');
    const underline = this.getAttribute('underline') || 'hover'; // 'always' | 'hover' | 'none'
    const isDraft = this.getAttribute('status') === 'draft';

    let textDecoration = 'none';
    if (underline === 'always') textDecoration = 'underline';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          position: relative;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
        }
        a {
          color: ${disabled ? 'var(--cad-color-text-disabled, #A4ABB5)' : 'var(--cad-color-primary, #266EFF)'};
          text-decoration: ${textDecoration};
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          transition: color 0.15s ease;
          display: inline-flex;
          align-items: center;
          gap: 4px;
        }
        a:hover {
          color: ${disabled ? 'var(--cad-color-text-disabled, #A4ABB5)' : 'var(--cad-color-primary-hover, #4B88FF)'};
          text-decoration: ${underline !== 'none' && !disabled ? 'underline' : textDecoration};
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <a href="${disabled ? 'javascript:void(0)' : href}" target="${target}">
        <slot></slot>
      </a>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-link', CadLink);

    if (typeof window !== 'undefined') window.CadLink = CadLink;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-link> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-main-toolbar> (Key: main_toolbar)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-main-toolbar> CAD 绘图修改主工具栏 (映射自 Figma MainToolbar Page 7930:2104)
 * --------------------------------------------------------------------
 */
class CadMainToolbar extends HTMLElement {
  static get observedAttributes() {
    return ['direction', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const dir = this.getAttribute('direction') || 'horizontal';
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          flex-direction: ${dir === 'vertical' ? 'column' : 'row'};
          gap: 2px;
          padding: 3px;
          background: #F2F3F5;
          border: 1px solid #D0D3D6;
          border-radius: 4px;
          box-sizing: border-box;
        }
        .btn {
          width: 24px;
          height: 24px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 3px;
          cursor: pointer;
          font-size: 12px;
        }
        .btn:hover {
          background: #E5E7EB;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="btn" title="直线 (L)">📏</div>
      <div class="btn" title="圆 (C)">⭕</div>
      <div class="btn" title="矩形 (REC)">⬜</div>
      <div class="btn" title="偏移 (O)">➿</div>
      <div class="btn" title="修剪 (TR)">✂️</div>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-main-toolbar', CadMainToolbar);

    if (typeof window !== 'undefined') window.CadMainToolbar = CadMainToolbar;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-main-toolbar> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-material-select> (Key: material_select)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-material-select> BIM 材质选择器 (映射自 Figma MaterialSelect Page 252:54)
 * --------------------------------------------------------------------
 */
class CadMaterialSelect extends HTMLElement {
  static get observedAttributes() {
    return ['value', 'disabled', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const val = this.getAttribute('value') || 'C30 混凝土';
    const disabled = this.hasAttribute('disabled');
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          align-items: center;
          position: relative;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
          height: var(--cad-height-small, 24px);
          min-width: 140px;
        }
        .box {
          display: flex;
          align-items: center;
          gap: 6px;
          height: 100%;
          width: 100%;
          padding: 2px 8px;
          background: var(--cad-color-bg-white, #FFFFFF);
          border: 1px solid var(--cad-color-border-default, #D0D3D6);
          border-radius: var(--cad-border-radius-base, 4px);
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          opacity: ${disabled ? '0.6' : '1'};
          user-select: none;
        }
        .texture-preview {
          width: 14px;
          height: 14px;
          border-radius: 2px;
          background: #A0A5AA;
          background-image: repeating-linear-gradient(45deg, #888E94 25%, transparent 25%, transparent 75%, #888E94 75%, #888E94), repeating-linear-gradient(45deg, #888E94 25%, #A0A5AA 25%, #A0A5AA 75%, #888E94 75%, #888E94);
          background-position: 0 0, 4px 4px;
          background-size: 8px 8px;
          border: 1px solid rgba(0,0,0,0.2);
          flex-shrink: 0;
        }
        .mat-name {
          flex: 1;
          color: var(--cad-color-text-main, #1F2329);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        select {
          position: absolute;
          left: 0;
          top: 0;
          width: 100%;
          height: 100%;
          opacity: 0;
          cursor: pointer;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="box">
        <span class="texture-preview"></span>
        <span class="mat-name">${val}</span>
        <span style="font-size: 9px; color: #8F959E;">▼</span>
      </div>
      <select ${disabled ? 'disabled' : ''}>
        <option value="C30 混凝土" ${val==='C30 混凝土'?'selected':''}>C30 混凝土</option>
        <option value="HRB400 螺纹钢筋" ${val==='HRB400 螺纹钢筋'?'selected':''}>HRB400 螺纹钢筋</option>
        <option value="加气混凝土砌块" ${val==='加气混凝土砌块'?'selected':''}>加气混凝土砌块</option>
        <option value="普通平板中空玻璃 6+12A+6" ${val==='普通平板中空玻璃 6+12A+6'?'selected':''}>普通平板中空玻璃 6+12A+6</option>
        <option value="结构铝合金 6063-T5" ${val==='结构铝合金 6063-T5'?'selected':''}>结构铝合金 6063-T5</option>
      </select>
      ${renderDraftBadge(isDraft)}
    `;

    this.shadowRoot.querySelector('select').addEventListener('change', (e) => {
      this.setAttribute('value', e.target.value);
      this.dispatchEvent(new CustomEvent('change', { detail: { value: e.target.value } }));
    });
  }
}
customElements.define('cad-material-select', CadMaterialSelect);

    if (typeof window !== 'undefined') window.CadMaterialSelect = CadMaterialSelect;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-material-select> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-menu> (Key: menu)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-menu> 级联/上下文菜单组件 (映射自 Figma Menu Page 252:8)
 * --------------------------------------------------------------------
 */
class CadMenu extends HTMLElement {
  static get observedAttributes() {
    return ['open', 'trigger', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const isDraft = this.getAttribute('status') === 'draft';
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          position: relative;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
        }
        .menu-list {
          min-width: 140px;
          background: var(--cad-color-bg-white, #FFFFFF);
          border: 1px solid var(--cad-color-border-default, #D0D3D6);
          border-radius: var(--cad-border-radius-base, 4px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          padding: 4px 0;
          margin: 0;
          list-style: none;
          box-sizing: border-box;
        }
        ::slotted(cad-menu-item), ::slotted(div.menu-item) {
          padding: 6px 12px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          cursor: pointer;
          color: var(--cad-color-text-main, #1F2329);
          transition: background 0.15s ease;
        }
        ::slotted(cad-menu-item:hover), ::slotted(div.menu-item:hover) {
          background: var(--cad-color-bg-hover, #F2F3F5);
          color: var(--cad-color-primary, #266EFF);
        }
        ::slotted(cad-divider), ::slotted(hr) {
          margin: 4px 0;
          border: none;
          border-top: 1px solid var(--cad-color-border-divider, #E5E6EB);
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="menu-list">
        <slot></slot>
      </div>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-menu', CadMenu);

    if (typeof window !== 'undefined') window.CadMenu = CadMenu;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-menu> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-message> (Key: message)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-message> 全局轻提示 Toast (映射自 Figma Message Page 252:43)
 * --------------------------------------------------------------------
 */
class CadMessage extends HTMLElement {
  static get observedAttributes() {
    return ['type', 'duration', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  static show(text, type = 'info', duration = 3000) {
    let container = document.getElementById('cad-message-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'cad-message-container';
      container.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);z-index:9999;display:flex;flex-direction:column;gap:8px;pointer-events:none;';
      document.body.appendChild(container);
    }
    const msg = document.createElement('cad-message');
    msg.setAttribute('type', type);
    msg.innerText = text;
    msg.style.pointerEvents = 'auto';
    container.appendChild(msg);

    setTimeout(() => {
      msg.style.opacity = '0';
      msg.style.transition = 'opacity 0.3s, transform 0.3s';
      msg.style.transform = 'translateY(-10px)';
      setTimeout(() => msg.remove(), 300);
    }, duration);
  }

  static success(text, duration) { CadMessage.show(text, 'success', duration); }
  static warning(text, duration) { CadMessage.show(text, 'warning', duration); }
  static error(text, duration) { CadMessage.show(text, 'error', duration); }
  static info(text, duration) { CadMessage.show(text, 'info', duration); }

  render() {
    const type = this.getAttribute('type') || 'info'; // 'info' | 'success' | 'warning' | 'error'
    const isDraft = this.getAttribute('status') === 'draft';

    const colors = {
      info: { bg: '#EBF4FF', border: '#BAD9FF', text: '#266EFF' },
      success: { bg: '#E8FFEA', border: '#AFF0B5', text: '#00B42A' },
      warning: { bg: '#FFF7E8', border: '#FFDCA3', text: '#FF7D00' },
      error: { bg: '#FFECE8', border: '#FFC5BC', text: '#F53F3F' }
    };
    const c = colors[type] || colors.info;
    const iconSvg = CAD_ALERT_SVGS[type] || CAD_ALERT_SVGS.info;

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          position: relative;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
        }
        .toast {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 6px 14px;
          background: #FFFFFF;
          border: 1px solid ${c.border};
          border-radius: 4px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.12);
          color: var(--cad-color-text-main, #1F2329);
        }
        .icon {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 16px;
          height: 16px;
          flex-shrink: 0;
        }
        .icon svg {
          width: 16px;
          height: 16px;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="toast">
        <span class="icon">${iconSvg}</span>
        <span><slot></slot></span>
      </div>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-message', CadMessage);
window.CadMessage = CadMessage;

    if (typeof window !== 'undefined') window.CadMessage = CadMessage;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-message> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-dialog> (Key: modal)
// ====================================================================
try {
  (function() {
class CadDialog extends HTMLElement {
  static get observedAttributes() {
    return ['title', 'subtitle', 'size', 'width', 'height', 'confirm-text', 'cancel-text', 'help-text', 'show-help', 'show-footer-help'];
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
    const confirmText = this.getAttribute('confirm-text') || '确定';
    const cancelText = this.getAttribute('cancel-text') || '取消';
    const helpText = this.getAttribute('help-text') || '帮助';
    const showHelp = this.getAttribute('show-help') !== 'false';
    const showFooterHelp = this.getAttribute('show-footer-help') === 'true';

    // 100% 对齐 Figma Page 252:45 对话框官方尺寸规格 (AutoLayout: VERTICAL FIXED x FIXED)
    const FIGMA_SIZES = {
      '480x240': { w: '480px', h: '240px' },
      '480x360': { w: '480px', h: '360px' },
      '600x360': { w: '600px', h: '360px' },
      '720x600': { w: '720px', h: '600px' },
      '840x600': { w: '840px', h: '600px' },
      '960x600': { w: '960px', h: '600px' },
      '920x600': { w: '960px', h: '600px' }
    };

    const sizeAttr = this.getAttribute('size');
    let width = this.getAttribute('width');
    let height = this.getAttribute('height');

    if (sizeAttr && FIGMA_SIZES[sizeAttr]) {
      width = FIGMA_SIZES[sizeAttr].w;
      height = FIGMA_SIZES[sizeAttr].h;
    } else {
      width = width || '720px';
      height = height || 'auto';
    }

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          width: ${width};
          ${height !== 'auto' ? `height: ${height};` : ''}
          font-family: var(--cad-font-family, "Microsoft YaHei", sans-serif);
          box-sizing: border-box;
        }
        .modal-shell {
          width: 100%;
          height: 100%;
          background: #FFFFFF;
          border: 1px solid var(--cad-color-border-default, #E4E5E7);
          border-radius: 8px;
          box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.20);
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
          flex-shrink: 0;
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
          min-height: 0;
          overflow: auto;
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
          flex-shrink: 0;
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
    if (typeof window !== 'undefined') window.CadDialog = CadDialog;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-dialog> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-options-dialog> (Key: options_dialog)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-options-dialog> CAD 系统选项配置面板 (映射自 Figma OptionsDialog Page 843:3979)
 * --------------------------------------------------------------------
 */
class CadOptionsDialog extends HTMLElement {
  static get observedAttributes() {
    return ['open', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const isDraft = this.getAttribute('status') === 'draft';
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <cad-dialog title="选项 (Options)" size="840x600">
        <cad-tabs>
          <div data-tab="文件与系统">文件路径与系统支持搜索路径设定</div>
          <div data-tab="显示">窗口元素、颜色主题与十字光标大小</div>
          <div data-tab="打开和保存">文件保存类型 DWG 2018、自动保存时间间隔</div>
          <div data-tab="用户系统配置">右键单击自定义、线宽设置</div>
        </cad-tabs>
      </cad-dialog>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-options-dialog', CadOptionsDialog);

    if (typeof window !== 'undefined') window.CadOptionsDialog = CadOptionsDialog;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-options-dialog> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-panel> (Key: panel)
// ====================================================================
try {
  (function() {
class CadPanel extends HTMLElement {
  static get observedAttributes() {
    return ['title', 'width', 'dock', 'collapsed', 'collapsible', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const title = this.getAttribute('title') || '面板';
    const width = this.getAttribute('width') || '260px';
    const dock = this.getAttribute('dock'); // 'left' | 'right' | null
    const isCollapsed = this.hasAttribute('collapsed');
    const collapsible = this.hasAttribute('collapsible');
    const isDraft = this.getAttribute('status') === 'draft';

    const dockBorder = dock === 'left' ? 'border-right: 1px solid var(--cad-color-border-default, #D0D3D6);' :
                       dock === 'right' ? 'border-left: 1px solid var(--cad-color-border-default, #D0D3D6);' :
                       'border: 1px solid var(--cad-color-border-default, #D0D3D6); border-radius: 4px;';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          position: relative;
          width: ${width};
          background: var(--cad-color-bg-white, #FFFFFF);
          ${dockBorder}
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Microsoft YaHei", sans-serif);
          font-size: 12px;
          overflow: hidden;
        }
        .header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          height: 28px;
          padding: 0 8px;
          background: var(--cad-color-bg-light, #F8FAFC);
          border-bottom: 1px solid var(--cad-color-border-default, #E3E5E7);
          user-select: none;
          font-weight: 600;
          color: var(--cad-color-text-main, #1F2329);
        }
        .header-title {
          font-size: 12px;
        }
        .collapse-icon {
          cursor: pointer;
          font-size: 10px;
          color: var(--cad-color-text-regular, #8A8D91);
          transition: transform 0.2s;
        }
        .body {
          padding: 8px;
          display: ${isCollapsed ? 'none' : 'block'};
          background: #FFFFFF;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="header">
        <span class="header-title">${title}</span>
        ${collapsible ? `<span class="collapse-icon">${isCollapsed ? '▶' : '▼'}</span>` : ''}
      </div>
      <div class="body">
        <slot></slot>
      </div>
      ${renderDraftBadge(isDraft)}
    `;

    if (collapsible) {
      const header = this.shadowRoot.querySelector('.header');
      if (header) {
        header.onclick = () => {
          if (this.hasAttribute('collapsed')) this.removeAttribute('collapsed');
          else this.setAttribute('collapsed', '');
        };
      }
    }
  }
}
customElements.define('cad-panel', CadPanel);

    if (typeof window !== 'undefined') window.CadPanel = CadPanel;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-panel> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-picker> (Key: picker)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadPicker = CadPicker;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-picker> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-picture> (Key: picture)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-picture> CAD 视口缩略图/图元预览容器 (映射自 Figma Picture Page 252:38)
 * --------------------------------------------------------------------
 */
class CadPicture extends HTMLElement {
  static get observedAttributes() {
    return ['src', 'alt', 'width', 'height', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const src = this.getAttribute('src');
    const alt = this.getAttribute('alt') || 'CAD图元预览';
    const w = this.getAttribute('width') || '100%';
    const h = this.getAttribute('height') || '120px';
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          position: relative;
          box-sizing: border-box;
          width: ${w};
          height: ${h};
          background: #18191B; /* CAD 经典深黑视口背景 */
          border: 1px solid var(--cad-color-border-default, #363B42);
          border-radius: var(--cad-border-radius-base, 4px);
          overflow: hidden;
        }
        .grid-bg {
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          background-image: linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
                            linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
          background-size: 16px 16px;
        }
        img {
          max-width: 90%;
          max-height: 90%;
          object-fit: contain;
        }
        .empty-hint {
          color: #646A73;
          font-size: 11px;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 4px;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="grid-bg">
        ${src ? `<img src="${src}" alt="${alt}">` : `<div class="empty-hint"><span>📐</span><span>${alt}</span></div>`}
      </div>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-picture', CadPicture);

    if (typeof window !== 'undefined') window.CadPicture = CadPicture;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-picture> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-popconfirm> (Key: popconfirm)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-popconfirm> 气泡确认框 (映射自 Figma Popconfirm Page 615:61944)
 * --------------------------------------------------------------------
 */
class CadPopconfirm extends HTMLElement {
  static get observedAttributes() {
    return ['title', 'ok-text', 'cancel-text', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.isOpen = false;
    this._onDoc = this._onDoc.bind(this);
  }

  connectedCallback() {
    this.render();
    document.addEventListener('click', this._onDoc);
  }

  disconnectedCallback() {
    document.removeEventListener('click', this._onDoc);
  }

  _onDoc(e) {
    if (!this.contains(e.target)) {
      if (this.isOpen) {
        this.isOpen = false;
        this.updatePopup();
      }
    }
  }

  attributeChangedCallback() {
    this.render();
  }

  updatePopup() {
    const p = this.shadowRoot.querySelector('.confirm-card');
    if (p) p.style.display = this.isOpen ? 'block' : 'none';
  }

  render() {
    const title = this.getAttribute('title') || '确认要执行此操作吗？';
    const okText = this.getAttribute('ok-text') || '确定';
    const cancelText = this.getAttribute('cancel-text') || '取消';
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          position: relative;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
        }
        .confirm-card {
          display: ${this.isOpen ? 'block' : 'none'};
          position: absolute;
          bottom: calc(100% + 8px);
          left: 50%;
          transform: translateX(-50%);
          width: 180px;
          background: #FFFFFF;
          border: 1px solid var(--cad-color-border-default, #D0D3D6);
          border-radius: 4px;
          box-shadow: 0 4px 16px rgba(0,0,0,0.15);
          z-index: 1500;
          padding: 8px;
        }
        .msg-line {
          display: flex;
          align-items: center;
          gap: 6px;
          margin-bottom: 8px;
          color: var(--cad-color-text-main, #1F2329);
        }
        .btn-line {
          display: flex;
          justify-content: flex-end;
          gap: 6px;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="trigger" style="display:inline-block; cursor:pointer;">
        <slot></slot>
      </div>
      <div class="confirm-card">
        <div class="msg-line">
          <span style="color:#FF7D00;">⚠️</span>
          <span>${title}</span>
        </div>
        <div class="btn-line">
          <cad-button size="small" type="secondary" class="btn-cancel">${cancelText}</cad-button>
          <cad-button size="small" type="primary" class="btn-ok">${okText}</cad-button>
        </div>
      </div>
      ${renderDraftBadge(isDraft)}
    `;

    this.shadowRoot.querySelector('.trigger').addEventListener('click', (e) => {
      e.stopPropagation();
      this.isOpen = !this.isOpen;
      this.updatePopup();
    });

    this.shadowRoot.querySelector('.btn-cancel').addEventListener('click', (e) => {
      e.stopPropagation();
      this.isOpen = false;
      this.updatePopup();
      this.dispatchEvent(new CustomEvent('cancel'));
    });

    this.shadowRoot.querySelector('.btn-ok').addEventListener('click', (e) => {
      e.stopPropagation();
      this.isOpen = false;
      this.updatePopup();
      this.dispatchEvent(new CustomEvent('confirm'));
    });
  }
}
customElements.define('cad-popconfirm', CadPopconfirm);

    if (typeof window !== 'undefined') window.CadPopconfirm = CadPopconfirm;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-popconfirm> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-popover> (Key: popover)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-popover> 气泡卡片 (映射自 Figma Popover Page 252:46)
 * --------------------------------------------------------------------
 */
class CadPopover extends HTMLElement {
  static get observedAttributes() {
    return ['title', 'trigger', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.isOpen = false;
    this._onDoc = this._onDoc.bind(this);
  }

  connectedCallback() {
    this.render();
    document.addEventListener('click', this._onDoc);
  }

  disconnectedCallback() {
    document.removeEventListener('click', this._onDoc);
  }

  _onDoc(e) {
    if (!this.contains(e.target)) {
      if (this.isOpen) {
        this.isOpen = false;
        this.updatePopup();
      }
    }
  }

  attributeChangedCallback() {
    this.render();
  }

  updatePopup() {
    const p = this.shadowRoot.querySelector('.pop-card');
    if (p) p.style.display = this.isOpen ? 'block' : 'none';
  }

  render() {
    const title = this.getAttribute('title') || '';
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          position: relative;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
        }
        .pop-card {
          display: ${this.isOpen ? 'block' : 'none'};
          position: absolute;
          bottom: calc(100% + 8px);
          left: 50%;
          transform: translateX(-50%);
          width: 200px;
          background: #FFFFFF;
          border: 1px solid var(--cad-color-border-default, #D0D3D6);
          border-radius: 4px;
          box-shadow: 0 4px 16px rgba(0,0,0,0.15);
          z-index: 1500;
          padding: 8px 10px;
        }
        .pop-card::after {
          content: "";
          position: absolute;
          top: 100%;
          left: 50%;
          margin-left: -5px;
          border-width: 5px;
          border-style: solid;
          border-color: #FFFFFF transparent transparent transparent;
        }
        .title {
          font-weight: 600;
          margin-bottom: 4px;
          color: var(--cad-color-text-main, #1F2329);
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="trigger" style="display:inline-block; cursor:pointer;">
        <slot name="trigger"><cad-button size="small">展开卡片</cad-button></slot>
      </div>
      <div class="pop-card">
        ${title ? `<div class="title">${title}</div>` : ''}
        <div class="content"><slot></slot></div>
      </div>
      ${renderDraftBadge(isDraft)}
    `;

    this.shadowRoot.querySelector('.trigger').addEventListener('click', (e) => {
      e.stopPropagation();
      this.isOpen = !this.isOpen;
      this.updatePopup();
    });
  }
}
customElements.define('cad-popover', CadPopover);

    if (typeof window !== 'undefined') window.CadPopover = CadPopover;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-popover> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-progress> (Key: progress)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-progress> 工业级进度指示器 (映射自 Figma Bar Page 253:55)
 * --------------------------------------------------------------------
 */
class CadProgress extends HTMLElement {
  static get observedAttributes() {
    return ['percent', 'status', 'stroke-width', 'show-info', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const percent = Math.min(100, Math.max(0, parseFloat(this.getAttribute('percent') || '0')));
    const status = this.getAttribute('status') || 'normal'; // 'normal' | 'success' | 'exception'
    const strokeWidth = this.getAttribute('stroke-width') || '6px';
    const showInfo = this.getAttribute('show-info') !== 'false';
    const isDraft = this.getAttribute('status') === 'draft';

    let barColor = 'var(--cad-color-primary, #266EFF)';
    if (status === 'success' || percent >= 100) barColor = '#00B42A';
    if (status === 'exception') barColor = '#F53F3F';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          width: 100%;
          min-width: 100px;
          position: relative;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
        }
        .track {
          flex: 1;
          height: ${strokeWidth};
          background: #E5E6EB;
          border-radius: 3px;
          overflow: hidden;
          position: relative;
        }
        .fill {
          height: 100%;
          width: ${percent}%;
          background: ${barColor};
          border-radius: 3px;
          transition: width 0.3s ease;
        }
        .text {
          font-size: 11px;
          color: var(--cad-color-text-main, #1F2329);
          min-width: 32px;
          text-align: right;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="track">
        <div class="fill"></div>
      </div>
      ${showInfo ? `<span class="text">${percent}%</span>` : ''}
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-progress', CadProgress);

    if (typeof window !== 'undefined') window.CadProgress = CadProgress;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-progress> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-project-browser> (Key: project_browser)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-project-browser> BIM 项目浏览器面板 (映射自 Figma ProjectBrowser Page 6376:55263)
 * --------------------------------------------------------------------
 */
class CadProjectBrowser extends HTMLElement {
  static get observedAttributes() {
    return ['title', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const title = this.getAttribute('title') || '项目浏览器 - 建筑1号楼';
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: flex;
          flex-direction: column;
          width: 240px;
          height: 360px;
          background: #FFFFFF;
          border: 1px solid #D0D3D6;
          border-radius: 4px;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: 12px;
          overflow: hidden;
        }
        .header {
          padding: 6px 8px;
          background: #F2F3F5;
          font-weight: 600;
          border-bottom: 1px solid #D0D3D6;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        .body {
          flex: 1;
          overflow-y: auto;
          padding: 4px;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="header">
        <span>${title}</span>
        <span style="cursor:pointer; color:#8F959E;">🔍</span>
      </div>
      <div class="body">
        <cad-tree></cad-tree>
      </div>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-project-browser', CadProjectBrowser);

    if (typeof window !== 'undefined') window.CadProjectBrowser = CadProjectBrowser;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-project-browser> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-property-panel> (Key: property_panel)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-property-panel> 属性编辑面板 PropertyGrid (映射自 Figma PropertyPanel Page 7462:11469)
 * --------------------------------------------------------------------
 */
class CadPropertyPanel extends HTMLElement {
  static get observedAttributes() {
    return ['title', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const title = this.getAttribute('title') || '特性 Properties';
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          width: 260px;
          background: #FFFFFF;
          border: 1px solid #D0D3D6;
          border-radius: 4px;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: 12px;
          overflow: hidden;
        }
        .header {
          padding: 6px 8px;
          background: #F2F3F5;
          font-weight: 600;
          border-bottom: 1px solid #D0D3D6;
        }
        .grid-table {
          width: 100%;
          border-collapse: collapse;
        }
        .grid-table td {
          padding: 4px 6px;
          border-bottom: 1px solid #F0F2F5;
        }
        .label-col {
          width: 40%;
          color: #646A73;
          background: #FAFAFA;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="header">${title}</div>
      <table class="grid-table">
        <tr><td class="label-col">图层</td><td>0 图层</td></tr>
        <tr><td class="label-col">颜色</td><td>ByLayer</td></tr>
        <tr><td class="label-col">线型</td><td>ByLayer</td></tr>
        <tr><td class="label-col">线宽</td><td>默认 (0.25mm)</td></tr>
        <tr><td class="label-col">标高</td><td>±0.000 (首层)</td></tr>
      </table>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-property-panel', CadPropertyPanel);

    if (typeof window !== 'undefined') window.CadPropertyPanel = CadPropertyPanel;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-property-panel> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-quick-nav> (Key: quick_nav)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-quick-nav> 快速访问工具栏 (映射自 Figma QuickNav Page 1712:473)
 * --------------------------------------------------------------------
 */
class CadQuickNav extends HTMLElement {
  static get observedAttributes() {
    return ['status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const isDraft = this.getAttribute('status') === 'draft';
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          align-items: center;
          gap: 2px;
          height: 28px;
          padding: 0 4px;
          background: #2C2D30;
          border-radius: 4px;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
        }
        .tool-btn {
          width: 22px;
          height: 22px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          color: #D3D5D9;
          border-radius: 3px;
          cursor: pointer;
          font-size: 13px;
          transition: background 0.15s;
        }
        .tool-btn:hover {
          background: rgba(255, 255, 255, 0.15);
          color: #FFFFFF;
        }
        .sep {
          width: 1px;
          height: 14px;
          background: #464A50;
          margin: 0 2px;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <span class="tool-btn" title="新建图纸">📄</span>
      <span class="tool-btn" title="打开图纸">📂</span>
      <span class="tool-btn" title="保存 (Ctrl+S)">💾</span>
      <span class="sep"></span>
      <span class="tool-btn" title="放弃/撤销 (Ctrl+Z)">↩️</span>
      <span class="tool-btn" title="重做 (Ctrl+Y)">↪️</span>
      <span class="sep"></span>
      <span class="tool-btn" title="打印/发布 (Ctrl+P)">🖨️</span>
      <slot></slot>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-quick-nav', CadQuickNav);

    if (typeof window !== 'undefined') window.CadQuickNav = CadQuickNav;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-quick-nav> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-radio> (Key: radio)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadRadio = CadRadio;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-radio> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-ribbon> (Key: ribbon)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-ribbon> CAD Ribbon 顶部多功能命令带 (映射自 Figma Ribbon Page 1461:34231)
 * --------------------------------------------------------------------
 */
class CadRibbon extends HTMLElement {
  static get observedAttributes() {
    return ['active-tab', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const activeTab = this.getAttribute('active-tab') || '常用';
    const tabs = ['常用', '插入', '注释', '参数化', '视图', '管理', '协作'];
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          position: relative;
          background: #F0F2F5;
          border-bottom: 1px solid #D0D3D6;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: 12px;
          user-select: none;
        }
        .tab-bar {
          display: flex;
          align-items: center;
          height: 28px;
          background: #E5E7EB;
          padding-left: 8px;
          border-bottom: 1px solid #D0D3D6;
        }
        .tab {
          padding: 4px 12px;
          cursor: pointer;
          color: #4E5969;
          font-weight: 500;
          border-top-left-radius: 4px;
          border-top-right-radius: 4px;
          transition: background 0.15s, color 0.15s;
        }
        .tab:hover {
          color: #1D2129;
        }
        .tab.active {
          background: #F0F2F5;
          color: #266EFF;
          font-weight: 600;
          box-shadow: 0 -1px 3px rgba(0,0,0,0.05);
        }
        .panel-area {
          display: flex;
          align-items: stretch;
          height: 72px;
          padding: 4px 8px;
          gap: 6px;
          overflow-x: auto;
        }
        .group-box {
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          border-right: 1px solid #D8DCE0;
          padding: 0 8px;
        }
        .group-title {
          font-size: 10px;
          color: #86909C;
          text-align: center;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="tab-bar">
        ${tabs.map(t => `<span class="tab ${t === activeTab ? 'active' : ''}">${t}</span>`).join('')}
      </div>
      <div class="panel-area">
        <slot>
          <div class="group-box">
            <div style="display:flex; gap:6px;">
              <cad-button size="small">直线</cad-button>
              <cad-button size="small">圆弧</cad-button>
              <cad-button size="small">矩形</cad-button>
            </div>
            <div class="group-title">绘图</div>
          </div>
          <div class="group-box">
            <div style="display:flex; gap:6px;">
              <cad-button size="small">移动</cad-button>
              <cad-button size="small">复制</cad-button>
              <cad-button size="small">镜像</cad-button>
            </div>
            <div class="group-title">修改</div>
          </div>
        </slot>
      </div>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-ribbon', CadRibbon);

    if (typeof window !== 'undefined') window.CadRibbon = CadRibbon;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-ribbon> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-scrollbar> (Key: scrollbar)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-scrollbar> 滚动条容器 (映射自 Figma Scrollbar Page 252:22)
 * --------------------------------------------------------------------
 */
class CadScrollbar extends HTMLElement {
  static get observedAttributes() {
    return ['orientation', 'theme', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const orientation = this.getAttribute('orientation') || 'vertical';
    const theme = this.getAttribute('theme') || 'dark'; // 'dark' | 'light'
    const isDraft = this.getAttribute('status') === 'draft';

    const thumbBg = theme === 'dark' ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.25)';
    const thumbHover = theme === 'dark' ? 'rgba(255, 255, 255, 0.35)' : 'rgba(0, 0, 0, 0.4)';
    const trackBg = theme === 'dark' ? '#1E1E1E' : '#F5F6F7';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          position: relative;
          overflow: auto;
          box-sizing: border-box;
        }
        :host::-webkit-scrollbar {
          width: 8px;
          height: 8px;
          background: ${trackBg};
        }
        :host::-webkit-scrollbar-thumb {
          background: ${thumbBg};
          border-radius: 4px;
        }
        :host::-webkit-scrollbar-thumb:hover {
          background: ${thumbHover};
        }
        :host::-webkit-scrollbar-corner {
          background: ${trackBg};
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <slot></slot>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-scrollbar', CadScrollbar);

    if (typeof window !== 'undefined') window.CadScrollbar = CadScrollbar;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-scrollbar> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-select> (Key: select)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadSelect = CadSelect;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-select> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-slider> (Key: slider)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-slider> 滑块调节器 (映射自 Figma Slider Page 252:33)
 * --------------------------------------------------------------------
 */
class CadSlider extends HTMLElement {
  static get observedAttributes() {
    return ['value', 'min', 'max', 'step', 'disabled', 'show-input', 'status'];
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
    return parseFloat(this.getAttribute('value') || '0');
  }

  set value(v) {
    this.setAttribute('value', v);
  }

  render() {
    const min = parseFloat(this.getAttribute('min') || '0');
    const max = parseFloat(this.getAttribute('max') || '100');
    const step = parseFloat(this.getAttribute('step') || '1');
    const val = parseFloat(this.getAttribute('value') || min);
    const disabled = this.hasAttribute('disabled');
    const showInput = this.hasAttribute('show-input');
    const isDraft = this.getAttribute('status') === 'draft';

    const percent = Math.min(100, Math.max(0, ((val - min) / (max - min)) * 100));

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          position: relative;
          width: 100%;
          min-width: 120px;
          height: var(--cad-height-small, 24px);
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
        }
        .track-wrap {
          flex: 1;
          position: relative;
          height: 4px;
          background: var(--cad-color-border-default, #E5E6EB);
          border-radius: 2px;
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
        }
        .fill-bar {
          position: absolute;
          left: 0;
          top: 0;
          height: 100%;
          width: ${percent}%;
          background: ${disabled ? '#C9CDD4' : 'var(--cad-color-primary, #266EFF)'};
          border-radius: 2px;
        }
        input[type="range"] {
          position: absolute;
          top: -6px;
          left: 0;
          width: 100%;
          height: 16px;
          opacity: 0;
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          margin: 0;
          z-index: 2;
        }
        .thumb {
          position: absolute;
          top: 50%;
          left: ${percent}%;
          transform: translate(-50%, -50%);
          width: 12px;
          height: 12px;
          border-radius: 50%;
          background: #FFFFFF;
          border: 2px solid ${disabled ? '#C9CDD4' : 'var(--cad-color-primary, #266EFF)'};
          box-shadow: 0 1px 3px rgba(0,0,0,0.2);
          pointer-events: none;
          z-index: 1;
          transition: transform 0.1s;
        }
        .val-display {
          font-size: 11px;
          color: var(--cad-color-text-main, #1F2329);
          min-width: 28px;
          text-align: right;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="track-wrap">
        <div class="fill-bar"></div>
        <div class="thumb"></div>
        <input type="range" min="${min}" max="${max}" step="${step}" value="${val}" ${disabled ? 'disabled' : ''}>
      </div>
      ${showInput ? `<span class="val-display">${val}</span>` : ''}
      ${renderDraftBadge(isDraft)}
    `;

    const inp = this.shadowRoot.querySelector('input');
    inp.addEventListener('input', (e) => {
      this.setAttribute('value', e.target.value);
      this.dispatchEvent(new CustomEvent('change', { detail: { value: parseFloat(e.target.value) } }));
    });
  }
}
customElements.define('cad-slider', CadSlider);

    if (typeof window !== 'undefined') window.CadSlider = CadSlider;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-slider> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-stair-tool> (Key: stair_tool)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-stair-tool> 双跑楼梯计算卡 (映射自 Figma StairTool Page 843:3972)
 * --------------------------------------------------------------------
 */
class CadStairTool extends HTMLElement {
  static get observedAttributes() {
    return ['status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const isDraft = this.getAttribute('status') === 'draft';
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: flex;
          flex-direction: column;
          gap: 6px;
          padding: 8px;
          background: #FFFFFF;
          border: 1px solid #D0D3D6;
          border-radius: 4px;
          box-sizing: border-box;
          font-size: 12px;
        }
        .row { display: flex; align-items: center; justify-content: space-between; }
        ${COMMON_DRAFT_STYLE}
      </style>
      <b>🪜 双跑楼梯参数</b>
      <div class="row"><span>梯段宽度:</span><cad-input size="small" value="1200" suffix-label="mm" style="width:80px;"></cad-input></div>
      <div class="row"><span>踏步高度:</span><cad-input size="small" value="150" suffix-label="mm" style="width:80px;"></cad-input></div>
      <div class="row"><span>踏步宽度:</span><cad-input size="small" value="300" suffix-label="mm" style="width:80px;"></cad-input></div>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-stair-tool', CadStairTool);

    if (typeof window !== 'undefined') window.CadStairTool = CadStairTool;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-stair-tool> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-status-bar> (Key: status_bar)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-status-bar> CAD 底部状态栏 (映射自 Figma StatusBar Page 2342:27138)
 * --------------------------------------------------------------------
 */
class CadStatusBar extends HTMLElement {
  static get observedAttributes() {
    return ['coords', 'scale', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const coords = this.getAttribute('coords') || 'X: 1204.50  Y: 850.25  Z: 0.00';
    const scale = this.getAttribute('scale') || '1:100';
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: flex;
          align-items: center;
          justify-content: space-between;
          height: 24px;
          background: #252628;
          color: #B2B6BD;
          padding: 0 8px;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Consolas", monospace);
          font-size: 11px;
          border-top: 1px solid #363B42;
          user-select: none;
        }
        .left-group {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .right-group {
          display: flex;
          align-items: center;
          gap: 4px;
        }
        .status-btn {
          padding: 2px 6px;
          border-radius: 2px;
          cursor: pointer;
          font-size: 11px;
          color: #B2B6BD;
        }
        .status-btn.active {
          background: #266EFF;
          color: #FFFFFF;
        }
        .status-btn:hover:not(.active) {
          background: rgba(255,255,255,0.1);
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="left-group">
        <span>${coords}</span>
        <span style="color:#646A73;">|</span>
        <span style="cursor:pointer;" title="比例尺">${scale}</span>
      </div>
      <div class="right-group">
        <span class="status-btn active" title="模型空间">模型</span>
        <span class="status-btn active" title="正交模式 (F8)">正交</span>
        <span class="status-btn" title="极轴追踪 (F10)">极轴</span>
        <span class="status-btn active" title="对象捕捉 (F3)">捕捉</span>
        <span class="status-btn active" title="动态输入 (F12)">动入</span>
      </div>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-status-bar', CadStatusBar);

    if (typeof window !== 'undefined') window.CadStatusBar = CadStatusBar;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-status-bar> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-alert> (Key: sweetalert)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadAlert = CadAlert;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-alert> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-switch> (Key: switch)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadSwitch = CadSwitch;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-switch> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-table> (Key: table)
// ====================================================================
try {
  (function() {
class CadTable extends HTMLElement {
  static get observedAttributes() {
    return [
      'cols', 'rows', 'col-width', 'row-height',
      'show-title', 'show-header', 'show-summary',
      'title-text', 'headers', 'data', 'zoom',
      'row1-style', 'row2-style', 'row-other-style', 'empty'
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

    // 兼容旧版属性与新版结构化布尔属性
    const hasLegacy = this.hasAttribute('row1-style') || this.hasAttribute('row2-style');
    const showTitle = hasLegacy
      ? (this.getAttribute('row1-style') === '标题')
      : (this.getAttribute('show-title') !== 'false');
    const showHeader = hasLegacy
      ? (this.getAttribute('row2-style') === '表头')
      : (this.getAttribute('show-header') !== 'false');
    const showSummary = this.getAttribute('show-summary') === 'true';
    const titleText = this.getAttribute('title-text') || '标题';

    let customHeaders = null;
    let customData = null;
    try {
      if (this.hasAttribute('headers')) customHeaders = JSON.parse(this.getAttribute('headers'));
    } catch (e) {}
    try {
      if (this.hasAttribute('data')) customData = JSON.parse(this.getAttribute('data'));
    } catch (e) {}

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
          const hText = (Array.isArray(customHeaders) && customHeaders[c] !== undefined)
            ? customHeaders[c]
            : '表头';
          hCells += `<td>${hText}</td>`;
        }
        rowsHtml += `<tr class="row-header">${hCells}</tr>`;
      }

      // 3. 数据行 (Data)
      for (let r = 0; r < rows; r++) {
        const cls = r === 0 ? 'row-data selected' : 'row-data';
        let dCells = `<td class="idx-cell">${rowIdx++}</td>`;
        for (let c = 0; c < cols; c++) {
          const dText = (Array.isArray(customData) && Array.isArray(customData[r]) && customData[r][c] !== undefined)
            ? customData[r][c]
            : '数据';
          dCells += `<td>${dText}</td>`;
        }
        rowsHtml += `<tr class="${cls}">${dCells}</tr>`;
      }

      // 4. 汇总底行 (Summary)
      if (showSummary) {
        let sCells = `<td class="idx-cell">${rowIdx++}</td>`;
        sCells += `<td class="summary-label">汇总</td>`;
        for (let c = 1; c < cols; c++) {
          sCells += `<td class="summary-val">—</td>`;
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
    if (typeof window !== 'undefined') window.CadTable = CadTable;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-table> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-table-viewport> (Key: table_viewport)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadTableViewport = CadTableViewport;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-table-viewport> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-tabs> (Key: tabs)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadTabs = CadTabs;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-tabs> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-tag> (Key: tag)
// ====================================================================
try {
  (function() {
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
    if (typeof window !== 'undefined') window.CadTag = CadTag;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-tag> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-tooltip> (Key: tooltip)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-tooltip> 文字气泡 (映射自 Figma Tooltip Page 368:1277)
 * --------------------------------------------------------------------
 */
class CadTooltip extends HTMLElement {
  static get observedAttributes() {
    return ['title', 'content', 'placement', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const text = this.getAttribute('content') || this.getAttribute('title') || '提示信息';
    const placement = this.getAttribute('placement') || 'top';
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          position: relative;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
        }
        .bubble {
          visibility: hidden;
          opacity: 0;
          position: absolute;
          background: #1F2329;
          color: #FFFFFF;
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 11px;
          line-height: 1.3;
          white-space: nowrap;
          z-index: 2000;
          box-shadow: 0 4px 10px rgba(0,0,0,0.25);
          pointer-events: none;
          transition: opacity 0.2s, visibility 0.2s;
        }
        :host(:hover) .bubble {
          visibility: visible;
          opacity: 1;
        }
        .bubble.top {
          bottom: calc(100% + 6px);
          left: 50%;
          transform: translateX(-50%);
        }
        .bubble.top::after {
          content: "";
          position: absolute;
          top: 100%;
          left: 50%;
          margin-left: -4px;
          border-width: 4px;
          border-style: solid;
          border-color: #1F2329 transparent transparent transparent;
        }
        .bubble.bottom {
          top: calc(100% + 6px);
          left: 50%;
          transform: translateX(-50%);
        }
        .bubble.bottom::after {
          content: "";
          position: absolute;
          bottom: 100%;
          left: 50%;
          margin-left: -4px;
          border-width: 4px;
          border-style: solid;
          border-color: transparent transparent #1F2329 transparent;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="target-wrap">
        <slot></slot>
      </div>
      <div class="bubble ${placement}">${text}</div>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-tooltip', CadTooltip);

    if (typeof window !== 'undefined') window.CadTooltip = CadTooltip;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-tooltip> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-tree> (Key: tree)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-tree> CAD/BIM 模型构件树 (映射自 Figma Tree Page 5454:66767)
 * --------------------------------------------------------------------
 */
class CadTree extends HTMLElement {
  static get observedAttributes() {
    return ['data', 'checkable', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const isDraft = this.getAttribute('status') === 'draft';
    const checkable = this.hasAttribute('checkable');
    let treeData = [];
    try {
      const d = this.getAttribute('data');
      if (d) treeData = JSON.parse(d);
    } catch(e) {}

    // 默认内置 CAD 典型构件层级演示数据
    if (!treeData.length) {
      treeData = [
        { id: '1', title: '地上建筑模型', expanded: true, children: [
          { id: '1-1', title: 'F1 首层平面', expanded: true, children: [
            { id: '1-1-1', title: '基本墙: 混凝土剪力墙 200mm' },
            { id: '1-1-2', title: '门: 单扇平开门 900x2100mm' }
          ]},
          { id: '1-2', title: 'F2 二层平面', children: [
            { id: '1-2-1', title: '基本墙: 砌块填充墙 100mm' }
          ]}
        ]},
        { id: '2', title: '地下基础与结构', children: [
          { id: '2-1', title: '承台与基础梁' }
        ]}
      ];
    }

    const renderNodes = (nodes, level = 0) => {
      return nodes.map(n => `
        <div class="tree-node" style="padding-left: ${level * 16 + 6}px;" data-id="${n.id}">
          <span class="expander ${n.children ? 'has-child' : ''}">${n.children ? (n.expanded ? '▼' : '▶') : '•'}</span>
          ${checkable ? `<input type="checkbox" class="node-chk">` : ''}
          <span class="node-icon">${n.children ? '📁' : '📄'}</span>
          <span class="node-title">${n.title}</span>
        </div>
        ${n.children && n.expanded !== false ? `<div class="node-children">${renderNodes(n.children, level + 1)}</div>` : ''}
      `).join('');
    };

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          position: relative;
          background: var(--cad-color-bg-white, #FFFFFF);
          border: 1px solid var(--cad-color-border-default, #D0D3D6);
          border-radius: var(--cad-border-radius-base, 4px);
          max-height: 280px;
          overflow-y: auto;
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
          user-select: none;
        }
        .tree-node {
          display: flex;
          align-items: center;
          gap: 4px;
          height: 24px;
          cursor: pointer;
          color: var(--cad-color-text-main, #1F2329);
          transition: background 0.15s;
        }
        .tree-node:hover {
          background: var(--cad-color-bg-hover, #F2F3F5);
        }
        .tree-node.selected {
          background: #E8F3FF;
          color: var(--cad-color-primary, #266EFF);
        }
        .expander {
          width: 12px;
          font-size: 8px;
          color: #8F959E;
          text-align: center;
        }
        .node-icon {
          font-size: 11px;
        }
        .node-title {
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="tree-container">
        ${renderNodes(treeData)}
      </div>
      ${renderDraftBadge(isDraft)}
    `;

    this.shadowRoot.querySelectorAll('.tree-node').forEach(el => {
      el.addEventListener('click', () => {
        this.shadowRoot.querySelectorAll('.tree-node').forEach(n => n.classList.remove('selected'));
        el.classList.add('selected');
        this.dispatchEvent(new CustomEvent('select', { detail: { id: el.getAttribute('data-id') } }));
      });
    });
  }
}
customElements.define('cad-tree', CadTree);

    if (typeof window !== 'undefined') window.CadTree = CadTree;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-tree> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-tree-select> (Key: tree_select)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-tree-select> 树形下拉选择器 (映射自 Figma TreeSelect Page 252:39)
 * --------------------------------------------------------------------
 */
class CadTreeSelect extends HTMLElement {
  static get observedAttributes() {
    return ['value', 'placeholder', 'disabled', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.isOpen = false;
    this._onDoc = this._onDoc.bind(this);
  }

  connectedCallback() {
    this.render();
    document.addEventListener('click', this._onDoc);
  }

  disconnectedCallback() {
    document.removeEventListener('click', this._onDoc);
  }

  _onDoc(e) {
    if (!this.contains(e.target)) {
      if (this.isOpen) {
        this.isOpen = false;
        this.updatePopup();
      }
    }
  }

  attributeChangedCallback() {
    this.render();
  }

  updatePopup() {
    const pop = this.shadowRoot.querySelector('.tree-popup');
    if (pop) pop.style.display = this.isOpen ? 'block' : 'none';
  }

  render() {
    const val = this.getAttribute('value') || '';
    const placeholder = this.getAttribute('placeholder') || '请选择构件层级...';
    const disabled = this.hasAttribute('disabled');
    const isDraft = this.getAttribute('status') === 'draft';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          position: relative;
          width: 100%;
          min-width: 160px;
          height: var(--cad-height-small, 24px);
          box-sizing: border-box;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: var(--cad-font-size-base, 12px);
        }
        .selector-box {
          display: flex;
          align-items: center;
          justify-content: space-between;
          height: 100%;
          padding: 2px 8px;
          background: var(--cad-color-bg-white, #FFFFFF);
          border: 1px solid var(--cad-color-border-default, #D0D3D6);
          border-radius: var(--cad-border-radius-base, 4px);
          cursor: ${disabled ? 'not-allowed' : 'pointer'};
          opacity: ${disabled ? '0.6' : '1'};
          user-select: none;
        }
        .selector-box:hover {
          border-color: ${disabled ? '#D0D3D6' : 'var(--cad-color-primary, #266EFF)'};
        }
        .tree-popup {
          display: ${this.isOpen ? 'block' : 'none'};
          position: absolute;
          top: calc(100% + 4px);
          left: 0;
          width: 100%;
          z-index: 1000;
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <div class="selector-box">
        <span style="color: ${val ? '#1F2329' : '#8F959E'}">${val || placeholder}</span>
        <span style="font-size: 9px; color: #8F959E;">▼</span>
      </div>
      <div class="tree-popup">
        <cad-tree></cad-tree>
      </div>
      ${renderDraftBadge(isDraft)}
    `;

    this.shadowRoot.querySelector('.selector-box').addEventListener('click', (e) => {
      e.stopPropagation();
      if (!disabled) {
        this.isOpen = !this.isOpen;
        this.updatePopup();
      }
    });

    const tree = this.shadowRoot.querySelector('cad-tree');
    if (tree) {
      tree.addEventListener('select', (e) => {
        this.setAttribute('value', e.detail.id);
        this.isOpen = false;
        this.updatePopup();
        this.render();
      });
    }
  }
}
customElements.define('cad-tree-select', CadTreeSelect);

    if (typeof window !== 'undefined') window.CadTreeSelect = CadTreeSelect;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-tree-select> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-typography> (Key: typography)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-typography> 字体排版组件 (映射自 Figma Typography Page 252:20)
 * --------------------------------------------------------------------
 */
class CadTypography extends HTMLElement {
  static get observedAttributes() {
    return ['type', 'size', 'color', 'weight', 'copyable', 'status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const type = this.getAttribute('type') || 'body'; // 'h1' | 'h2' | 'h3' | 'body' | 'caption' | 'secondary'
    const color = this.getAttribute('color');
    const weight = this.getAttribute('weight') || (type.startsWith('h') ? '600' : 'normal');
    const copyable = this.hasAttribute('copyable');
    const isDraft = this.getAttribute('status') === 'draft';

    let fontSize = 'var(--cad-font-size-base, 12px)';
    let lineHeight = '1.5';
    let defaultColor = 'var(--cad-color-text-main, #1F2329)';

    if (type === 'h1') {
      fontSize = '18px';
      lineHeight = '1.3';
    } else if (type === 'h2') {
      fontSize = '15px';
      lineHeight = '1.4';
    } else if (type === 'h3') {
      fontSize = '13px';
      lineHeight = '1.4';
      defaultColor = 'var(--cad-color-text-title, #1F2329)';
    } else if (type === 'caption') {
      fontSize = '11px';
      defaultColor = 'var(--cad-color-text-placeholder, #8F959E)';
    } else if (type === 'secondary') {
      fontSize = '12px';
      defaultColor = 'var(--cad-color-text-sub, #646A73)';
    }

    const finalColor = color || defaultColor;

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          position: relative;
          font-family: var(--cad-font-family, "Segoe UI", -apple-system, sans-serif);
          font-size: ${fontSize};
          line-height: ${lineHeight};
          color: ${finalColor};
          font-weight: ${weight};
          box-sizing: border-box;
        }
        .text-wrap {
          display: inline-flex;
          align-items: center;
          gap: 4px;
        }
        .copy-btn {
          cursor: pointer;
          opacity: 0.6;
          transition: opacity 0.2s;
          display: inline-flex;
          align-items: center;
        }
        .copy-btn:hover {
          opacity: 1;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <span class="text-wrap">
        <slot></slot>
        ${copyable ? `<span class="copy-btn" title="点击复制" onclick="navigator.clipboard.writeText(this.parentElement.innerText)">📋</span>` : ''}
      </span>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-typography', CadTypography);

    if (typeof window !== 'undefined') window.CadTypography = CadTypography;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-typography> 失败，已熔断跳过:', err);
}

// ====================================================================
// Component: <cad-wall-tool> (Key: wall_tool)
// ====================================================================
try {
  (function() {
/**
 * --------------------------------------------------------------------
 * <cad-wall-tool> 绘制墙体参数快捷卡 (映射自 Figma WallTool Page 252:48)
 * --------------------------------------------------------------------
 */
class CadWallTool extends HTMLElement {
  static get observedAttributes() {
    return ['status'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const isDraft = this.getAttribute('status') === 'draft';
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 6px 10px;
          background: #F8F9FA;
          border: 1px solid #D0D3D6;
          border-radius: 4px;
          box-sizing: border-box;
          font-size: 12px;
        }
        ${COMMON_DRAFT_STYLE}
      </style>
      <span>🧱 墙体厚度:</span>
      <cad-input size="small" value="200" suffix-label="mm" style="width:90px;"></cad-input>
      <span>定位线:</span>
      <cad-select size="small" value="wall_center" style="width:110px;">
        <option value="wall_center">墙中心线</option>
        <option value="core_center">核心层中心</option>
        <option value="finish_ext">面层外部</option>
      </cad-select>
      ${renderDraftBadge(isDraft)}
    `;
  }
}
customElements.define('cad-wall-tool', CadWallTool);

    if (typeof window !== 'undefined') window.CadWallTool = CadWallTool;
  })();
} catch (err) {
  console.error('[Nova Component Warning] 注册组件 <cad-wall-tool> 失败，已熔断跳过:', err);
}


/**
 * ====================================================================
 * End of Nova CAD/BIM Components Bundle (Total: 52 components)
 * ====================================================================
 */
