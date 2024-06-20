
# main.py
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # React development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, Any]

class Edge(BaseModel):
    id: str
    source: str
    target: str
    type: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

def read_root():
    return {'Ping': 'Pong'}

@app.get('/pipelines/parse')
def parse_pipeline(pipeline: str = Form(...)):
    return {'status': 'parsed'}

def is_dag(nodes: List[Node], edges: List[Edge]) -> bool:
    graph = {node.id: [] for node in nodes}
    for edge in edges:
        graph[edge.source].append(edge.target)

    visited = set([])
    rec_stack = set([])

    def dfs(v):
        if v in rec_stack:
            return False
        if v in visited:
            return True
        
        visited.add(v)
        rec_stack.add(v)

        for neighbor in graph[v]:
            if not dfs(neighbor):
                return False
        
        rec_stack.remove(v)
        return True

    for node in nodes:
        if node.id not in visited:
            if not dfs(node.id):
                return False
    
    return True

@app.post("/pipeline/parse")
async def parse_pipeline(pipeline: Pipeline):
    # Process nodes and edges here
    return {"num_nodes": len(pipeline.nodes), "num_edges": len(pipeline.edges), "is_dag": is_dag(pipeline.nodes, pipeline.edges)}

