from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

import json

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

with open("docs/release_notes.txt", "r") as file:
    release_notes = file.read() 
    
    prompt = f"""
    Analyze the following release notes.
    
    Return output in JSON format:
    
{{
  "high_risk_modules": [],
  "recommended_tests": [],
  "critical_focus_areas": []
}}

Release Notes:
{release_notes}  
    """
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user",
         "content": prompt
        }
    ]
)

output = response.choices[0].message.content

print(output)