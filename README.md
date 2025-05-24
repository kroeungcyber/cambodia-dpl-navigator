# Cambodia DPL Navigator

A Python application for navigating and querying documents in the Cambodia Digital Public Library (DPL).

## Features

- Document ingestion and processing pipeline
- REST API endpoints for document search
- Integration with LLMs for question answering
- RAG (Retrieval-Augmented Generation) capabilities

## Installation

1. Ensure you have Python 3.10+ installed
2. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Clone this repository:
   ```bash
   git clone https://github.com/[your-username]/cambodia-dpl-navigator.git
   cd cambodia-dpl-navigator
   ```
4. Install dependencies:
   ```bash
   poetry install
   ```

## Configuration

Copy `.env.example` to `.env` and update the values:
```bash
cp .env.example .env
```

Key configuration options:
- `OPENAI_API_KEY`: Your OpenAI API key for LLM integration
- `EMBEDDING_MODEL`: Name of the embedding model to use
- `VECTOR_DB_URL`: URL for your vector database (if using remote)

## Usage

### Running the API
```bash
poetry run uvicorn app.api.endpoints:app --reload
```

### Ingesting Documents
```bash
poetry run python scripts/ingest.py --path /path/to/documents
```

### Running Tests
```bash
poetry run pytest
```

## Project Structure

```
cambodia-dpl-navigator/
├── app/
│   ├── api/              # API endpoints
│   ├── core/             # Core configuration and services
│   ├── models/           # Data models
│   └── services/         # Business logic services
├── scripts/              # Utility scripts
└── tests/                # Test files
```

## API Documentation

The API provides the following endpoints:

- `POST /api/search`: Search documents
- `POST /api/ask`: Ask questions about documents
- `GET /api/health`: Health check endpoint

See the OpenAPI docs at `/docs` when running locally.

## Contributing

Pull requests are welcome. Please ensure tests pass before submitting.

## License

[MIT](https://choosealicense.com/licenses/mit/)