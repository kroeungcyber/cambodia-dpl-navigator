# Cambodia DPL Navigator

A Python application for navigating and querying documents in the Cambodia Digital Public Library (DPL).

## Features

- Document ingestion and processing pipeline
- REST API endpoints for document search
- Integration with LLMs for question answering
- RAG (Retrieval-Augmented Generation) capabilities

## Installation

Follow these steps to get the project up and running on your local machine.

### Prerequisites

*   **Python 3.12+**: It's highly recommended to use a Python version manager like `pyenv` to install and manage Python versions.
    *   If you don't have `pyenv`, you can install it via Homebrew on macOS: `brew install pyenv`
    *   Then install Python 3.12.0: `pyenv install 3.12.0`
    *   Set it as your global Python version: `pyenv global 3.12.0`
*   **uv**: A fast Python package installer and resolver.
    *   Install `uv` by running:
        ```bash
        curl -LsSf https://astral.sh/uv/install.sh | sh
        ```
    *   **Important**: Ensure `uv` is in your system's PATH. Add the following line to your shell configuration file (e.g., `~/.zshrc` for Zsh, `~/.bashrc` for Bash), then restart your terminal or `source` the file:
        ```bash
        export PATH="$HOME/.local/bin:$PATH"
        ```
        After adding, run: `source ~/.zshrc` (or `source ~/.bashrc`)

### Steps

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/[your-username]/cambodia-dpl-navigator.git
    cd cambodia-dpl-navigator
    ```

2.  **Set up Virtual Environment and Install Dependencies**:
    This project uses `poetry` for dependency management, installed within a `uv`-managed virtual environment.
    ```bash
    # Create a virtual environment using Python 3.12.0
    uv venv --python 3.12.0

    # Activate the virtual environment
    source .venv/bin/activate

    # Install Poetry into the virtual environment
    pip install poetry

    # Install project dependencies using Poetry
    poetry install
    ```

## Configuration

Before running the application, you need to set up your environment variables.

1.  **Create `.env` file**:
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```

2.  **Edit `.env` file**:
    Open the newly created `.env` file and replace `YOUR_OPENAI_API_KEY` with your actual OpenAI API key.

    ```ini
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx # Replace with your actual key
    LLM_MODEL_NAME=gpt-4o             # Default LLM model
    LLM_TEMPERATURE=0.7               # LLM response creativity (0.0-1.0)
    VECTOR_DB_PATH=./chroma_db        # Local path for ChromaDB data persistence
    PRODUCTION_MODE=False             # Set to True for production deployment to disable debug mode and hide API docs
    ```

## Usage

Ensure your virtual environment is activated before running any commands:
```bash
source .venv/bin/activate
```

### Running the API

To start the FastAPI application:
```bash
poetry run uvicorn app.api.endpoints:app --reload
```
The API will be accessible at `http://127.0.0.1:8000`. You can view the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/api/v1/docs`.

### Ingesting Documents

The ingestion script processes documents and stores their content embeddings in the ChromaDB. It currently supports `.pdf` and `.txt` file formats.

*   **To ingest a single document**:
    ```bash
    poetry run python scripts/ingest.py --path /path/to/your/document.pdf
    ```
    (Replace `/path/to/your/document.pdf` with the actual path to your PDF or TXT file.)

*   **To ingest all documents from a directory**:
    ```bash
    poetry run python scripts/ingest.py --path /path/to/your/documents_directory/
    ```
    (Replace `/path/to/your/documents_directory/` with the actual path to your directory containing PDF/TXT files.)

### Running Tests

To execute the project's test suite:
```bash
poetry run pytest
```

## Project Structure

```
cambodia-dpl-navigator/
├── app/
│   ├── api/              # API endpoints (FastAPI)
│   ├── core/             # Core configuration (settings, LLM service)
│   ├── models/           # Data models (Document)
│   └── services/         # Business logic services (RAGService)
├── scripts/              # Utility scripts (document ingestion)
├── tests/                # Test files
├── .env.example          # Example environment variables
├── .env                  # Environment variables (user-specific)
└── pyproject.toml        # Project and dependency management (Poetry)
```

## API Documentation

The API provides the following endpoints:

- `POST /api/v1/search`: Search documents based on a query.
- `POST /api/v1/ask`: Ask questions about ingested documents using RAG.
- `GET /health`: Health check endpoint.

See the interactive OpenAPI docs at `/api/v1/docs` when running locally.

## Security Considerations

To enhance the security posture of this application, consider the following:

*   **Input Validation**: Pydantic models are used for API request validation, which helps prevent common injection attacks by ensuring data conforms to expected types and lengths.
*   **Sensitive Data Handling**: API keys are loaded from environment variables (`.env`), which is a good practice. Ensure `.env` is never committed to version control.
*   **Production Configuration**: Set `PRODUCTION_MODE=True` in your `.env` file when deploying to production. This will disable debug mode and hide interactive API documentation (`/docs`, `/redoc`), reducing the attack surface.
*   **Dependency Vulnerability Scanning**: Regularly scan your project dependencies for known vulnerabilities. Tools like `pip-audit` or `safety` can be integrated into your CI/CD pipeline for automated checks.
    *   Example using `pip-audit`: `pip install pip-audit && pip-audit`
*   **Error Handling**: Implement robust error handling to avoid leaking sensitive information in error responses.
*   **Rate Limiting**: For public-facing APIs, consider implementing rate limiting to prevent abuse and denial-of-service attacks.

## Contributing

Pull requests are welcome. Please ensure tests pass before submitting.

## License

[MIT](https://choosealicense.com/licenses/mit/)
