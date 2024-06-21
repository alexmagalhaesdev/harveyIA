from loguru import logger
from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore

from db.vectordb_client import qdrant_client

try:
    # LLM Model global settings
    logger.info("Setting LLM Model Global Configuration ...")
    Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

    # Embedding Model global settings
    logger.info("Setting Embedding Model Global Configuration ...")
    Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")

    # Chunk Pattern Global Settings
    logger.info("Setting Chunk Pattern Global Configuration ...")
    text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)
    Settings.text_splitter = text_splitter

    # Load documents from S3
    logger.info("Loading documents from './data' directory using PDFReader ...")
    parser = PDFReader()
    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(
        "./data", file_extractor=file_extractor
    ).load_data()
    logger.info(f"Loaded {len(documents)} documents")

    # Vector store setup
    logger.info(
        "Setting up QdrantVectorStore with client=qdrant_client, collection_name='teste' ..."
    )
    vector_store = QdrantVectorStore(client=qdrant_client, collection_name="teste")

    # Storage context setup
    logger.info(
        "Creating StorageContext from defaults with vector_store=QdrantVectorStore instance ..."
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create index using documents and storage context
    logger.info(
        "Creating VectorStoreIndex from loaded documents and StorageContext ..."
    )
    vector_index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        transformations=[text_splitter],
    )
    logger.info("VectorStoreIndex created successfully")

    # Query engine setup
    logger.info("Setting up QueryEngine from VectorStoreIndex ...")
    query_engine = vector_index.as_query_engine()
    logger.info("QueryEngine setup completed")

except Exception as e:
    logger.error(f"Error occurred: {str(e)}")
    raise e
