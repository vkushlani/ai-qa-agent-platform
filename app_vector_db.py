from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

load_dotenv()

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

print(f"Total Chunks: {len(chunks)}")

#Create embeddings
embedding_model = OpenAIEmbeddings()

#Store in vector database
vectorestore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="vector_db"
)

#User Question
#query = "What payment system risks exist?"
query = input("Ask your testing question: ")

#Retrieve relevant chunks from vector database
results = vectorestore.similarity_search(query)

for result in results:
    print(result.page_content)
    
#print("Vector database created successfully.")

