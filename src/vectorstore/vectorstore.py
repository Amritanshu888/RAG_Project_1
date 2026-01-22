"""Vector store module for document embedding and retrieval"""

from typing import List
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

class VectorStore:
    """Manages vector store application"""
    ## As usual defining a constructor for the class
    def __init__(self):
        self.embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        self.vectorstore = None ## Currently none, it will be initialized later
        self.retriever = None

    def create_retriever(self, documents: List[Document]):
        """
        Create vector store from documents

        Args:
            documents: List of documents to embed
        """
        self.vectorstore = FAISS.from_documents(documents, self.embedding)
        self.retriever = self.vectorstore.as_retriever()

    def get_retriever(self):
        """
        Get the retriever instance

        Returns:
            Retriever instance
        """
        if self.retriever is None:
            raise ValueError("Vector store not initialized. Call create_vectorstore first.")
        return self.retriever
    
    ## How this retriever is going to retrieve the data
    def retrieve(self, query: str, k: int = 4) -> List[Document]:
        """
        Retrieve relevant documents for a query

        Args:
            query: Search query
            k: Number of documents to retrieve

        Returns:
            List of relevant documents    
        """
        if self.retrieve is None:
            raise ValueError("Vector store not initialized. Call create_vectorstore first.")
        return self.retriever.invoke(query)