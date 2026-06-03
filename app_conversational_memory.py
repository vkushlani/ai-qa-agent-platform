import streamlit as st

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.2
)

st.title("AI Testing Agent")

# Initialize memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input(
    "Ask your testing question:"
)

if question:

    # Save user question
    st.session_state.chat_history.append(
        f"User: {question}"
    )

    # Build conversation context
    history = "\n".join(
        st.session_state.chat_history
    )

    prompt = f"""
    You are a senior QA architect.

    Use the conversation history below
    to answer the latest question.

    Conversation History:
    {history}
    """

    response = llm.invoke(prompt)

    answer = response.content

    # Save AI response
    st.session_state.chat_history.append(
        f"AI: {answer}"
    )

# Display history
st.subheader("Conversation History")

for message in st.session_state.chat_history:
    st.write(message)