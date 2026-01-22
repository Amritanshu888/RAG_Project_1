## Anything that is related to the graph i will be writing the code over here

"""Graph builder for LangGraph workflow"""

from langgraph.graph import StateGraph, END
from src.state.rag_state import RAGState ## Class that we have defined, since we are going to use this values in our graph it is going to maintain the values within the graph itself
from src.nodes.reactnode import RAGNodes ## At any point of time if u really want to just use this reactnode which u have created u can just import like this: "from src.nodes.reactnode import RAGNodes" , rest all the functions below will remain the same.
# from src.nodes.nodes import RAGNodes

class GraphBuilder:
    """Builds and manages the LangGraph workflow"""

    def __init__(self, retriever, llm):
        ## So these are my 3 parameters i definitely require once i initialize my graph builder
        """
        Initialize graph builder

        Args:
            retriever: Document retriever instance
            llm: Language model instance
        """
        self.nodes = RAGNodes() ## Initially it was None
        self.graph = None
        ## The above both needs to be defined hence its kept None

    def build(self):
        """
        Build the RAG workflow graph

        Returns:
            Compiled graph instance
        """
        # Creates a state graph
        builder = StateGraph(RAGState)

        # Add Nodes
        builder.add_node("retriever", self.nodes.retrieve_docs) ## This retriever node is nothing but it is the node that will be interacting with the vectorstore, here retrieve_docs is a function that i have to create inside my nodes folder, bcoz this is one of the node definition.
        builder.add_node("responder", self.nodes.generate_answer) ## Similarily responder is nothing but if u see inside this particular graph, it is used to generate the answer after u retrieve. Here i will be having my LLM and this function will be defined as generate_answer, which will again be defined inside my nodes folder.
        ## So here we have to define two functions one is retrieve_docs and the other is generate_answer

        # Set entry point
        builder.set_entry_point("retriever")

        # Add edges
        builder.add_edge("retriever", "responder")
        builder.add_edge("responder", END)

        # Compile graph
        self.graph = builder.compile()
        return self.graph 
    
    ## Another function to run this entire pipeline
    def run(self, question:str) -> dict:
        """
        Run the RAG workflow

        Args:
            question: User question

        Returns:
           Final state with answer    
        """
        if self.graph is None:
            self.build() ## If self.graph is not there then we are using self.build() which will be completely creating our graph, by build() we get our self.graph

        initial_state = RAGState(question=question) ## Initializing it with the initial question this is our initial state
        return self.graph.invoke(initial_state)    ## Then we are invoking the graph with our initial state. --> Whatever initial state we get from our RAGState.
    
## This way we are integrating graph builder with nodes.
# This is a very simple workflow: We have our retriever and generator, later we will convert this into a React Agent Also.
# For converting into React Agent inside generate answer initially i m just using an LLM which is integrated with the context and prompt.
# Let's say we build some more additional tools, u have tools integrated with those agents that also u can actually define it.  
