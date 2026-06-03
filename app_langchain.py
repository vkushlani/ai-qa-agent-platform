from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

#Loand LLM
llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

#Get user question
user_question = input("Enter your testing question: ")

#Resusable function to analyze release notes based on user question
def analyze_release_notes(release_notes):
    # Read Prompt Template
    with open("prompts/regression_prompt.txt", "r") as file:
        template = file.read()

    # create prompt Template
    prompt = PromptTemplate(
        input_variables=["release_notes","question"],
        template=template
    )

    # Generate final prompt
    final_prompt = prompt.format(
        release_notes=release_notes,
        question=user_question
    )

    # Invoke LLM
    response = llm.invoke(final_prompt)

    return response.content

#Read Release Notes
with open("docs/release_notes.txt", "r") as file:
    release_notes = file.read()
    
result = analyze_release_notes(release_notes)
#print(result)

with open("outputs/report.txt", "w") as file:
    file.write(result)

#print(response.content)

