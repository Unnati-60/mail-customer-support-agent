import uuid
from typing import Any, AsyncGenerator, Union

from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage
# from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver
from opik.integrations.langchain import OpikTracer

from src.application.workflow.graph import (
    create_workflow_graph
)
from src.application.workflow.state import AgentState
from src.config import settings
from datetime import date


async def get_response(
    customer_email: str,
) -> tuple[str, AgentState]:
    
    graph_builder = create_workflow_graph()

    try:
        graph = graph_builder.compile()
        opik_tracer = OpikTracer(graph=graph.get_graph(xray=True))

        config =  {
                "configurable": {"thread_id": uuid.uuid4()},
                "callbacks": [opik_tracer],
            }

        output_state = await graph.ainvoke(
                input={
                    "customer_email": customer_email,
                    "current_date": str(date.today().isoformat()),
                    "db_client": None,
                },
                config=config
            )
        response_email = output_state["response_email"]
        return response_email, AgentState(**output_state)
    except Exception as e:
        raise RuntimeError(f"Error running conversation workflow: {str(e)}") from e
