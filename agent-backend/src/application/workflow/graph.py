from langgraph.graph import END, START, StateGraph

from src.application.workflow.state import CustomerState
from src.application.workflow.nodes import answer_query



def create_workflow_graph():
    graph_builder = StateGraph(CustomerState)
    graph_builder.add_node("answer_query", answer_query)
    graph_builder.add_edge(START, "answer_query")
    graph_builder.add_edge("answer_query", END)

    return graph_builder

# Compiled without a checkpointer. Used for LangGraph Studio
graph = create_workflow_graph().compile()