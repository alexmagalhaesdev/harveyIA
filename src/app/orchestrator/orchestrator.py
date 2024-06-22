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

    def load_documents(self) -> list:
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
        document_chunks = text_splitter.split_documents(documents)
        return document_chunks

    def build_vector_store(self, document_chunks) -> Chroma:
        """Builds the Chroma vector store and assigns it to self.vector_store."""
        vector_store = Chroma.from_documents(document_chunks, self.embeddings)
        retriever = vector_store.as_retriever()
        return retriever

    def retrieve_relevant_documents(
        self, retriever: str, query: str, k: int = 3
    ) -> list:
        """Retrieves the k most relevant text chunks from the vector store based on a query."""
        context = retriever.similarity_search(query, k=k)
        return context

    def generate_prompt_template(self, query: str, context: str):
        prompt = hub.pull("rlm/rag-prompt")
        return prompt.format(question=query, context=context)

    def create_rag_chain(context, prompt, llm):
        rag_chain = (
            {"context": context | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return rag_chain

    def answer_query(self, rag_chain=None, query=None):
        """Generates an answer to the query using the retrieved texts and an LLM."""
        if rag_chain is None:
            rag_chain = self.create_rag_chain(self.context, self.prompt, self.llm)

        rag_response = rag_chain.invoke(query)
        return rag_response
