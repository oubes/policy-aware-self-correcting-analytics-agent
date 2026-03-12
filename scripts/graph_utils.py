from pathlib import Path
from langgraph.graph import StateGraph

def save_graph_image(graph: StateGraph, filename: str = "graph_flow.png"):
    try:
        project_root = Path(__file__).resolve().parents[2]
        save_dir = project_root / "app" / "data"
        save_dir.mkdir(parents=True, exist_ok=True)
        full_path = save_dir / filename
        img_data = graph.get_graph().draw_mermaid_png()  # type: ignore
        with open(full_path, "wb") as f:
            f.write(img_data)
    except Exception:
        pass