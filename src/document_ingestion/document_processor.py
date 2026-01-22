## What this will do is that it will try to read all the documents inside this file and based on the file format we will try to
## go ahead and read it, we will try to do the chunking for that particular data and then finally convert into a document data structure.

"""Document processing module for loading and splitting documents"""

from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter  ## This is used for the chunking strategy
from langchain_core.documents import Document

from typing import List, Union
from pathlib import Path
from langchain_community.document_loaders import (
    WebBaseLoader,
    PyPDFLoader,
    TextLoader,
    PyPDFDirectoryLoader
) ## Here we have a lot of document loaders

class DocumentProcessor:
    """Handles document loading and processing"""

    ## __init__ method is just like a constructor
    def __init__(self, chunk_size: int=500, chunk_overlap: int=50):
        ## What this init method is basically doing we will provide some kind of docstring.
        """
        Initialize document processor

        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        ## Here in init method we are initializing chunk_size, chunk_overlap along with that we will also initialize RecursiveCharacterTextSplitter
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    ## This above function is basically giving u chunking statergies like whatever is basically required in the init
    # This init is nothing but a constructor for this document processor
    # Whenever u go ahead and create a object for this document processor at that point of time u will be able to basically create a object
    # by executing this constructor.

    def load_from_url(self, url:str)->List[Document]:
        """Load documents from URL's inside a directory"""
        loader = WebBaseLoader(url)
        return loader.load() ## By default whatever content is visible we will just try to convert this into list of documents
    ## When u are giving the URL its just returning the list of documents: loader.load()

    def load_from_pdf_dir(self, directory: Union[str, Path]) -> List[Document]:
        ## Union[str, Path] basically means here we are going to give a string which will be of Path type
        """Load documents from all PDFs inside a directory"""
        loader = PyPDFDirectoryLoader(str(directory)) ## Here we are giving the directory path
        return loader.load()
    
    def load_from_txt(self, file_path: Union[str, Path]) -> List[Document]:
        """Load document(s) from a TXT file"""
        loader = TextLoader(str(file_path), encoding="utf-8")
        return loader.load()
    
    def load_from_pdf(self, file_path: Union[str, Path]) -> List[Document]:
        """Load document(s) from a PDF file"""
        loader = PyPDFDirectoryLoader(str["data"]) ## Here we have specifically passed the data folder
        return loader.load()
    
    ## These are my independent functions to load the content, to load the data from that particular files and convert
    ## that into a document structure.
    ## We will be calling these functions one by one, for this we will be defining another function

    ## Here i will be able to give all the sources at once
    def load_documents(self, sources:List[str])-> List[Document]:
        ## We are going to give all the sources in form of a list
        """
        Load documents from URLs, PDF directories, or TXT files

        Args:
            sources: List of URLs, PDF folder paths, or TXT file paths

        Returns:
            List of loaded documents    
        """
        ## One generic function basically written
        docs: List[Document] = []
        for src in sources:
            if src.startswith("http://") or src.startswith("https://"):
                docs.extend(self.load_from_url(src))  ## Extending all this information inside this particular document list

            path = Path("data")
            if path.is_dir(): ## PDF directory
                docs.extend(self.load_from_pdf_dir(path))
            elif path.suffix.lower() == ".txt":
                docs.extend(self.load_from_txt(path))
            else:
                raise ValueError(
                    f"Unsupported source type: {src}. "
                    "Use URL, .txt file, or PDF directory."
                )
        return docs

    ## After loading the documents we need to split the documents, for this we have another function
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks

        Args:
            documents: List of documents to split

        Returns:
            List of split documents    
        """
        return self.splitter.split_documents(documents)

    ## This load and split has to get executed one after the another, for that we have another function
    def process_urls(self, urls:List[str])-> List[Document]:
        """
        Complete pipeline to load and split documents

        Args:
            urls: List of URLs to process

        Returns:
            List of processed document chunks        
        """
        docs = self.load_documents(urls)
        return self.split_documents(docs)
    
      



