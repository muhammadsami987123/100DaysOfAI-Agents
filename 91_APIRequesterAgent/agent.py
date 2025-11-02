import requests
import json
import time
from typing import Dict, Any, Optional, Tuple
from config import Config
import os

class APIRequesterAgent:
    def __init__(self):
        self.history_file = Config.HISTORY_FILE
        self._ensure_history_file_exists()

    def _ensure_history_file_exists(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump([], f)

    def _save_request_to_history(self, request_data: Dict[str, Any], response_data: Dict[str, Any]):
        history_entry = {
            "timestamp": time.time(),
            "request": request_data,
            "response": response_data
        }
        with open(self.history_file, 'r+') as f:
            history = json.load(f)
            history.append(history_entry)
            f.seek(0)
            json.dump(history, f, indent=4)

    def get_request_history(self) -> list:
        with open(self.history_file, 'r') as f:
            return json.load(f)

    def send_request(
        self,
        url: str,
        method: str,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, Any], int, int]:
        start_time = time.time()
        response_data = {}
        status_code = 0
        response_time = 0

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=body, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=body, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return {"error": "Invalid HTTP method"}, 400, 0

            status_code = response.status_code
            response_time = int((time.time() - start_time) * 1000)

            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"message": response.text}

            request_data = {"url": url, "method": method, "headers": headers, "body": body}
            self._save_request_to_history(request_data, {"status_code": status_code, "response_data": response_data})

            return response_data, status_code, response_time

        except requests.exceptions.Timeout:
            return {"error": "Request timed out"}, 408, int((time.time() - start_time) * 1000)
        except requests.exceptions.ConnectionError:
            return {"error": "Connection error"}, 500, int((time.time() - start_time) * 1000)
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500, int((time.time() - start_time) * 1000)
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}, 500, int((time.time() - start_time) * 1000)

    def format_response(self, response_data: Dict[str, Any], status_code: int, response_time: int) -> Dict[str, Any]:
        formatted_response = {
            "response_json": json.dumps(response_data, indent=2),
            "status_code": status_code,
            "response_time": f"{response_time}ms"
        }
        return formatted_response
