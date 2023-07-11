# load .env first before importing llama_index
from dotenv import load_dotenv
load_dotenv()

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index.storage import StorageContext
from llama_index.vector_stores import ChromaVectorStore
import chromadb

#  https://docs.trychroma.com/embeddings
# create a Chroma vector store, by default operating purely in-memory
chroma_client = chromadb.Client()

# create a collection
chroma_collection = chroma_client.create_collection("newspieces")
# https://docs.trychroma.com/api-reference
print(chroma_collection.count())

documents = SimpleDirectoryReader('news').load_data()

vector_store = ChromaVectorStore(chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = GPTVectorStoreIndex.from_documents(documents, storage_context=storage_context)
print(chroma_collection.count())
print(chroma_collection.get()['documents'])
print(chroma_collection.get()['metadatas'])

index.storage_context.persist()

# During query time, the index uses Chroma to query for the top k
# most similar nodes, and synthesizes an answer from the retrieved nodes.

query_engine = index.as_query_engine()
r = query_engine.query("Who are the main exporters of Coal to China? What is the role of Indonesia in this?")
print(r)
