from langchain import hub
from langchain_voyageai import VoyageAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma

from orchestrator.utils import format_docs
from core.config import settings


class PromptOrchestrator:
    def __init__(
        self,
    ):
        self.pdf_file_path = "/home/alex/Documents/myprojects/harveyIA/src/app/orchestrator/data/direito.pdf"
        self.embeddings = VoyageAIEmbeddings(
            voyage_api_key=settings.voyage_ai.EMBEDDING_API_KEY,
            model=settings.voyage_ai.EMBEDDING_MODEL,
            show_progress_bar=True,
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro", google_api_key=settings.gemini.GEMINI_API_KEY
        )

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
        return vector_store

    def retrieve_relevant_documents(self, vector_store, k: int = 3) -> list:
        """Retrieves the k most relevant text chunks from the vector store based on a query."""
        return vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": k}
        )

    def generate_prompt_template(self, query, context):
        # prompt = hub.pull("rlm/rag-prompt")
        template = "somestring..."
        prompt = ChatPromptTemplate.from_template(template)
        return prompt

    def create_rag_chain(self, context, prompt):
        rag_chain = (
            {"context": context, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        return rag_chain

    def answer_query(self, query: str) -> str:
        """Generates an answer to the query using the RAG process."""
        vector_store = self.build_vector_store()
        relevant_docs = self.retrieve_relevant_documents(vector_store=vector_store)
        prompt_template = self.generate_prompt_template(query, relevant_docs)
        rag_chain = self.create_rag_chain(relevant_docs, prompt_template)
        rag_response = rag_chain.invoke(query)
        return rag_response
