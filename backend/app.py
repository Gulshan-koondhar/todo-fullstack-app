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

    # Get port from environment variable (standard for Hugging Face Spaces)
    port = int(os.environ.get("PORT", 7860))
    # Get host from environment variable, default to 0.0.0.0 for external access
    host = os.environ.get("HOST", "0.0.0.0")

    print(f"Starting server on {host}:{port}")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )