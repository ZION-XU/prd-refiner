"""Start the pinned MCP Atlassian server with native Confluence headings.

The upstream 0.8.4 preprocessor enables generated heading anchors. Those
anchors appear as editable Anchor macros in Confluence and are unnecessary for
ordinary PRD headings. This process-local patch changes only that converter
option; all MCP tools and authentication continue to come from mcp-atlassian.
"""

from __future__ import annotations

from typing import Any

import mcp_atlassian.preprocessing.confluence as confluence_preprocessing


_original_options = confluence_preprocessing.ConfluenceConverterOptions


def _options_without_heading_anchors(*args: Any, **kwargs: Any) -> Any:
    kwargs["heading_anchors"] = False
    return _original_options(*args, **kwargs)


confluence_preprocessing.ConfluenceConverterOptions = _options_without_heading_anchors


if __name__ == "__main__":
    from mcp_atlassian import main

    main()
