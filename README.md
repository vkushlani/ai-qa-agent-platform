# AI-Powered QA Agent Platform

This is a Streamlit-based AI QA assistant that uses LLMs, RAG, memory, and specialized QA agents to support software testing activities.

## Features

- Test case generation
- Defect analysis
- Requirement traceability
- Regression risk assessment
- Mock automation execution
- Multi-document upload
- Document summarization
- Document comparison
- Persistent memory
- Vector memory
- Multi-agent coordination

## Tech Stack

- Python
- Streamlit
- LangChain
- OpenAI
- ChromaDB
- Pandas
- PDF / Word / Excel parsing

## Architecture

User Prompt  
→ Router  
→ Coordinator Agent  
→ Specialized QA Agents  
→ RAG / Memory  
→ Response

## Supported Agents

- Test Case Agent
- Defect Analysis Agent
- Requirement Traceability Agent
- Regression Risk Agent
- Automation Agent
- Planning Agent

## Example Prompts

Generate test cases for login page

Analyze defect: Users cannot login after password reset

Create traceability matrix for checkout feature

Perform regression risk analysis for payment module

Run test for login page

Summarize uploaded documents

Compare uploaded documents

## Local Setup

```bash
pip install -r requirements.txt
streamlit run app.py