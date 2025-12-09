
def extract_inventory(project_id):
    # MOCK LOGIC: In a real app, this uses PyMuPDF or OCR
    print(f"Processing P&ID for project: {project_id}")
    return {
        "pipelines": [
            {"line_no": "8-L-1001-CS", "diameter": "8"", "fluid": "LNG", "from": "T-100", "to": "P-101A", "hazop_risk": "Low Pressure"},
            {"line_no": "6-L-1002-CS", "diameter": "6"", "fluid": "Steam", "from": "P-101A", "to": "E-201", "hazop_risk": "High Temperature"}
        ],
        "equipment": [
            {"tag": "P-101A", "type": "Pump", "spec": "API 610"},
            {"tag": "E-201", "type": "Heat Exchanger", "spec": "TEMA"}
        ]
    }

def create_highlighted_pdf(project_id, size):
    print(f"Generating highlighted PDF for size: {size}")
    return "outputs/highlighted_demo.pdf" 
