from typing import List, Optional
from app.core.llm import LLMService
from app.models.documents import Document
from app.core.config import settings

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

class RAGService:
    def __init__(self):
        self.llm_service = LLMService()
        self.embedding_model = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
        self.vector_db = Chroma(
            persist_directory=settings.vector_db_path,
            embedding_function=self.embedding_model
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(
                openai_api_key=settings.openai_api_key,
                model_name=settings.llm_model_name,
                temperature=settings.llm_temperature
            ),
            chain_type="stuff",
            retriever=self.vector_db.as_retriever()
        )
        
    async def ingest_document(self, document: Document) -> bool:
        """Process and store a document in the vector database."""
        try:
            texts = self.text_splitter.split_text(document.content)
            metadatas = [{"source": document.source, "title": document.title} for _ in texts]
            self.vector_db.add_texts(texts=texts, metadatas=metadatas)
            self.vector_db.persist()
            return True
        except Exception as e:
            print(f"Error ingesting document {document.title}: {e}")
            return False
        
    async def query(self, question: str, top_k: int = 3) -> str:
        """Query the RAG system using the QA chain."""
        try:
            response = self.qa_chain.invoke({"query": question})
            return response["result"]
        except Exception as e:
            print(f"Error querying RAG system: {e}")
            return f"Error: Could not retrieve answer. {e}"
        
    async def batch_ingest(self, documents: List[Document]) -> bool:
        """Process multiple documents in a batch."""
        results = []
        for doc in documents:
            results.append(await self.ingest_document(doc))
        return all(results)
