import os
from loguru import logger
from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)

from llama_index.readers.file import PDFReader
from llama_index.llms.replicate import Replicate
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore

from db.vectordb_client import qdrant_client

os.environ["REPLICATE_API_TOKEN"] = "r8_1iGzzmnDEtIIsfTtwnvedBtCWkWk7Vs2wspxG"

try:
    # LLM Model global settings
    logger.info("Setting LLM Model Global Configuration ...")
    Settings.llm = Replicate(
        model="meta/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf",
        is_chat_model=True,
        additional_kwargs={"max_new_tokens": 512},
    )

    # Embedding Model global settings
    logger.info("Setting Embedding Model Global Configuration ...")
    Settings.embed_model = FastEmbedEmbedding(
        model_name="BAAI/bge-base-en-v1.5", max_length=384
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
        "Setting up QdrantVectorStore with client=qdrant_client, collection_name='teste' ..."
    )
    vector_store = QdrantVectorStore(
        client=qdrant_client, collection_name="pdf_collection"
    )

    # Storage context setup
    logger.info(
        "Creating StorageContext from defaults with vector_store=QdrantVectorStore instance ..."
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print(f"my storage context {storage_context}")

    # Create index using documents and storage context
    logger.info(
        "Creating VectorStoreIndex from loaded documents and StorageContext ..."
    )
    vector_index = VectorStoreIndex.from_documents(
        documents=documents, storage_context=storage_context
    )
    logger.info("VectorStoreIndex created successfully")

    # Query engine setup
    logger.info("Setting up QueryEngine from VectorStoreIndex ...")
    query_engine = vector_index.as_query_engine()
    logger.info("QueryEngine setup completed")

except Exception as e:
    logger.error(f"Error occurred: {str(e)}")
    raise e
