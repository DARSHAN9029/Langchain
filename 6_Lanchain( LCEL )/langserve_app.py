#LangServe helps developers deploy LangChain runnables and chains as a REST API.
#This library is integrated with FastAPI and uses pydantic for data validation.

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langserve import add_routes
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)


#create prompt template
generic_prompt_temp="Transalte the following into {language}"
prompt_template=ChatPromptTemplate.from_messages(
    [("system",generic_prompt_temp),
    ("user","{text}")]
)

parser=StrOutputParser()

#create chain 
chain=prompt_template|model|parser

#App definition
app=FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server using Langchain runnable interfaces"
)

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)