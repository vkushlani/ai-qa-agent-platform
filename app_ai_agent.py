import streamlit as st
from tools import (analyze_risk, generate_test_cases)
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import (
    initialize_agent,
    Tool,
    AgentType
)
load_dotenv()

#Initialize LLM
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.2
)

#Define tools
tools = [
    Tool( 
         name="RiskAnalyzer",
         func=analyze_risk,
         description="""
        Use this tool to analyze testing risks
        for software modules.
        """
     ),
    
    Tool(
    name="TestCaseGenerator",

    func=generate_test_cases,

    description="""
    Use this tool to generate
    software testing scenarios.
    """
)
]

#Create agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

#Streallit UI
st.title("AI Testing Agent")

question = st.text_input(
    "Enter your testing question:")

if question:

    response = agent.run(question)

    st.subheader("Agent Response")

    st.write(response)