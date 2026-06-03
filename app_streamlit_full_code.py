import streamlit as st
from dotenv import load_dotenv
from langchain_openai import (ChatOpenAI,OpenAIEmbeddings)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.2
)

# Streamlit UI
st.title("AI Testing Agent")

st.markdown(
    "Upload release notes and ask QA-related questions."
)

uploaded_file = st.file_uploader(
    "Upload Release Notes",
    type=["txt"]
)

question = st.text_input(
    "Enter your question:"
)

if uploaded_file and question:

    # Read uploaded file
    content = uploaded_file.read().decode("utf-8")

    # Convert to document
    documents = [Document(page_content=content)]

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    # Create embeddings
    embedding_model = OpenAIEmbeddings()

    # Create vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    # Retrieve relevant chunks
    results = vectorstore.similarity_search(question)

    retrieved_context = "\n".join(
        [r.page_content for r in results]
    )

    # Final prompt
    prompt = f"""
    You are a senior QA architect.

    Use the retrieved context below
    to answer the user's question.

    Context:
    {retrieved_context}

    Question:
    {question}
    """

    with st.spinner("Analyzing release notes..."):

        response = llm.invoke(prompt)

st.subheader("AI Response")

st.write(response.content)