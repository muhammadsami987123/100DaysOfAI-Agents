import requests
import qrcode
import os
from PIL import Image
from io import BytesIO
import base64
from config import Config # Import Config

class URLShortenerAgent:
    def __init__(self, api_service=Config.DEFAULT_SHORTENER_API):
        self.api_service = api_service
        self.tinyurl_api_key = Config.TINYURL_API_KEY

    def shorten_url(self, long_url, alias=None):
        if self.api_service == 'shrtco.de':
            return self._shorten_with_shrtcode(long_url, alias)
        elif self.api_service == 'tinyurl':
            return self._shorten_with_tinyurl(long_url, alias)
        else:
            return {"error": "Unsupported API service", "short_link": None}

    def _shorten_with_shrtcode(self, long_url, alias):
        try:
            params = {'url': long_url}
            if alias:
                params['custom_code'] = alias # shrtco.de uses 'custom_code' for alias
            response = requests.get("https://api.shrtco.de/v2/shorten", params=params)
            response.raise_for_status()
            data = response.json()
            if data['ok']:
                return {"error": None, "short_link": data['result']['full_short_link']}
            else:
                return {"error": data['error'], "short_link": None}
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {e}", "short_link": None}

    def _shorten_with_tinyurl(self, long_url, alias):
        if not self.tinyurl_api_key:
            return {"error": "TinyURL API key not configured.", "short_link": None}
        try:
            headers = {
                "Authorization": f"Bearer {self.tinyurl_api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "url": long_url
            }
            if alias:
                data["domain"] = "tinyurl.com"
                data["alias"] = alias

            response = requests.post("https://api.tinyurl.com/create", headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            if result['code'] == 0: # TinyURL API indicates success with code 0
                return {"error": None, "short_link": result['data']['tiny_url']}
            else:
                return {"error": result['errors'][0]['message'], "short_link": None}
        except requests.exceptions.RequestException as e:
            return {"error": f"TinyURL API request failed: {e}", "short_link": None}

    def generate_qr_code(self, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO object
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str
