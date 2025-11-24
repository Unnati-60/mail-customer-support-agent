from langgraph.graph import END, START, StateGraph

from src.application.workflow.state import AgentState
from src.application.workflow.nodes import extract_classify_query, generate_SQL, reflect_on_SQL, generate_response_email
from src.application.workflow.edges import route_sql



def create_workflow_graph():
    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("extract_classify_query", extract_classify_query)
    graph_builder.add_node("generate_SQL", generate_SQL)
    graph_builder.add_node("reflect_on_SQL", reflect_on_SQL)
    graph_builder.add_node("generate_response_email", generate_response_email)


    graph_builder.add_edge(START, "extract_classify_query")
    
    graph_builder.add_conditional_edges(
        "extract_classify_query",
        route_sql,
        {
            "generate_SQL": "generate_SQL",
            "generate_response_email": "generate_response_email",
        },
    )
    graph_builder.add_edge("generate_SQL", "reflect_on_SQL")
    graph_builder.add_edge("reflect_on_SQL", "generate_response_email")
    graph_builder.add_edge("generate_response_email", END)

    return graph_builder

# Compiled without a checkpointer. Used for LangGraph Studio
graph = create_workflow_graph().compile()
