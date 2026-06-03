from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

load_dotenv()

#Load LLM
llm=ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.2
)

#Load Document
loader = TextLoader("docs/release_notes.txt")
documents = loader.load()

#Split Document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    #how much text per chunk.
    chunk_size=300, 
    #preserves context continuity between chunks.
    chunk_overlap=50
)

chunks =text_splitter.split_documents(documents)

#print(f"Total Chunks: {len(chunks)}")

#Create embeddings
embedding_model = OpenAIEmbeddings()

#Store in vector database
vectorestore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="vector_db"
)

#user Question

query = input("Ask your testing question: ")

#Retrieve relevant chunks from vector database
results = vectorestore.similarity_search(query)

retrieved_context = "\n\n".join(
    [result.page_content for result in results]
)

#Build Final Prompt
prompt = f"""
You are a senior QA architect.

Use the retrieved release notes context below
to answer the user's question.

Context:
{retrieved_context}

Question:
{query}
"""

#Invoke LLM
response = llm.invoke(prompt)

print("\nAI Response:\n")
print("LLM Response: ", response.content)



