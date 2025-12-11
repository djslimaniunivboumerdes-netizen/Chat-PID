from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
import os
import shutil

# --- Safely Import Services ---
# This prevents the app from crashing if a service file is missing or has a syntax error
try:
    from services import pdf_processor, graph_builder, hazop_ai
    SERVICES_AVAILABLE = True
except ImportError as e:
    print(f"WARNING: Service imports failed: {e}")
    SERVICES_AVAILABLE = False

app = FastAPI(title="Chat-PID API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Setup Directories (Auto-Create to prevent crashes) ---
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
STATIC_DIR = "static"

for directory in [UPLOAD_DIR, OUTPUT_DIR, STATIC_DIR]:
    os.makedirs(directory, exist_ok=True)

# --- Mount Static Files ---
# We check if index.html exists to avoid 404 errors on the homepage
if not os.path.exists(os.path.join(STATIC_DIR, "index.html")):
    # Create a dummy index.html if it's missing so the app doesn't look broken
    with open(os.path.join(STATIC_DIR, "index.html"), "w") as f:
        f.write("<h1>Chat-PID is Running!</h1><p>Please upload your frontend files to the static folder.</p>")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- API Endpoints ---

@app.post("/api/v1/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{project_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "status": "Uploaded", "project_id": project_id}

@app.get("/api/v1/inventory/{project_id}")
async def get_inventory(project_id: str):
    if SERVICES_AVAILABLE:
        return pdf_processor.extract_inventory(project_id)
    return {"error": "Services module not loaded"}

@app.get("/api/v1/network/{project_id}")
async def get_network(project_id: str):
    if SERVICES_AVAILABLE:
        return graph_builder.build_equipment_network(project_id)
    return {"error": "Services module not loaded"}

@app.get("/api/v1/hazop/analyze")
async def run_hazop_analysis(tag: str):
    if SERVICES_AVAILABLE:
        suggestions = hazop_ai.generate_hazop_suggestions(tag)
        return {"tag": tag, "analysis": suggestions}
    return {"tag": tag, "analysis": ["Error: AI Service unavailable"]}

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_ui():
    return FileResponse(f"{STATIC_DIR}/index.html")

# Health check for Render
@app.get("/health")
async def health_check():
    return {"status": "active"}
