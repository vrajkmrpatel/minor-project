from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGSMITH_API_KEY")

if not OPENAI_API_KEY:
    st.error("Missing OpenAI API Key! Please check your .env file.")
else:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_TRACING_V2"] = "true"

    # Creating chatbot prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Please provide responses to user queries."),
        ("user", "Question: {question}")
    ])

    # Streamlit UI
    st.title("LangChain Chatbot with OpenAI API")
    input_text = st.text_input("Ask me anything!")

    # OpenAI LLM and output parser
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    output_parser = StrOutputParser()

    # LangChain pipeline
    chain = prompt | llm | output_parser

    if input_text:
        with st.spinner("Thinking..."):
            response = chain.invoke({'question': input_text})
            st.chat_message("assistant").write(response)
