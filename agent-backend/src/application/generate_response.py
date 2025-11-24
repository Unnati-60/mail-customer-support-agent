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
                    "db_client": None,
                },
                config=config
            )
        last_message = output_state["response_email"]
        return last_message, AgentState(**output_state)
    except Exception as e:
        raise RuntimeError(f"Error running conversation workflow: {str(e)}") from e


# def __format_messages(
#     messages: Union[str, list[dict[str, Any]]],
# ) -> list[Union[HumanMessage, AIMessage]]:
#     """Convert various message formats to a list of LangChain message objects.

#     Args:
#         messages: Can be one of:
#             - A single string message
#             - A list of string messages
#             - A list of dictionaries with 'role' and 'content' keys

#     Returns:
#         List[Union[HumanMessage, AIMessage]]: A list of LangChain message objects
#     """

#     if isinstance(messages, str):
#         return [HumanMessage(content=messages)]

#     if isinstance(messages, list):
#         if not messages:
#             return []

#         if (
#             isinstance(messages[0], dict)
#             and "role" in messages[0]
#             and "content" in messages[0]
#         ):
#             result = []
#             for msg in messages:
#                 if msg["role"] == "user":
#                     result.append(HumanMessage(content=msg["content"]))
#                 elif msg["role"] == "assistant":
#                     result.append(AIMessage(content=msg["content"]))
#             return result

#         return [HumanMessage(content=message) for message in messages]

#     return []
