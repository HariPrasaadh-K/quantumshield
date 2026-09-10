"""
Cryptographic Dependency Graph Builder using NetworkX.
Generates React Flow nodes & edges directly from scan database assets and findings.
"""
import os
import networkx as nx
from typing import List, Dict, Any

def build_dependency_graph(project_name: str, assets: List[Any], dependencies: List[Any] = None) -> Dict[str, Any]:
    """
    Constructs a dependency graph from scan assets and dependencies.
    Returns React-Flow compatible nodes and edges structure.
    """
    G = nx.DiGraph()

    # 1. Add Root Project Node
    proj_node_id = f"proj-{project_name.lower().replace(' ', '-')}"
    G.add_node(proj_node_id, label=project_name, type="project", risk="Low", priority="P3")

    file_nodes = set()
    library_nodes = set()

    for asset in assets:
        # File Node
        rel_file = asset.file_path
        file_node_id = f"file-{rel_file.replace('/', '-').replace('.', '-')}"
        if file_node_id not in file_nodes:
            file_nodes.add(file_node_id)
            file_name = os.path.basename(rel_file)
            G.add_node(file_node_id, label=file_name, type="file", path=rel_file, risk="Low", priority="P3")
            G.add_edge(proj_node_id, file_node_id, relationship="CONTAINS", confidence=1.0, evidence="Project file hierarchy")

        # Asset Node
        asset_node_id = f"asset-{asset.id}"
        G.add_node(
            asset_node_id,
            label=f"{asset.algorithm} ({asset.crypto_purpose})",
            type="crypto_asset",
            algorithm=asset.algorithm,
            purpose=asset.crypto_purpose,
            risk=asset.risk_type,
            risk_score=asset.risk_score,
            priority=asset.priority,
            file_path=asset.file_path,
            line_number=asset.line_number
        )
        G.add_edge(file_node_id, asset_node_id, relationship="USES", confidence=asset.purpose_confidence, evidence=f"Code at line {asset.line_number}")

        # Library Node if present
        if asset.library:
            lib_node_id = f"lib-{asset.library.lower().replace(' ', '-')}"
            if lib_node_id not in library_nodes:
                library_nodes.add(lib_node_id)
                G.add_node(lib_node_id, label=asset.library, type="library", risk="Low", priority="P3")
            G.add_edge(asset_node_id, lib_node_id, relationship="IMPORTS", confidence=0.9, evidence=f"Imported package {asset.library}")

    # Add custom dependencies if provided
    if dependencies:
        for dep in dependencies:
            s_id = f"asset-{dep.source_asset_id}"
            t_id = f"asset-{dep.target_asset_id}"
            if G.has_node(s_id) and G.has_node(t_id):
                G.add_edge(s_id, t_id, relationship=dep.relationship_type, confidence=dep.confidence, evidence=dep.evidence or "")

    # Format into React Flow structure
    nodes = []
    edges = []

    # Position layout using Graphviz/Spring or Grid hierarchy
    # Grid layout mapping for visual separation
    type_columns = {"project": 0, "file": 1, "crypto_asset": 2, "library": 3}
    column_counts = {"project": 0, "file": 0, "crypto_asset": 0, "library": 0}

    for node_id, data in G.nodes(data=True):
        ntype = data.get("type", "file")
        col = type_columns.get(ntype, 1)
        row = column_counts.get(ntype, 0)
        column_counts[ntype] = row + 1

        x_pos = col * 320 + 50
        y_pos = row * 130 + 50

        nodes.append({
            "id": node_id,
            "type": "custom",
            "position": {"x": x_pos, "y": y_pos},
            "data": {
                "id": node_id,
                "label": data.get("label", node_id),
                "type": ntype,
                "risk": data.get("risk", "Low"),
                "risk_score": data.get("risk_score", 0.0),
                "priority": data.get("priority", "P3"),
                "algorithm": data.get("algorithm", ""),
                "purpose": data.get("purpose", ""),
                "file_path": data.get("file_path", ""),
                "line_number": data.get("line_number", 1)
            }
        })

    edge_id_counter = 0
    for u, v, data in G.edges(data=True):
        edge_id_counter += 1
        edges.append({
            "id": f"edge-{edge_id_counter}",
            "source": u,
            "target": v,
            "label": data.get("relationship", "USES"),
            "animated": True if data.get("relationship") in ("USES", "DEPENDS_ON") else False,
            "data": {
                "relationship": data.get("relationship", "USES"),
                "confidence": data.get("confidence", 1.0),
                "evidence": data.get("evidence", "")
            }
        })

    return {
        "nodes": nodes,
        "edges": edges,
        "summary": {
            "total_nodes": len(nodes),
            "total_edges": len(edges)
        }
    }
