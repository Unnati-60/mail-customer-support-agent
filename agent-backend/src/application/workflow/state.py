from langgraph.graph import MessagesState


class CustomerState(MessagesState):
    """State class for the LangGraph workflow. It keeps track of the information necessary to maintain a coherent
    conversation between the Philosopher and the user.

    Attributes:
       
    """

    user_query: str
    


def state_to_str(state: CustomerState) -> str:

    return f"""
CustomerState(user_query={state["user_query"]})
        """
