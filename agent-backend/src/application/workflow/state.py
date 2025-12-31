from langgraph.graph import MessagesState
from typing import TypedDict, Literal, Any, Optional
from src.infrastructure.postgreDb import PostgreDb


class InputState(TypedDict):
    customer_email: str

class OutputState(TypedDict):
    response_email: str

class AgentState(TypedDict):
    customer_query: str 
    query_type: Literal["needs_data", "general"]
    current_date: Optional[str]
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

def state_to_str(state: AgentState) -> str:
    return f"""
AgentState(
    customer_query={state["customer_query"]},
    query_type={state["query_type"]},
    sql_query_v1={state["sql_query_v1"]},
    sql_output_v1={state["sql_output_v1"]},
    sql_query_v2={state["sql_query_v2"]},
    sql_output_v2={state["sql_output_v2"]},
    refinement_attempts={state["refinement_attempts"]},
    reflect_sql_feedback={state["reflect_sql_feedback"]},
    db_client={state["db_client"]},
    db_schema={state["db_schema"]},
    customer_email={state["customer_email"]},
    response_email={state["response_email"]}
)
    """
