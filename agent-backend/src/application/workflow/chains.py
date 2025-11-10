from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq


from src.config import settings
from src.domain.prompt import ANSWER_QUERY_PROMPT

def get_chat_model(temperature: float = 0.7, model_name: str = settings.GROQ_LLM_MODEL) -> ChatGroq:
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=model_name,
        temperature=temperature,
    )



def get_answer_query_response_chain():
    model = get_chat_model()
    # model = model.bind_tools(tools)
    system_message = ANSWER_QUERY_PROMPT

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message.prompt),
            MessagesPlaceholder(variable_name="messages"),
        ],
        template_format="jinja2",
    )

    return prompt | model