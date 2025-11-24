from src.application.generate_response import get_response
from pydantic import BaseModel
from opik.integrations.langchain import OpikTracer
from src.infrastructure.opik_utils import configure

import asyncio
class ChatMessage(BaseModel):
    customer_email: str 

mail  = """
Hi SwiftCart Team,

I hope you’re doing well. I recently ordered an iPhone 14 and the order ID is 1. I received the confirmation message, but I just wanted to check on the shipping details. Could you please share the current status of my shipment and the expected delivery date?

Thanks a lot,
Amit Sharma
"""

async def main():


    chat_message = ChatMessage(
        customer_email=mail
    )
    try:
        response, _ = await get_response(
                customer_email=chat_message.customer_email
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
