from langchain_community.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.docstore.document import Document
import pandas as pd


# formatting the data for ingestion
all_prods_df = pd.read_csv("data/cleaned_CSVIndian10000.csv")
all_prods_df = all_prods_df.fillna("")

product_metadata = all_prods_df.to_dict(orient="index")

texts = [str(v['name']) + "\n" + str(v['product_desc']) for k, v in product_metadata.items()]

metadatas = list(product_metadata.values())

docs = [Document(page_content=txt, metadata={"source": meta}) for txt, meta in zip(texts, metadatas)]

print("Data loaded.........")


# load the embedding model
model_name = "BAAI/bge-large-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}

embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

print("Embedding model loaded.........")


# load the vector store
url="http://localhost:6333"
collection_name = "shopintel100v3"

vector_store = Qdrant.from_documents(
    docs,
    embeddings,
    url=url,
    collection_name=collection_name,
    prefer_grpc = False
)

print("Vector store loaded.........")