from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from service.document_service import DocumentService
from service.base_llm_service import BaseLLMService
from service.vectorstore_service import VectorStoreService


class OpenAIService(BaseLLMService):
    def __init__(self,):
        super().__init__()
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.template = """Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Use 10 sentences maximum and keep the answer as concise as possible.

        {context}

        Question: {question}

        Helpful Answer:"""
        self.custom_rag_prompt = PromptTemplate.from_template(self.template)

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def get_answers(self, questions, file):
        docs = DocumentService.load_documents(file)
        if not docs:
            return None, "Failed to load file"
        splits = DocumentService.split_documents(docs)
        vectorstore_service = VectorStoreService()
        vectorstore_service.create_vectorstore(splits)
        retriever = vectorstore_service.get_retriever()
        data = {}
        for question in questions:  
            rag_chain = (
                    {"context": retriever | self.format_docs, "question": RunnablePassthrough()}
                | self.custom_rag_prompt
                | self.llm
                | StrOutputParser()
            )
            data[question] = rag_chain.invoke(question)
        return data, None