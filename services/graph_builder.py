
# This module would use the NetworkX library
def build_equipment_network(project_id):
    # MOCK DATA for React Flow or Vis.js visualization
    return {
        "nodes": [
            {"id": "T-100", "label": "Storage Tank", "type": "tank", "style": "bg-blue-400"},
            {"id": "P-101A", "label": "Pump A", "type": "pump", "style": "bg-red-400"},
            {"id": "E-201", "label": "Exchanger", "type": "exchanger", "style": "bg-green-400"}
        ],
        "edges": [
            {"id": "e1-2", "source": "T-100", "target": "P-101A", "label": "Line 1001"},
            {"id": "e2-3", "source": "P-101A", "target": "E-201", "label": "Line 1002"}
        ]
    }
