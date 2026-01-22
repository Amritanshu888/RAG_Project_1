"""RAG state definition for LangGraph"""

from typing import List
from pydantic import BaseModel
from langchain_core.documents import Document

class RAGState(BaseModel):
    """State object for RAG workflow"""
    ## Here we are defining 3 parameters
    question: str ## We are storing it
    retrieved_docs: List[Document] = [] ## This is basically coming from the retriever
    answer: str = ""  ## Coming from the LLM

## RAGState is important as we will be using this entirely in our LangGraph.