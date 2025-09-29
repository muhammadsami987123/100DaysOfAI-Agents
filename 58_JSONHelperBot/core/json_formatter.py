import json
from typing import Any, Dict, Optional, Tuple

class JsonFormatter:
    """Handles formatting of JSON data"""

    def pretty_print(self, json_data: Dict[str, Any], indent: int = 2) -> str:
        """
        Pretty prints a JSON object.

        Args:
            json_data: The parsed JSON object.
            indent: The indentation level for pretty printing.

        Returns:
            A pretty-printed JSON string.
        """
        return json.dumps(json_data, indent=indent)

    def minify(self, json_data: Dict[str, Any]) -> str:
        """
        Minifies a JSON object (removes whitespace).

        Args:
            json_data: The parsed JSON object.

        Returns:
            A minified JSON string.
        """
        return json.dumps(json_data, separators=(',', ':'))
