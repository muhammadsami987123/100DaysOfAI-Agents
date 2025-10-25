from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import generate_image, download_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your Next.js frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_image.router)
app.include_router(download_image.router)

@app.get("/")
async def root():
    return {"message": "ImageDownloaderBot Backend is running!"}
