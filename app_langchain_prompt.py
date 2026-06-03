from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

#Loand LLM
llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

def analyze_risk_notes(risk_notes):
    # Read Prompt Template
    with open("prompts/risk_analysis_prompt.txt", "r") as file:
        template = file.read()

    # create prompt Template
    prompt = PromptTemplate(
        input_variables=["risk_notes"],
        template=template
    )

    # Generate final prompt
    final_prompt = prompt.format(risk_notes=risk_notes)
    
    # Invoke LLM
    response = llm.invoke(final_prompt)

    return response.content

#Read Release Notes
with open("docs/risk_notes.txt", "r") as file:
    risk_notes = file.read()
    
result = analyze_risk_notes(risk_notes)
print(result)

with open("outputs/report.txt", "w") as file:
    file.write(result)

#print(response.content)