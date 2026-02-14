import os
from dotenv import load_dotenv
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser # default output parser whenever your llm model gives any kinda response

load_dotenv() 

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

if not GOOGLE_API_KEY or not LANGCHAIN_API_KEY:
    st.error("Please set GOOGLE_API_KEY and LANGCHAIN_API_KEY in your .env file")
    st.stop()


# tracing to capture all monitor results 
os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY
#langsmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true" #do tracing
os.environ["LANGCHAIN_API_KEY"]=LANGCHAIN_API_KEY #help us to know where entire tracing results needs to be store

#streamlit framework
st.title("Langchain Demo with Google_AI")
input_text=st.text_input("Search Anything you want")

# prompt template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to the user queries"),
        ("user","question:{question}")
    ]
)


#google ai llm
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",  # Fast and latest
    google_api_key=GOOGLE_API_KEY
)

output_parser=StrOutputParser()
chain=prompt|llm|output_parser

#prompt ko llm se integrate kiya phir output diya 
if input_text:
    with st.spinner("Generating response..."):
        try:
            response = chain.invoke({"question": input_text})
            st.subheader("Response:")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
#to run this streamlit run app.py
