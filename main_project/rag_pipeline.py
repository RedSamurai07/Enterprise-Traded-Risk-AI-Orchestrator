import os
from langchain_community.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings

CONNECTION_STRING = "postgresql+psycopg2://admin:admin@localhost:5432/risk_db"
COLLECTION_NAME = "sr11_7_policies"

def get_retriever():
    embeddings = OpenAIEmbeddings()
    store = PGVector(
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
    )
    return store.as_retriever(search_kwargs={"k": 3})

def retrieve_policy_context(query: str) -> str:
    retriever = get_retriever()
    docs = retriever.invoke(query)
    return "\n".join([d.page_content for d in docs])
