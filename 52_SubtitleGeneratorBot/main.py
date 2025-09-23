from __future__ import annotations

import uvicorn
from config import CONFIG
from server import create_app


def main():
	app = create_app()
	uvicorn.run(app, host=CONFIG.host, port=CONFIG.port, log_level="info")


if __name__ == "__main__":
	main()
