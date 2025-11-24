from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from opik.integrations.langchain import OpikTracer
from pydantic import BaseModel

from src.application.generate_response import get_response
from .opik_utils import configure

configure()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events for the API."""
    # Startup code (if any) goes here
    yield
    # Shutdown code goes here
    opik_tracer = OpikTracer()
    opik_tracer.flush()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],            
)

class ChatMessage(BaseModel):
    customer_mail: str

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        response, _ = await get_response(
            customer_email=chat_message.customer_mail
        )
        return {"response": response}
    except Exception as e:
        opik_tracer = OpikTracer()
        opik_tracer.flush()
        raise HTTPException(status_code=500, detail=str(e)) 


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)