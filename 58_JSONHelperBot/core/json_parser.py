import json
import requests
from typing import Any, Dict, Optional, Tuple
import re

class JsonParser:
    """Handles parsing and validating JSON data from various sources"""

    def parse_from_string(self, json_string: str) -> Tuple[Optional[Dict[str, Any]], Optional[str], bool]:
        """
        Parses and validates a JSON string. Attempts to fix common errors if parsing fails.

        Args:
            json_string: The raw JSON string.

        Returns:
            A tuple containing the parsed JSON object (or None), an error message (or None), and
            a boolean indicating if the JSON was fixed.
        """
        fixed = False
        try:
            data = json.loads(json_string)
            return data, None, fixed
        except json.JSONDecodeError as e:
            # Attempt to fix common issues
            fixed_json_string = self._attempt_fix(json_string)
            if fixed_json_string != json_string:
                fixed = True
                try:
                    data = json.loads(fixed_json_string)
                    return data, None, fixed
                except json.JSONDecodeError as fixed_e:
                    return None, f"JSON parsing error even after attempt to fix: {fixed_e}", fixed
            return None, f"JSON parsing error: {e}", fixed

    def _attempt_fix(self, json_string: str) -> str:
        """
        Attempts to fix common JSON syntax errors like unquoted keys or single quotes.
        This is a heuristic and might not catch all errors or produce valid JSON in all cases.
        """
        fixed_string = json_string.replace("'", '"')

        # More robust approach: Try to load with JavaScript-like syntax parsing first.
        # This is a common pattern for handling malformed JSON.
        try:
            # Use a JavaScript-like parser if available (e.g., `demjson` or `json5`)
            # Since we don't have these, we'll try a more aggressive regex approach.

            # Add double quotes to unquoted keys
            # Matches keys that are valid identifiers (start with letter/underscore, contain letters/numbers/underscores)
            # and are not already quoted, and are followed by a colon.
            fixed_string = re.sub(r'([{\s,]+)(\b[a-zA-Z_][a-zA-Z0-9_]*\b)(?=\s*:)', r'\1"\2"', fixed_string, flags=re.MULTILINE)

            # Add double quotes around unquoted string values
            # Matches values after a colon, that are not numbers, booleans, or null,
            # and are not already quoted. Captures until a comma, closing brace/bracket, or end of string.
            fixed_string = re.sub(r':\s*(\\b(?!true\\b|false\\b|null\\b)[a-zA-Z_][a-zA-Z0-9_]*\\b)([,\]} ]|$)', r':"\1"\2', fixed_string, flags=re.IGNORECASE|re.MULTILINE)
            
            # Handle cases where value is at the end of the JSON string without a trailing comma/bracket/brace
            fixed_string = re.sub(r':\s*(\\b(?!true\\b|false\\b|null\\b)[a-zA-Z_][a-zA-Z0-9_]*\\b)$' , r':"\1"' , fixed_string , flags=re.IGNORECASE|re.MULTILINE)

            # Fix trailing commas in objects or arrays (e.g., `[1,2,]` or `{"a":1,}`)
            fixed_string = re.sub(r',\s*([}\]])', r'\1', fixed_string)

        except Exception as e:
            # If aggressive regex itself fails, fall back to original string
            print(f"Warning: Aggressive regex fix failed: {e}")
            pass # Will re-attempt json.loads with potentially partially fixed string

        return fixed_string

    def parse_from_file(self, file_path: str) -> Tuple[Optional[Dict[str, Any]], Optional[str], bool]:
        """
        Reads and parses JSON from a file. Attempts to fix common errors if parsing fails.

        Args:
            file_path: The path to the JSON file.

        Returns:
            A tuple containing the parsed JSON object (or None), an error message (or None), and
            a boolean indicating if the JSON was fixed.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_string = f.read()
            return self.parse_from_string(json_string)
        except FileNotFoundError:
            return None, f"Error: File not found at {file_path}", False
        except Exception as e:
            return None, f"Error reading file {file_path}: {e}", False

    def parse_from_url(self, url: str) -> Tuple[Optional[Dict[str, Any]], Optional[str], bool]:
        """
        Fetches and parses JSON from a public URL. Attempts to fix common errors if parsing fails.

        Args:
            url: The public URL.

        Returns:
            A tuple containing the parsed JSON object (or None), an error message (or None), and
            a boolean indicating if the JSON was fixed.
        """
        try:
            response = requests.get(url, timeout=10)  # 10-second timeout
            response.raise_for_status()  # Raise an exception for HTTP errors
            json_string = response.text
            return self.parse_from_string(json_string) # Reuse string parsing with fix attempt
        except requests.exceptions.Timeout:
            return None, "Error: Request timed out while fetching from URL.", False
        except requests.exceptions.RequestException as e:
            return None, f"Error fetching from URL {url}: {e}", False
        except Exception as e:
            return None, f"An unexpected error occurred while fetching from URL: {e}", False
