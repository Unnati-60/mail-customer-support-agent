from src.application.generate_response import get_response
from pydantic import BaseModel
from opik.integrations.langchain import OpikTracer
from src.infrastructure.opik_utils import configure

import asyncio
class ChatMessage(BaseModel):
    message: str
    user_query: str 


async def main():

    chat_message = ChatMessage(
        message="",
        user_query="What is the return policy for online purchases?"
    )
    try:
        response, _ = await get_response(
                messages=chat_message.message,
                user_query=chat_message.user_query
            )
        print(f"Response: \n{response}")
    except Exception as e:
        print(f"Error: {str(e)}")
        opik_tracer = OpikTracer()
        opik_tracer.flush()
        return


if __name__ == "__main__":
    configure()
    asyncio.run(main())
