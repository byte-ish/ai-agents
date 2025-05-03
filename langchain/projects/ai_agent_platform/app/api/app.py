from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agents.agent_factory import get_selected_agent
from app.utils.logger import logger
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Agent Platform",
    description="AI Code Assistant Agent API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

class AgentRequest(BaseModel):
    input: str

class AgentResponse(BaseModel):
    result: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/agent", response_model=AgentResponse)
async def invoke_agent(request: AgentRequest):
    logger.info(f"Received agent request: {request.input}")

    try:
        agent = get_selected_agent()

        result = await agent.ainvoke({"input": request.input})

        return AgentResponse(result=result["output"] if isinstance(result, dict) else result)

    except Exception as e:
        logger.exception("Agent invocation failed.")
        raise HTTPException(status_code=500, detail=str(e))