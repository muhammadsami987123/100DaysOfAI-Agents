"""Small runner for local development."""
import os

if __name__ == "__main__":
    # Use import string when reload=True so uvicorn can restart the process correctly.
    # This avoids the warning: "You must pass the application as an import string to enable 'reload' or 'workers'."
    import uvicorn
    port = int(os.getenv("PORT", 9000))
    # pass the app as import string if reload is enabled
    uvicorn.run("web_app:app", host="0.0.0.0", port=port, reload=True)
