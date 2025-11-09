from src.application.workflow.chains import get_answer_query_response_chain



async def answer_query(state):
    # Implementation for answering a customer query

    chain = get_answer_query_response_chain()

    response = await chain.ainvoke(
        {
            "messages": state["messages"],
            "user_query": state["user_query"]
        }
    )
    return {"messages": response}
