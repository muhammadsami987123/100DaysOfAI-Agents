import uvicorn
from web_app import app
from config import Config

if __name__ == '__main__':
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)

