#!/usr/bin/env python3
import argparse
from pathlib import Path
from app.services.rag import RAGService
from app.models.documents import Document
import asyncio
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extracts text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

async def ingest_file(file_path: Path, rag_service: RAGService):
    """Ingests a single file into the RAG system."""
    content = ""
    if file_path.suffix.lower() == ".pdf":
        print(f"Extracting text from PDF: {file_path.name}")
        content = extract_text_from_pdf(file_path)
    elif file_path.suffix.lower() == ".txt":
        print(f"Reading text file: {file_path.name}")
        content = file_path.read_text()
    else:
        print(f"Skipping unsupported file type: {file_path.name}")
        return

    if content:
        document = Document(title=file_path.name, content=content, source=str(file_path))
        success = await rag_service.ingest_document(document)
        if success:
            print(f"Successfully ingested: {file_path.name}")
        else:
            print(f"Failed to ingest: {file_path.name}")

async def main():
    parser = argparse.ArgumentParser(description="Document ingestion script")
    parser.add_argument("path", help="Path to document or directory")
    args = parser.parse_args()
    
    rag = RAGService()
    path = Path(args.path)
    
    if path.is_file():
        await ingest_file(path, rag)
    elif path.is_dir():
        print(f"Ingesting documents from directory: {path.name}")
        for file_path in path.iterdir():
            if file_path.is_file():
                await ingest_file(file_path, rag)
    else:
        print(f"Invalid path: {args.path}")

if __name__ == "__main__":
    asyncio.run(main())
