import argparse
import sys
from web_app import app
from url_shortener_agent import URLShortenerAgent
import pyperclip
import os

def run_cli():
    parser = argparse.ArgumentParser(description="URL Shortener Bot CLI")
    parser.add_argument("--url", required=True, help="Long URL to shorten")
    parser.add_argument("--alias", help="Custom alias for the short URL (if supported by API)")
    parser.add_argument("--copy", action="store_true", help="Copy the short URL to clipboard")
    parser.add_argument("--qr", action="store_true", help="Generate a QR code for the short URL")
    parser.add_argument("--track", action="store_true", help="Mock tracking (API dependent)") # Mocked for now

    args = parser.parse_args()

    agent = URLShortenerAgent()
    result = agent.shorten_url(args.url, args.alias)

    if result['error']:
        print(f"Error: {result['error']}")
        sys.exit(1)

    short_link = result['short_link']
    print(f"Short Link: {short_link}")

    if args.qr:
        qr_code_base64 = agent.generate_qr_code(short_link)
        # In a real CLI, you might save this as a file or display it in a terminal if supported
        print("QR Code generated (Base64 encoded string - not displayed directly in CLI).")
        # For actual file saving in CLI:
        # qr_filename = f"qrcode_{os.path.basename(short_link).replace('/', '_')}.png"
        # with open(qr_filename, "wb") as f:
        #     f.write(base64.b64decode(qr_code_base64))
        # print(f"QR Code saved as {qr_filename}")

    if args.copy:
        try:
            pyperclip.copy(short_link)
            print("Copied to clipboard!")
        except pyperclip.PyperclipException:
            print("Failed to copy to clipboard (install xclip or xsel for Linux).")

    if args.track:
        print("Tracking usage clicks (mocked for this API).")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].startswith('--'):
        run_cli()
    else:
        app.run(debug=True)
