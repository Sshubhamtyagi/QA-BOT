from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

class VectorStoreService:
    def __init__(self):
        self.vectorstore = None

    def create_vectorstore(self, splits):
        self.vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    def get_retriever(self):
        return self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
