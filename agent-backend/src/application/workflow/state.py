from langgraph.graph import MessagesState
from typing import TypedDict, Literal, Any, Optional
from src.infrastructure.postgreDb import PostgreDb


class InputState(TypedDict):
    customer_email: str

class OutputState(TypedDict):
    response_email: str

class AgentState(TypedDict):
    customer_query: str  # Extracted query
    query_type: Literal["needs_data", "general"]
    sql_query_v1: str
    sql_output_v1: Optional[Any]
    sql_query_v2: str
    sql_output_v2: Optional[Any]
    refinement_attempts: int
    reflect_sql_feedback: str
    db_client: PostgreDb | None
    db_schema: str
    customer_email: str
    response_email: str