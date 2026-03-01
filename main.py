import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools import query_monday_board
from prompts import SYSTEM_PROMPT

load_dotenv()

def initialize_agent():
    llm = ChatGroq(
        model="openai/gpt-oss-120b", 
        temperature=0, 
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    tools = [query_monday_board]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True
    )