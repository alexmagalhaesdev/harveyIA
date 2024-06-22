from langchain import hub
from langchain_voyageai import VoyageAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma

from orchestrator.utils import format_docs
from core.config import settings


class PromptOrchestrator:
    def __init__(
        self,
    ):
        self.pdf_file_path = "teste"
        self.embeddings = VoyageAIEmbeddings(
            voyage_api_key=settings.voyage_ai.EMBEDDING_API_KEY,
            model=settings.voyage_ai.EMBEDDING_MODEL,
            show_progress_bar=True,
        )
        self.llm = None

    def load_documents(self):
        """Loads a PDF document and returns a list of its pages."""
        loader = PyPDFLoader(self.pdf_file_path)
        documents = loader.load()
        return documents

    def split_documents(
        self, documents: list, chunk_size: int = 1000, chunk_overlap: int = 200
    ) -> list:
        """Splits a list of documents into smaller chunks."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        return text_splitter.split_documents(documents)

    def build_vector_store(self):
        """Builds and returns the Chroma vector store from the PDF document."""
        documents = self.load_documents()
        document_chunks = self.split_documents(documents)
        vector_store = Chroma.from_documents(document_chunks, self.embeddings)
        retriever = vector_store.as_retriever()
        return retriever

    def retrieve_relevant_documents(self, retriever, query: str, k: int = 3) -> list:
        """Retrieves the k most relevant text chunks from the vector store based on a query."""
        context = retriever.similarity_search(query, k=k)
        return context

    def generate_prompt_template(self, query, context):
        prompt = hub.pull("rlm/rag-prompt")
        return prompt.format(question=query, context=context)

    def create_rag_chain(self, context, prompt):
        rag_chain = (
            {"context": context | format_docs(), "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        return rag_chain

    def answer_query(self, query: str) -> str:
        """Generates an answer to the query using the RAG process."""
        retriever = self.build_vector_store()
        relevant_docs = self.retrieve_relevant_documents(retriever, query)
        prompt_template = self.generate_prompt_template(query, relevant_docs)
        rag_chain = self.create_rag_chain(relevant_docs, prompt_template)
        rag_response = rag_chain.invoke(query)
        return rag_response
