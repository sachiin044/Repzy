# Repzy - Go Deeper Than the README

Repzy is an intelligent repository analysis system that leverages AI and vector embeddings to provide deep insights into GitHub repositories. Ask questions about code structure, functionality, and implementation details, and get instant answers with contextual understanding.

## Features

- 🤖 **AI-Powered Analysis**: Semantic search and RAG (Retrieval-Augmented Generation) powered by LangChain and OpenAI
- 📊 **Structural Queries**: Get repository structure, file listings, and function counts
- 🔍 **Content Analysis**: Retrieve and analyze specific files and code snippets
- 💾 **Conversation Memory**: Maintain context across multiple questions with session-based memory
- 🎯 **Smart Follow-ups**: Automatic generation of contextual follow-up questions
- 🌐 **Web Interface**: Streamlit-based frontend for easy interaction
- ⚡ **Fast Backend**: FastAPI-powered REST API for scalable performance

## Architecture

Repzy follows a modular architecture:

```
┌─────────────────────────────────────────────────────┐
│           Frontend (Streamlit App)                   │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP Requests
┌──────────────────▼──────────────────────────────────┐
│           FastAPI Backend (main.py)                  │
├──────────────────────────────────────────────────────┤
│  • Repo ingestion & indexing                         │
│  • Question routing & processing                     │
│  • Session management                                │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────┬──────────────┐
        │          │          │              │
        ▼          ▼          ▼              ▼
    ┌────────┐ ┌──────┐ ┌───────┐ ┌──────────┐
    │ Ingest │ │ Embed│ │ RAG   │ │ Followup │
    │ (Git)  │ │(Vec) │ │(LLM)  │ │ (Gen)    │
    └────────┘ └──────┘ └───────┘ └──────────┘
        │          │
        └──────────┴────────────────────────┐
                                           │
                    ┌──────────────────────▼──┐
                    │   Vector Store (FAISS)   │
                    └──────────────────────────┘
```

## How It Works

1. **Repository Ingestion**: Clones the GitHub repository and extracts all source files
2. **Code Embedding**: Converts code into vector embeddings using sentence-transformers
3. **Vector Storage**: Stores embeddings in FAISS for fast similarity search
4. **Question Routing**: Analyzes questions to determine query type (structural/content/semantic)
5. **Response Generation**: Uses LangChain + OpenAI for intelligent answers
6. **Context Memory**: Maintains conversation history for follow-up understanding

## Installation

### Prerequisites

- Python 3.8+
- Git
- OpenAI API key

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sachiin044/Repzy.git
   cd Repzy
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Running the Application

1. **Start the FastAPI backend** (in one terminal):
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`

2. **Start the Streamlit frontend** (in another terminal):
   ```bash
   streamlit run streamlit_app.py
   ```
   The web interface will open at `http://localhost:8501`

### Workflow

1. Enter a GitHub repository URL in the Streamlit interface
2. Click "Index Repository" to analyze and embed the codebase
3. Ask questions about the repository in natural language
4. Click on follow-up suggestions or ask new questions
5. View the conversation history

### Example Questions

- "Show me the repository structure"
- "How many functions are in this repo?"
- "What functions are in main.py?"
- "How does authentication work?"
- "Explain the embeddings module"

## Project Structure

```
Repzy/
├── main.py              # FastAPI application & routes
├── streamlit_app.py     # Web interface
├── ingest.py            # Repository cloning & file reading
├── embed.py             # Vector embedding creation
├── rag.py               # RAG query & retrieval
├── router.py            # Question type routing
├── followups.py         # Follow-up generation
├── memory.py            # Conversation memory
├── repo_index.py        # Repository indexing utilities
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Dependencies

- **FastAPI**: Web framework for building APIs
- **LangChain**: LLM orchestration and RAG framework
- **OpenAI**: Language model for semantic understanding
- **FAISS**: Vector similarity search library
- **Streamlit**: Web UI framework
- **GitPython**: Git repository operations
- **Sentence-Transformers**: Embedding models
- **Torch**: PyTorch for ML operations

See `requirements.txt` for complete dependency list.

## Configuration

### API Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload-repo` | Index a GitHub repository |
| POST | `/chat` | Submit a question and get answers |

### Request/Response Format

**Upload Repository**:
```json
POST /upload-repo
{
  "repo_url": "https://github.com/user/repo"
}

Response:
{
  "status": "Repository indexed successfully"
}
```

**Chat Query**:
```json
POST /chat
{
  "question": "What does this repo do?",
  "session_id": "optional-session-id"
}

Response:
{
  "answer": "The answer...",
  "follow_ups": ["Follow-up question 1", "Follow-up question 2"],
  "session_id": "session-id"
}
```

## Advanced Features

### Session Management
- Each user gets a unique session ID for conversation tracking
- Maintains context across multiple questions
- Enables personalized follow-up suggestions

### Semantic Search
- Uses transformer-based embeddings for contextual understanding
- Retrieves relevant code snippets based on meaning, not just keywords
- Supports multi-turn conversations with memory

### Query Routing
The system intelligently routes queries:
- **STRUCTURAL**: Repository metadata & code structure questions
- **CONTENT**: Specific file content retrieval
- **SEMANTIC**: Complex reasoning and explanation queries

## Limitations & Future Improvements

### Current Limitations
- Python-focused (best with Python repositories)
- Requires OpenAI API credits
- Limited to repositories under ~100MB
- Context window limited by LLM capabilities

### Planned Features
- Support for multiple programming languages
- Local LLM support (Ollama, LLaMA)
- Batch repository indexing
- Export conversation to PDF
- Code diff analysis
- Performance optimization

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Author

Created by [@sachiin044](https://github.com/sachiin044)

## Support

For issues, questions, or suggestions:
- Open an [GitHub Issue](https://github.com/sachiin044/Repzy/issues)
- Check existing documentation and examples

---
