# LLM CONFIGURATION 
#PROMPTS
#CHAINS
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import uvicorn
import os
load_dotenv() 
app=FastAPI()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# tracing to capture all monitor results 
os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",  # Fast and latest
    google_api_key=GOOGLE_API_KEY
)

prompt1=ChatPromptTemplate.from_template("Write me an essay about {topic} around 100 words")
prompt2=ChatPromptTemplate.from_template("Write me an poem about {topic} around 100 words")

add_routes(
    app,
    llm,
    path="/gemini"
)
# In automatic routing using add_routes():
# - We do NOT need to specify HTTP methods (GET, POST, etc.)
# - We do NOT need to specify status codes (200, 201, etc.)
# - Routes are automatically created by LangServe
# - It automatically exposes POST endpoints for the LLM/chain
# - Response returned will always be the LLM output
# - We cannot directly send additional/custom responses from this route

# Traditional FastAPI routing method:

# @app.post("/gemini", status_code=200)
# def chat_with_gemini(user_input: str):
#     response = llm.invoke(user_input)
#     return {
#         "message": "Response generated successfully",
#         "output": response
#     }

# In traditional routing:
# - We manually define HTTP methods (@app.get, @app.post etc.)
# - We manually set status codes
# - We can customize response format
# - We can add extra messages or logic
# - Full control over API behavior

#User input → prompt template → Gemini LLM → response
add_routes(
    app,
    prompt1|llm, #| means chaining
    path="/essay"
)

add_routes(
    app,
    prompt2|llm,
    path="/poem"
)

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)