import json
import os

from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import Chroma

from langchain_core.documents import Document

# =====================================================
# MEMORY FILE PATH
# =====================================================

MEMORY_FILE = "memory/chat_memory.json"

VECTOR_DB_PATH = "memory_vector_db"

# =====================================================
# SAVE MEMORY TO JSON
# =====================================================

def save_memory(user_message, ai_response):

    # Load existing memory

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r") as f:

            memories = json.load(f)

    else:

        memories = []

    # Append new memory

    memories.append({

        "user": user_message,
        "ai": ai_response

    })

    # Save updated memory

    with open(MEMORY_FILE, "w") as f:

        json.dump(memories, f, indent=4)

# =====================================================
# LOAD MEMORIES
# =====================================================

def load_memories():

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r") as f:

            return json.load(f)

    return []

# =====================================================
# SAVE MEMORY TO VECTOR DB
# =====================================================

def save_memory_to_vector_db(
    user_message,
    ai_response
):

    memory_text = f"""
USER:
{user_message}

AI:
{ai_response}
"""

    memory_doc = Document(
        page_content=memory_text
    )

    embedding_model = OpenAIEmbeddings()

    # Check if vector DB already exists

    if os.path.exists(VECTOR_DB_PATH):

        vectorstore = Chroma(

            persist_directory=VECTOR_DB_PATH,

            embedding_function=embedding_model
        )

        vectorstore.add_documents(
            [memory_doc]
        )

    else:

        vectorstore = Chroma.from_documents(

            documents=[memory_doc],

            embedding=embedding_model,

            persist_directory=VECTOR_DB_PATH
        )

# =====================================================
# RETRIEVE MEMORY
# =====================================================

def retrieve_memory(query):

    embedding_model = OpenAIEmbeddings()

    if not os.path.exists(VECTOR_DB_PATH):

        return []

    vectorstore = Chroma(

        persist_directory=VECTOR_DB_PATH,

        embedding_function=embedding_model
    )

    results = vectorstore.similarity_search(
        query,
        k=3
    )

    return results