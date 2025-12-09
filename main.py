
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from services import pdf_processor, graph_builder, hazop_ai
import os
import shutil # Added shutil import for file handling

app = FastAPI(title="Chat-PID API", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup directories
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("outputs", exist_ok=True) # For highlighted PDFs

# --- API Endpoints (Routes) ---

@app.post("/api/v1/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile = File(...)):
    # Save the file (e.g., PDF)
    file_path = f"{UPLOAD_DIR}/{project_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "status": "Uploaded", "project_id": project_id}

@app.get("/api/v1/inventory/{project_id}")
async def get_inventory(project_id: str):
    data = pdf_processor.extract_inventory(project_id)
    return data

@app.get("/api/v1/network/{project_id}")
async def get_network(project_id: str):
    data = graph_builder.build_equipment_network(project_id)
    return data

@app.get("/api/v1/hazop/analyze")
async def run_hazop_analysis(tag: str):
    suggestions = hazop_ai.generate_hazop_suggestions(tag)
    return {"tag": tag, "analysis": suggestions}

# --- Frontend & Static Files ---

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_ui():
    return FileResponse("static/index.html")
