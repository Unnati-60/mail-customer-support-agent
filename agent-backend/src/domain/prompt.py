# verify query (extract, answer q)
# write sql
# reflect on sql
# write mail
# reflect on mail

import opik
import logging

class Prompt:
    def __init__(self, name: str, prompt: str):
        self.name = name

        try:
            self.__prompt = opik.Prompt(name=name, prompt=prompt)
        except Exception as e:
            logging.warning(
                "Can't use Opik to version the prompt (probably due to missing or invalid credentials). Falling back to local prompt. The prompt is not versioned, but it's still usable: {e}"
            )
            self.__prompt = prompt
    
    @property                      # # creates a safe, read-only attribute with extra logic
    def prompt(self) -> str:
        if isinstance(self.__prompt, opik.Prompt):
            return self.__prompt.prompt
        else:
            return self.__prompt
    
    # give string representation of object (whenerver printed print(obj) or converted to string str(obj))
    def __str__(self) -> str:
        return self.prompt
    def __repr__(self) -> str:
        return self.__str__()
    

# ===== PROMPTS =====

# Answer query prompt
_ANSWER_QUERY_PROMPT = """
You are an expert customer support agent. 
- Given user query, write a email response to the user's question.
- Use the provided tools to gather any necessary information to answer the user's question.

User Query: {{user_query}}
"""

ANSWER_QUERY_PROMPT = Prompt(
    name="  answer_query_prompt",
    prompt=_ANSWER_QUERY_PROMPT,
)

# write sql prompt
_SQL_PROMPT = """
    You are a SQL assistant. Given the schema and the user's question, write a SQL query for SQLite.

    Schema:
    {{schema}}

    User question:
    {{question}}

    Respond with the SQL only.
"""

SQL_PROMPT = Prompt(
    name="sql_prompt",  
    prompt=_SQL_PROMPT,
)

# Reflect on SQL prompt
_REFLECT_SQL_PROMPT = """
You are a SQL reviewer and refiner.

    User asked:
    {{question}}

    Original SQL:
    {{sql_query}}

    SQL Output:
    {{sql_output}}

    Table Schema:
    {{schema}}

    Step 1: Briefly evaluate if the SQL output answers the user's question.
    Step 2: If the SQL could be improved, provide a refined SQL query.
    If the original SQL is already correct, return it unchanged.

    Return a strict JSON object with two fields:
    - "feedback": brief evaluation and suggestions
    - "refined_sql": the final SQL to run    
"""
REFLECT_SQL_PROMPT = Prompt(
    name="reflect_sql_prompt",
    prompt=_REFLECT_SQL_PROMPT,
)

# # Write email prompt
# _EMAIL_PROMPT = """       
# You are an expert customer support agent. Given the following user query and the answer retrieved from the database, write a professional and empathetic email response to the user's question.
# User Query: {user_query}        
# Answer from Database: {db_answer}      
# """
# EMAIL_PROMPT = Prompt(
#     name="email_prompt",
#     prompt=_EMAIL_PROMPT,
# )


# --- Evaluation ---
