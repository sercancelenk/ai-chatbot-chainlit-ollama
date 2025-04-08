import chainlit as cl
import os
from dotenv import load_dotenv
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# New imports for the data layer
import chainlit.data as cl_data
# from custom_layer import CustomSQLAlchemyDataLayer
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from typing import Optional
from chainlit.chat_context import chat_context
from chainlit.types import ThreadDict


# Load environment variables
load_dotenv()

MODEL = ChatOllama(
    model="llama3:8b-instruct-q8_0",
    num_predict=4096,
    base_url="http://localhost:11434",
    )
PROMPT_TEMPLATE = ChatPromptTemplate(
    [
        ("system", "You are a helpful ai assistant."),
        ("user", """
         <message history>
         {message_history}
         </message history>
         
         User's question: {question}
         
         """),
    ]
)
PARSER = StrOutputParser()

# Set up the data layer
cl_data._data_layer = SQLAlchemyDataLayer(
    conninfo="postgresql+asyncpg://myuser:mypassword@localhost:5432/mydatabase"
)

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin",
            metadata={"role": "admin", "provider": "credentials"},
            id="admin_id"
        )
    elif (username, password) == ("volkan", "volkan"):
        return cl.User(
            identifier="volkan",
            metadata={"role": "admin", "provider": "credentials"},
            id="volkan_id"
        )
    else:
        return None


@cl.on_chat_start
async def start():
    user = cl.user_session.get("user")
    if not user:
        await cl.Message(content="Please log in to start a chat.").send()
        return

    await cl.Message(content="Hello, I'm Claude! How can I help you today?", author="Assistant").send()


@cl.on_message
async def main(message: cl.Message):
    user = cl.user_session.get("user")
    if not user:
        await cl.Message(content="User information not found. Please try logging in again.").send()
        return

    chain = PROMPT_TEMPLATE | MODEL | PARSER

    message_history = "\n".join([f"{m.author}: {m.content}" for m in chat_context.get()])
    print(message_history)

    response = await chain.ainvoke(
        {
            "question": message.content,
            "message_history": message_history
        }
    )

    await cl.Message(content=response, author="Assistant").send()


@cl.on_chat_resume
async def resume(thread: ThreadDict):
    pass


