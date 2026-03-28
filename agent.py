import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent

def get_agent(df):
    # Works both locally and on Streamlit Cloud
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0
    )
    
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True,
        agent_type="tool-calling"
    )
    
    return agent
