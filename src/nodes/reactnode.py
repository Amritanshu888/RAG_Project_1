## Here i want to go ahead and create my React Node itself

"""LangGraph nodes for RAG workflow + ReAct Agent inside generate_content"""

from typing import List, Optional
from src.state.rag_state import RAGState

from langchain_core.documents import Document
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent ## This library is basically used to create a react agent itself

# Wikipedia Tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun

class RAGNodes:
    """Contains the node functions for RAG workflow"""

    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm
        self._agent = None ## Initially this is None(This is lazy init agent i.e. it will be initialized in later stages), Why using _agent ?? --> I m just saying that this is a protected variable in my project
        ## W.r.t nodes.py in this folder there we did not create any agent we just had retriever and llm, here we are planning to create one more additional agent

    def retrieve_docs(self, state: RAGState) -> RAGState:
        """Classic retriever node"""
        docs = self.retriever.invoke(state.question) 
        return RAGState(
            question = state.question,
            retrieved_docs = docs
        )
    
    ### Build Tools
    def _build_tools(self, )-> List[Tool]: ## This function will give us the list of tools
        """Build retriever + wikipedia tools"""

        def retriever_tool_fn(query:str)->str: ## This will provide us the response of the retrieved docs
            docs: List[Document] = self.retriever.invoke(query)
            if not docs:
                return "No documents found."
            merged = []
            for i,d in enumerate(docs[:8], start=1):
                meta = d.metadata if hasattr(d, "metadata") else {}
                title = meta.get("title") or meta.get("source") or f"doc_{i}"
                merged.append(f"[{i}] {title}\n{d.page_content}")  ## We are combining it merging it and then appending it
            return "\n\n".join(merged) ## Here we are combining all the documents with metadata and title
        
        retriever_tool = Tool(
            name = "retriever",
            description = "Fetch passages from indexed vectorstore",
            func = retriever_tool_fn
        )
        wiki = WikipediaQueryRun(
            api_wrapper = WikipediaAPIWrapper(top_k_results=3, lang="en") ## Language will be english
        )
        wikipedia_tool = Tool(
            name = "wikipedia",
            description = "Search Wikipedia for general knowledge.",
            func = wiki.run,
        )

        return [retriever_tool, wikipedia_tool]

    ## Build Agent
    def _build_agent(self):
        ## This Agent will have the ReAct Agent Architecture
        """ReAct agent with tools"""
        tools = self._build_tools()
        system_prompt = (
            "You are a helpful RAG agent. "
            "Prefer 'retriever' for user-provided docs; use 'wikipedia' for general knowledge."
            "Return only the final useful answer."
        )
        self._agent = create_react_agent(self.llm, tools=tools, prompt=system_prompt)

    def generate_answer(self, state: RAGState) -> RAGState:
        """
        Generate answer using ReAct agent with retriever + wikipedia.
        """
        if self.agent is None:
            self._build_agent() ## Building the Agent

        result = self._agent.invoke({"messages": [HumanMessage(content=state.question)]})

        messages = result.get("messages", [])
        answer: Optional[str] = None
        if messages:
            answer_msg = messages[-1]
            answer = getattr(answer_msg, "content", None)

        return RAGState(   ## Updating the RAG state
            question = state.question,
            retrieved_docs = state.retrieved_docs,
            answer = answer or "Could not generate answer."
        )       