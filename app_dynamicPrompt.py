from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

with open("docs/release_notes.txt", "r") as file:
    release_notes = file.read() 
    
    prompt = f"""
    Analyze the following release notes.

Identify:
1. High-risk modules
2. Regression testing recommendations
3. Critical testing focus areas

Release Notes:
{release_notes}  
    """
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[
            {
            "role": "system",
            "content": "You are a senior QA architect."
        },
            {"role": "user",
             "content": prompt
            }
        ]
    )

    print(response.choices[0].message.content)

except Exception as e:
    print("Error occurred while generating response: " ,e)