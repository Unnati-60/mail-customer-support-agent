import json
from src.application.workflow.chains import build_chain
from src.prompt import EXTRACT_CLASSIFY_QUERY_PROMPT, SQL_PROMPT, REFLECT_SQL_PROMPT, EMAIL_PROMPT
from src.infrastructure.postgreDb import PostgreDb


async def extract_classify_query(state):

    chain = build_chain(system_prompt=EXTRACT_CLASSIFY_QUERY_PROMPT)

    response = await chain.ainvoke(
        {
            "customer_email": state["customer_email"],
            "current_date": state.get("current_date")
        }
    )

    response= json.loads(response.content.strip().removeprefix("```json").removesuffix("```").strip())

    return  {
            "customer_query": response['query'],
            "query_type": response['category']
        }


async def generate_SQL(state):
    if state["db_client"] is None:
        state["db_client"] = PostgreDb()
    
    schema =  state["db_client"].get_schema()

    chain = build_chain(system_prompt=SQL_PROMPT)

    response = await chain.ainvoke(
        {
            "schema": schema,
            "question": state["customer_query"]
        }
    )

    response= response.content.strip()

    # execute the SQL

    sql_output = state["db_client"].execute_sql(response)

    return  {"db_schema": schema,"sql_query_v1": response,"sql_output_v1": sql_output, "refinement_attempts": 0}


async def reflect_on_SQL(state):

    chain = build_chain(system_prompt=REFLECT_SQL_PROMPT)

    response = await chain.ainvoke(
        {
            "customer_query": state["customer_query"],
            "sql_query_v1": state["sql_query_v1"],
            "sql_output_v1": state["sql_output_v1"],
            "schema": state["db_schema"]
        }
    )
    response= json.loads(response.content.strip().removeprefix("```json").removesuffix("```").strip())

    sql_v2 = response.get("refined_sql")
    feedback = response.get("feedback")

    # execute the refined SQL
    if state["db_client"] is None:
        state["db_client"] = PostgreDb()
    
    database_client = state["db_client"]

    sql_output = database_client.execute_sql(sql_v2)
    

    return  {"sql_query_v2": sql_v2,"sql_output_v2": sql_output, "reflect_sql_feedback": feedback, "refinement_attempts": state.get("refinement_attempts", 0) + 1}


async def generate_response_email(state):

    chain = build_chain(system_prompt=EMAIL_PROMPT)

    response = await chain.ainvoke(
        {
            "customer_email": state["customer_email"],
            "customer_query": state["customer_query"],
            "retrieved_data": state.get("sql_output_v2", ""),
        }
    )

    response= response.content.strip()


    return  {"response_email": response}

