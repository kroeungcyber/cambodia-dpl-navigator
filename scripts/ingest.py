#!/usr/bin/env python3
import argparse
from pathlib import Path
from app.services.rag import RAGService

def main():
    parser = argparse.ArgumentParser(description="Document ingestion script")
    parser.add_argument("path", help="Path to document or directory")
    args = parser.parse_args()
    
    rag = RAGService()
    path = Path(args.path)
    
    if path.is_file():
        print(f"Ingesting file: {path.name}")
        # TODO: Implement single file processing
    elif path.is_dir():
        print(f"Ingesting directory: {path.name}")
        # TODO: Implement directory processing
    else:
        print(f"Invalid path: {args.path}")

if __name__ == "__main__":
    main()
