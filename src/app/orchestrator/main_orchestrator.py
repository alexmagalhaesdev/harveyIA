from loguru import logger
from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    ServiceContext,
)

from llama_index.readers.file import PDFReader
from llama_index.llms.gemini import Gemini
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.voyageai import VoyageEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore


from core.config import settings
from db.vectordb_client import qdrant_client

try:
    # LLM Model global settings
    logger.info("Setting LLM Model Global Configuration ...")
    Settings.llm = None

    # Embedding Model global settings
    logger.info("Setting Embedding Model Global Configuration ...")
    embed_model = VoyageEmbedding(
        model_name=settings.voyage_ai.EMBEDDING_MODEL,
        voyage_api_key=settings.voyage_ai.EMBEDDING_API_KEY,
    )

    # Chunk Pattern Global Settings
    logger.info("Setting Chunk Pattern Global Configuration ...")
    text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)
    Settings.text_splitter = text_splitter

    # Load documents from S3
    logger.info("Loading documents from './data' directory using PDFReader ...")
    parser = PDFReader()
    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(
        "/home/alex/Documents/myprojects/harveyIA/src/app/orchestrator/data",
        file_extractor=file_extractor,
    ).load_data()
    logger.info(f"Loaded {len(documents)} documents")

    # Vector store setup
    logger.info(
        "Setting up QdrantVectorStore with client=qdrant_client, collection_name='law_collection' ..."
    )
    vector_store = QdrantVectorStore(
        client=qdrant_client, collection_name="law_collection"
    )

    # Storage context setup
    logger.info(
        "Creating StorageContext from defaults with vector_store=QdrantVectorStore instance ..."
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Service Context
    logger.info("Setting up Service Context' ...")
    service_context = ServiceContext.from_defaults(
        llm=None, llm_predictor=None, embed_model=embed_model
    )

    # Create index using documents and storage context
    logger.info(
        "Creating VectorStoreIndex from loaded documents and StorageContext ..."
    )
    vector_index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        service_context=service_context,
    )
    logger.info("VectorStoreIndex created successfully")

    # Query engine setup
    logger.info("Setting up QueryEngine from VectorStoreIndex ...")
    query_engine = vector_index.as_query_engine()
    logger.info("QueryEngine setup completed")

except Exception as e:
    logger.error(f"Error occurred: {str(e)}")
    raise e
