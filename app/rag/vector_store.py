from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader

def load_vectorstore():

    loader = TextLoader("data/business_knowledge.txt")
    docs = loader.load()

    embeddings = OllamaEmbeddings(model="llama3.2")

    return FAISS.from_documents(docs, embeddings)