import uvicorn
from web_app import app
from config import Config
import os

if __name__ == '__main__':
    # Ensure the upload directory exists
    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
