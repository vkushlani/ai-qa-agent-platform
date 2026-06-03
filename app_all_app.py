import streamlit as st

from dotenv import load_dotenv

from langchain_openai import (
    ChatOpenAI,
    OpenAIEmbeddings
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma

from langchain_core.documents import Document

from app_router import classify_question

# ======================================================
# LOAD ENV VARIABLES
# ======================================================

load_dotenv()

# ======================================================
# INITIALIZE LLM
# ======================================================

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.2
)

# ======================================================
# STREAMLIT PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AI Testing Agent",
    layout="wide"
)

# ======================================================
# UI HEADER
# ======================================================

st.title("AI Testing Agent")

st.markdown("""
### Features
- Multi-document upload
- RAG-based semantic search
- Document comparison
- Conversation memory
- AI-powered QA assistant
""")

# ======================================================
# SESSION MEMORY
# ======================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ======================================================
# FILE UPLOAD
# ======================================================

uploaded_files = st.file_uploader(
    "Upload Documents",
    type=["txt"],
    accept_multiple_files=True
)

# ======================================================
# USER QUESTION
# ======================================================

question = st.text_input(
    "Ask your question:"
)



# ======================================================
# MAIN EXECUTION
# ======================================================

if uploaded_files and question:

    

    all_documents = []

    uploaded_document_names = []

   

    # ==================================================
    # READ ALL DOCUMENTS
    # ==================================================

    for uploaded_file in uploaded_files:

        file_name = uploaded_file.name

        uploaded_document_names.append(file_name)

        content = uploaded_file.read().decode("utf-8")


        all_documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": file_name
                }
            )
        )

    # ==================================================
    # REMOVE DUPLICATES
    # ==================================================

    unique_documents = list(
        set(uploaded_document_names)
    )

    # ==================================================
    # SPECIAL HANDLING:
    # DOCUMENT COUNT QUESTIONS
    # RULE BASED ROUTING
    # ==================================================

    if (
        "how many documents" in question.lower()
        or "number of documents" in question.lower()
    ):

        answer = f"""
Total uploaded documents: {len(unique_documents)}

Uploaded document names:
{chr(10).join(unique_documents)}
"""

        st.subheader("AI Response")

        st.write(answer)

    else:

        # ==================================================
        # SPLIT DOCUMENTS INTO CHUNKS
        # ==================================================

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(
            all_documents
        )

        # ==================================================
        # CREATE EMBEDDINGS
        # ==================================================

        embedding_model = OpenAIEmbeddings()

        # ==================================================
        # CREATE VECTOR DATABASE
        # ==================================================

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory="vector_db"
        )

        # ==================================================
        # DETECT COMPARISON QUESTIONS
        # ==================================================

        comparison_keywords = [
            "difference",
            "compare",
            "comparison",
            "similarities",
            "different"
        ]

        is_comparison_query = any(
            keyword in question.lower()
            for keyword in comparison_keywords
        )

        # ==================================================
        # RETRIEVAL STRATEGY
        # ==================================================

        if is_comparison_query:

            # IMPORTANT:
            # For comparison questions,
            # use ALL chunks from ALL documents

            results = chunks

        else:

            # Normal semantic retrieval

            results = vectorstore.similarity_search(
                question,
                k=6
            )

        # ==================================================
        # BUILD RETRIEVED CONTEXT
        # ==================================================

        retrieved_context = ""

        for r in results:

            source = r.metadata.get(
                "source",
                "Unknown"
            )

            retrieved_context += f"""

DOCUMENT: {source}

CONTENT:
{r.page_content}

"""

        # ==================================================
        # BUILD CONVERSATION HISTORY
        # ==================================================

        history = "\n".join(
            st.session_state.chat_history
        )

        # ==================================================
        # FINAL PROMPT
        # ==================================================

        prompt = f"""
You are an AI document comparison assistant
and senior QA architect.

IMPORTANT:
- The user uploaded exactly {len(unique_documents)} documents.
- Retrieved context contains CHUNKS from those documents.
- Multiple chunks may belong to the same document.
- Never confuse chunks with documents.

Uploaded Documents:
{unique_documents}

If the user asks for:
- comparison
- differences
- similarities

Then:
- compare ALL uploaded documents
- do not ignore any document
- explain similarities and differences clearly
- reference document names accurately

Your responsibilities:
1. Identify which content belongs to which document
2. Compare documents accurately
3. Explain similarities and differences
4. Reference document names clearly
5. Answer only using retrieved context

Conversation History:
{history}

Retrieved Context:
{retrieved_context}

Latest Question:
{question}
"""

        # ==================================================
        # GENERATE RESPONSE
        # ==================================================

        with st.spinner("Analyzing documents..."):

            response = llm.invoke(prompt)

        answer = response.content

        # ==================================================
        # SAVE CHAT HISTORY
        # ==================================================

        st.session_state.chat_history.append(
            f"User: {question}"
        )

        st.session_state.chat_history.append(
            f"AI: {answer}"
        )

        # ==================================================
        # DISPLAY RESPONSE
        # ==================================================

        st.subheader("AI Response")

        st.write(answer)

        # ==================================================
        # DEBUG SECTION
        # ==================================================

        with st.expander("Retrieved Context"):

            st.text(retrieved_context)

# ======================================================
# DISPLAY CHAT HISTORY
# ======================================================

st.subheader("Conversation History")

for message in st.session_state.chat_history:

    st.write(message)