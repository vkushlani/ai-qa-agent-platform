import streamlit as st
import time
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from pypdf import PdfReader
from docx import Document as DocxDocument
env_path = Path(__file__).with_name('.env')
load_dotenv(dotenv_path=env_path)

from langchain_openai import (
    ChatOpenAI,
    OpenAIEmbeddings
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma

from langchain_core.documents import Document

from app_router import classify_question

from app_memory_manager import (
    save_memory,
    load_memories,
    save_memory_to_vector_db,
    retrieve_memory
)

from app_agents import coordinator_agent


# =====================================================
# ENVIRONMENT
# =====================================================

# .env already loaded above before importing modules that require it.

# =====================================================
# LLM
# =====================================================

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.2
)

# =====================================================
# STREAMLIT PAGE
# =====================================================

st.set_page_config(
    page_title="AI Testing Agent Platform",
    layout="wide"
)

st.title("AI-Powered QA Agent Platform")

st.caption(
    """
AI Assistant for Test Design, Defect Analysis,
Traceability, Regression Risk Assessment,
Document Analysis and QA Planning.
"""
)

st.markdown("""
This app demonstrates an AI assistant for software testing.

You can use it to:

- Generate test cases from requirements
- Analyze defects and root causes
- Create requirement traceability ideas
- Identify regression risks
- Run mock automation checks

You may ask questions directly, or optionally upload documents such as:
release notes, requirements, defect reports, test plans, or user stories.
""")

    
# =====================================================
# SAMPLE PROMPTS
# =====================================================

# st.markdown("### Try one of these prompts:")


# =====================================================
# CHATGPT-STYLE INPUT
# =====================================================

typed_prompt = st.chat_input(
    "Ask the AI Testing Agent..."
)

question = typed_prompt

# =====================================================
# SESSION STATE
# =====================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# =====================================================
# LOAD PERSISTENT MEMORY
# =====================================================

past_memories = load_memories()

# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_files = st.file_uploader(
    "Optional: Upload QA documents",
    type=["txt", "pdf", "docx", "csv", "xlsx"],
    accept_multiple_files=True,
    help="Upload release notes, requirements, defect reports, user stories, test plans, CSV, Excel, Word, or PDF files."
)



# =====================================================
# MAIN PROCESS
# =====================================================
def extract_file_content(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    elif file_name.endswith(".pdf"):
        pdf_reader = PdfReader(uploaded_file)
        text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    elif file_name.endswith(".docx"):
        doc = DocxDocument(uploaded_file)
        text = ""

        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

        return text

    elif file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        return df.to_string(index=False)

    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        return df.to_string(index=False)

    else:
        return ""
    
if question:
    start_time = time.time()
    
    query_type = classify_question(question)

    # st.info(
    #     f"Workflow Selected: {query_type}"
    # )

    # ================================================
    # WORKFLOWS REQUIRING DOCUMENTS
    # ================================================

    document_required_workflows = [

        "comparison",
        "summary",
        "document_count",
        # "rag_search"

    ]

    if (

        query_type in document_required_workflows

        and

        not uploaded_files

    ):

        st.error(
            "This question requires documents. Please upload release notes, requirements, defect reports, or test plans below the prompt box."
        )

        st.stop()

    # ================================================
    # INITIALIZE VARIABLES
    # ================================================

    all_documents = []

    uploaded_document_names = []

    combined_content = ""

    unique_documents = []

    retrieved_context = ""

    memory_context = ""

    history = "\n".join(
        st.session_state.chat_history
    )

    # ================================================
    # LOAD DOCUMENTS (OPTIONAL)
    # ================================================

    if uploaded_files:
        
        st.success(
        f"{len(uploaded_files)} document(s) uploaded"
    )

    for file in uploaded_files:

        st.write(
            f"📄 {file.name}"
        )
        
        for uploaded_file in uploaded_files:

            filename = uploaded_file.name

            uploaded_document_names.append(
                filename
            )

            content = extract_file_content(uploaded_file)

            combined_content += f"""

DOCUMENT NAME:
{filename}

DOCUMENT CONTENT:
{content}

"""

            all_documents.append(

                Document(

                    page_content=content,

                    metadata={
                        "source": filename
                    }
                )
            )

        unique_documents = list(
            set(uploaded_document_names)
        )

    # ================================================
    # MEMORY RETRIEVAL
    # ================================================

    memory_results = retrieve_memory(
        question
    )

    for memory in memory_results:

        memory_context += f"""

{memory.page_content}

"""

    # ================================================
    # RAG SEARCH (ONLY IF DOCUMENTS EXIST)
    # ================================================

    if all_documents:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(
            all_documents
        )

        embedding_model = OpenAIEmbeddings()

        vectorstore = Chroma.from_documents(

            documents=chunks,

            embedding=embedding_model,

            persist_directory="vector_db"
        )

        results = vectorstore.similarity_search(

            question,

            k=6
        )

        for r in results:

            source = r.metadata.get(
                "source",
                "Unknown"
            )

            retrieved_context += f"""

DOCUMENT:
{source}

CONTENT:
{r.page_content}

"""

    # ================================================
    # MASTER CONTEXT
    # ================================================

    master_context = f"""

Uploaded Documents:
{unique_documents}

Conversation History:
{history}

Historical Memory:
{memory_context}

Retrieved Context:
{retrieved_context}

Document Content:
{combined_content}

"""

    # ================================================
    # DOCUMENT COUNT
    # ================================================

    if query_type == "document_count":

        answer = f"""
Total Uploaded Documents: {len(unique_documents)}

Document Names:

{chr(10).join(unique_documents)}
"""

    # ================================================
    # SUMMARY
    # ================================================

    elif query_type == "summary":

        prompt = f"""
Summarize all uploaded documents.

Documents:
{unique_documents}

Content:
{combined_content}
"""

        response = llm.invoke(prompt)

        answer = response.content

    # ================================================
    # COMPARISON
    # ================================================

    elif query_type == "comparison":

        prompt = f"""
Compare all uploaded documents.

Content:
{combined_content}

Question:
{question}
"""

        response = llm.invoke(prompt)

        answer = response.content

    # ================================================
    # MULTI AGENT WORKFLOWS
    # ================================================

    elif query_type in [

       "test_case",

    "defect_analysis",

    "traceability",

    "regression_risk",

    "coverage_pipeline",

    "automation",

    "website_testing",

    "planning"


    ]:
        
    
        answer = coordinator_agent(

            query_type=query_type,

            context=master_context,

            question=question
        )

    # ================================================
    # DEFAULT RAG
    # ================================================

    else:

        if retrieved_context:

            prompt = f"""
You are a Senior QA AI Assistant.

Use uploaded documents if relevant.

Conversation History:
{history}

Historical Memory:
{memory_context}

Retrieved Context:
{retrieved_context}

Question:
{question}
"""

        else:

            prompt = f"""
You are a friendly AI QA Assistant.

If the user is chatting casually,
respond naturally.

If the user asks QA questions,
answer using your QA knowledge.

Conversation History:
{history}

Historical Memory:
{memory_context}

Question:
{question}
"""

        response = llm.invoke(prompt)

        answer = response.content

    # ================================================
    # SAVE CHAT
    # ================================================

    st.session_state.chat_history.append(
        f"User: {question}"
    )

    st.session_state.chat_history.append(
        f"AI: {answer}"
    )

    save_memory(
        question,
        answer
    )

    save_memory_to_vector_db(
        question,
        answer
    )

    # =====================================================
# DISPLAY CHATGPT-STYLE RESPONSE
# =====================================================

    # st.chat_message("user").write(question)

    # st.chat_message("assistant").write(answer)
    
    
    
    # with st.expander(
    #     "Retrieved Document Context"
    # ):
    #     st.text(retrieved_context)

    # with st.expander(
    #     "Retrieved Memory Context"
    # ):
    #     st.text(memory_context)
    
 

    # =================================================
    # DEBUG SECTION
    # =================================================

    # with st.expander(
    #     "Retrieved Document Context"
    # ):
    #     st.text(retrieved_context)

    # with st.expander(
    #     "Retrieved Memory Context"
    # ):
    #     st.text(memory_context)

    
# =====================================================
# CHATGPT-STYLE CHAT HISTORY
# =====================================================

st.subheader("Conversation")

for item in st.session_state.chat_history:

    if item.startswith("User:"):

        st.chat_message("user").write(
            item.replace("User:", "").strip()
        )

    elif item.startswith("AI:"):

        st.chat_message("assistant").write(
            item.replace("AI:", "").strip()
        )
        
end_time = time.time()

st.caption(
    f"Response generated in {end_time-start_time:.2f} seconds"
)
# =====================================================
# PERSISTENT MEMORY
# =====================================================

# with st.expander(
#     "Persistent Memory Store"
# ):

#     st.write(
#         past_memories
#     )
    
st.markdown("---")

st.caption(
    """
Built with:

Streamlit
LangChain
OpenAI
ChromaDB

Multi-Agent QA Architecture
"""
)