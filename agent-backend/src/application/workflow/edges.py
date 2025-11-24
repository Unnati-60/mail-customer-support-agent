from typing_extensions import Literal

from src.application.workflow.state import AgentState



def route_sql(
    state: AgentState,
) -> Literal["generate_response_email", "generate_SQL"]:
    
    if state["query_type"] == "needs_db":
        return "generate_SQL"
    else:
        return "generate_response_email"
