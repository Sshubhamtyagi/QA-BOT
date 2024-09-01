from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentService:
    
    @classmethod
    def load_documents(cls, file):
        try:
            loader = PyPDFLoader(file_path=file)
            return loader.load()
        except Exception as e:
            print(e)
            return None

    @classmethod
    def split_documents(cls, docs):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
        return text_splitter.split_documents(docs)
