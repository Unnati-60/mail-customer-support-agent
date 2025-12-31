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

# Extract query prompt
_EXTRACT_CLASSIFY_QUERY_PROMPT = """
You are a customer support assistant. Analyze the customer's email and extract the query & classify it:

1. Extract "query": the core question or request in one sentence along with relevant details.
2. "category": choose one:
   - "needs_db" → requires checking database records, order status, invoices, account info, history, transactions, profile details, etc.
   - "general" → can be answered without any data lookup.
- today's date is {{current_date}}.
- date must be mentioned in format YYYY-MM-DD.
Return a JSON object: {"query": "...", "category": "..."}.
Only output JSON.

Customer Email: {{customer_email}}

"""
EXTRACT_CLASSIFY_QUERY_PROMPT = Prompt(
    name="extract_classify_query_prompt",    
    prompt=_EXTRACT_CLASSIFY_QUERY_PROMPT,
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
    {{customer_query}}

    Original SQL:
    {{sql_query_v1}}

    SQL Output:
    {{sql_output_v1}}

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

# Write email prompt
_EMAIL_PROMPT = """       
You are a helpful customer support agent. Write a professional, friendly email response to the customer.  
Make sure to address the customer's original query and incorporate any relevant data retrieved from the database.

Original customer email:
{{customer_email}}

customer query:
{{customer_query}}

Retrieved Data from Database:
{{retrieved_data}}
"""
EMAIL_PROMPT = Prompt(
    name="email_prompt",
    prompt=_EMAIL_PROMPT,
)


# --- Evaluation ---
_SQL_EVALUATION_PROMPT = """
    You are an expert SQL evaluator.

    Your task is to evaluate whether a GENERATED_SQL correctly answers the USER_QUESTION,
    using EXPECTED_SQL and EXPECTED_SQL_OUTPUT as reference.

    Focus on semantic correctness, not exact SQL string matching.

    USER_QUESTION:
    {user_query}

    EXPECTED_SQL:
    {expected_sql}

    EXPECTED_SQL_OUTPUT:
    {expected_sql_output}

    GENERATED_SQL:
    {generated_sql}

    GENERATED_SQL_OUTPUT:
    {generated_sql_output}

    Evaluation Criteria:
    1. Does the GENERATED_SQL retrieve the correct data needed to answer the USER_QUESTION?
    2. Is the GENERATED_SQL semantically equivalent to EXPECTED_SQL?
    3. Does the GENERATED_SQL_OUTPUT match or logically align with EXPECTED_SQL_OUTPUT?
    4. Are all necessary joins, filters, and conditions correctly applied?
    5. If no records exist, does the query correctly infer the answer from related tables?

    Scoring Rules:
    - Score should be between 0 and 1.
    - Score = 1.0 → Fully correct, answers the question completely.
    - Score = 0.5 → Partially correct, retrieves some but not all required data.
    - Score = 0.0 → Incorrect, irrelevant, or misleading result.

    If GENERATED_SQL_OUTPUT is empty but EXPECTED_SQL_OUTPUT is non-empty → score = 0.0
    If both outputs are empty and logically correct → score = 1.0

    Output Format (STRICT JSON ONLY):
    {
    "score": <float between 0 and 1>,
    "verdict": "<correct | partially_correct | incorrect>",
    "reasoning": "<short explanation>"
    }

"""

SQL_EVALUATION_PROMPT = Prompt(
    name="sql_evaluation_prompt",  
    prompt=_SQL_EVALUATION_PROMPT,
)