"""Unit tests for render_story_map.py."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from render_story_map import (
    find_system_browser,
    generate_story_map_html,
    render_story_map,
    main,
)

PNG_HEADER = (b'\x89PNG\r\n\x1a\n' + b'\x00\x00\x00\rIHDR' +
              b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00' + b'\x00' * 12)


class RenderStoryMapTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.sample_data = {
            "title": "测试用户故事地图",
            "badge": "V1.0",
            "core_value": "简化数据集成",
            "role": "GIS 工程师",
            "activities": [
                {"id": "ACT-1", "name": "发现服务", "desc": "查找与定位"},
                {"id": "ACT-2", "name": "加载服务", "desc": "解析图层"},
            ],
            "releases": [
                {
                    "theme": "mvp",
                    "badge": "MVP Release",
                    "title": "第 1 阶段",
                    "desc": "核心连通性",
                    "stories": [
                        {
                            "id": "US-001",
                            "activity": 0,
                            "fr": "FR-001",
                            "title": "输入 URL",
                            "desc": "支持输入服务地址",
                            "tag": "P0"
                        },
                        {
                            "id": "US-002",
                            "activity": "ACT-2",
                            "fr": "FR-002",
                            "title": "渲染图层",
                            "desc": "将要素添加到图面",
                            "tag": "P0"
                        }
                    ]
                },
                {
                    "theme": "next",
                    "badge": "Next Release",
                    "title": "第 2 阶段",
                    "desc": "高级功能",
                    "stories": [
                        {
                            "id": "US-003",
                            "activity": "发现服务",
                            "fr": "FR-003",
                            "title": "历史记录",
                            "desc": "记忆最近常用服务"
                        }
                    ]
                }
            ]
        }

    def test_generate_html_content_and_geometry(self):
        html, width, height = generate_story_map_html(self.sample_data)
        self.assertIn("<title>测试用户故事地图</title>", html)
        self.assertIn("简化数据集成", html)
        self.assertIn("GIS 工程师", html)
        self.assertIn("发现服务", html)
        self.assertIn("加载服务", html)
        self.assertIn("US-001", html)
        self.assertIn("US-002", html)
        self.assertIn("US-003", html)
        self.assertIn("FR-001", html)
        self.assertIn("MVP Release", html)
        self.assertIn("Next Release", html)
        self.assertGreater(width, 700)
        self.assertGreater(height, 400)

    def test_generate_html_activity_lookup_fallback(self):
        data = {
            "title": "Fallback 测试",
            "activities": [{"id": "A1", "name": "单活动"}],
            "releases": [
                {
                    "theme": "mvp",
                    "badge": "R1",
                    "stories": [
                        {"id": "US-X", "activity": "UNKNOWN_ACTIVITY", "title": "未识别活动归入第一列"}
                    ]
                }
            ]
        }
        html, _, _ = generate_story_map_html(data)
        self.assertIn("US-X", html)
        self.assertIn("未识别活动归入第一列", html)

    def test_generate_html_escaping(self):
        data = {
            "title": "测试 <>& 符号",
            "activities": [{"id": "A<1>", "name": "活动 & 名称"}],
            "releases": [
                {
                    "theme": "mvp",
                    "badge": "R<1>",
                    "stories": [
                        {"id": "US-1", "activity": 0, "title": "故事 <Title & Check>"}
                    ]
                }
            ]
        }
        html, _, _ = generate_story_map_html(data)
        self.assertIn("测试 &lt;&gt;&amp; 符号", html)
        self.assertIn("A&lt;1&gt;", html)
        self.assertIn("故事 &lt;Title &amp; Check&gt;", html)

    def test_render_story_map_missing_data_file(self):
        res = render_story_map(self.root / "nonexistent.json", self.root / "out.png")
        self.assertFalse(res["passed"])
        self.assertIn("data file not found", res["errors"][0])

    def test_render_story_map_invalid_json(self):
        bad_json = self.root / "bad.json"
        bad_json.write_text("{invalid json", encoding="utf-8")
        res = render_story_map(bad_json, self.root / "out.png")
        self.assertFalse(res["passed"])
        self.assertIn("invalid JSON format", res["errors"][0])

    @patch("render_story_map.find_system_browser", return_value=None)
    def test_render_story_map_fallback_when_no_browser(self, _find_browser):
        data_file = self.root / "data.json"
        data_file.write_text(json.dumps(self.sample_data, ensure_ascii=False), encoding="utf-8")
        out_png = self.root / "out.png"

        res = render_story_map(data_file, out_png, browser_path=None)
        self.assertFalse(res["passed"])
        self.assertIn("no Chrome/Edge browser found", res["errors"][0])
        fallback_html = Path(res["html"])
        self.assertTrue(fallback_html.is_file())
        self.assertIn("测试用户故事地图", fallback_html.read_text(encoding="utf-8"))

    def test_render_story_map_successful_browser_run(self):
        data_file = self.root / "data.json"
        data_file.write_text(json.dumps(self.sample_data, ensure_ascii=False), encoding="utf-8")
        out_png = self.root / "out.png"
        fake_browser = self.root / "fake_browser.exe"
        fake_browser.write_text("dummy", encoding="utf-8")

        def fake_run(command, **_kwargs):
            out_arg = [c for c in command if c.startswith("--screenshot=")][0]
            out_path = Path(out_arg.split("=", 1)[1])
            out_path.write_bytes(PNG_HEADER)
            return subprocess.CompletedProcess(command, 0, "", "")

        with patch("render_story_map.subprocess.run", side_effect=fake_run):
            res = render_story_map(data_file, out_png, browser_path=fake_browser)

        self.assertTrue(res["passed"])
        self.assertTrue(out_png.is_file())
        self.assertEqual(res["size"], len(PNG_HEADER))

    def test_render_story_map_browser_failure(self):
        data_file = self.root / "data.json"
        data_file.write_text(json.dumps(self.sample_data, ensure_ascii=False), encoding="utf-8")
        out_png = self.root / "out.png"
        fake_browser = self.root / "fake_browser.exe"
        fake_browser.write_text("dummy", encoding="utf-8")

        def fake_run(command, **_kwargs):
            return subprocess.CompletedProcess(command, 1, "", "Fatal error rendering")

        with patch("render_story_map.subprocess.run", side_effect=fake_run):
            res = render_story_map(data_file, out_png, browser_path=fake_browser)

        self.assertFalse(res["passed"])
        self.assertIn("screenshot failed with exit code 1", res["errors"][0])

    def test_cli_main(self):
        data_file = self.root / "data.json"
        data_file.write_text(json.dumps(self.sample_data, ensure_ascii=False), encoding="utf-8")
        out_png = self.root / "out.png"
        fake_browser = self.root / "fake_browser.exe"
        fake_browser.write_text("dummy", encoding="utf-8")

        def fake_run(command, **_kwargs):
            out_arg = [c for c in command if c.startswith("--screenshot=")][0]
            out_path = Path(out_arg.split("=", 1)[1])
            out_path.write_bytes(PNG_HEADER)
            return subprocess.CompletedProcess(command, 0, "", "")

        with patch("render_story_map.subprocess.run", side_effect=fake_run):
            code = main([
                "--data", str(data_file),
                "--output", str(out_png),
                "--browser", str(fake_browser),
            ])
        self.assertEqual(code, 0)
        self.assertTrue(out_png.is_file())


if __name__ == "__main__":
    unittest.main()
