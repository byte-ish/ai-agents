# app/api/app.py

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.agents.agent_factory import get_selected_agent
from app.utils.logger import logger
from fastapi.middleware.cors import CORSMiddleware
import uuid
from typing import Dict, Optional
import asyncio

app = FastAPI(
    title="AI Agent Platform",
    description="AI Code Assistant Agent API (Background Task version)",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# ----------------------------
# Task Storage (In-Memory)
# ----------------------------

tasks: Dict[str, Dict] = {}

# ----------------------------
# Models
# ----------------------------

class AgentRequest(BaseModel):
    input: str

class AgentResponse(BaseModel):
    task_id: str
    status: str

class AgentResultResponse(BaseModel):
    status: str
    result: Optional[str] = None


# ----------------------------
# Background Agent Runner
# ----------------------------

async def run_agent(task_id: str, user_input: str):
    logger.info(f"[AgentTask] Starting agent for task: {task_id}")

    agent = get_selected_agent()

    try:
        result = await agent.ainvoke({"input": user_input})

        # Save result
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["result"] = result["output"] if isinstance(result, dict) else result

        logger.info(f"[AgentTask] Completed task {task_id}")

    except Exception as e:
        logger.exception(f"[AgentTask] Failed task {task_id}")
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["result"] = str(e)


# ----------------------------
# API Endpoints
# ----------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/agent", response_model=AgentResponse)
async def invoke_agent(request: AgentRequest, background_tasks: BackgroundTasks):
    logger.info(f"Received agent request: {request.input}")

    # Generate task ID
    task_id = str(uuid.uuid4())

    # Add to task store
    tasks[task_id] = {
        "status": "processing",
        "result": None
    }

    # Start agent in background
    background_tasks.add_task(run_agent, task_id, request.input)

    return AgentResponse(task_id=task_id, status="received")


@app.get("/agent/{task_id}", response_model=AgentResultResponse)
async def get_agent_result(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasks[task_id]

    return AgentResultResponse(status=task["status"], result=task["result"])