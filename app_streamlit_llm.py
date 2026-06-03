import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm=ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.2
)

st.title("AI Testing Agent")

st.markdown(
    "Upload release notes and ask QA-related questions."
)

#st.subheader("Upload Release Notes")

uploaded_file = st.file_uploader(
    "Upload Release Notes",
    type=["txt"]
)

question = st.text_input(
   "Enter your question:"
)

if uploaded_file and question:

    release_notes = uploaded_file.read().decode("utf-8")

    prompt = f"""
    You are a senior QA architect.

    Analyze the following release notes
    and answer the user's question.

    Release Notes:
    {release_notes}

    Question:
    {question}
    """
    response = llm.invoke(prompt)
    

    st.subheader("AI Response")

    st.write(response.content)

# with st.spinner("Analyzing release notes..."):



