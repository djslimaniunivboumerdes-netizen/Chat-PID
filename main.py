from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import os
import shutil

app = FastAPI(title="Chat-PID API")

# Setup directories
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    # Minimal HTML response to prove the server is running
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Chat-PID Live</title></head>
    <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
        <h1 style="color: green;">Chat-PID is Running!</h1>
        <p>The backend server is active.</p>
    </body>
    </html>
    """

@app.post("/api/v1/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{project_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "status": "Uploaded", "project_id": project_id}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
