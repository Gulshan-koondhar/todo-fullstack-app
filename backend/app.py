"""
Hugging Face Space Application Entry Point
This file is used by Hugging Face Spaces to run the application.
"""
from app.main import app

# This allows Hugging Face Spaces to run the application
# The application will be available on the port specified by the PORT environment variable
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 7860))
    host = os.environ.get("HOST", "0.0.0.0")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False
    )