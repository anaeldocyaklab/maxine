# MAXINE (**M**ultifunctional **A**gent with e**X**ceptional **I**ntelligence, **N**ominal **E**fficiency)

A powerful Python package providing local AI agent capabilities with web search, file operations, and Python execution tools. Built with LangChain, FastAPI, and Ollama for fully local AI operations.

## 🚀 Features

- **Local AI Agent**: Powered by Ollama for complete privacy and control
- **Web Search**: Integrated SearXNG web search capabilities
- **File Operations**: Read and write files with intelligent caching
- **Python Execution**: Safe Python code execution in sandboxed environment
- **Streaming Responses**: Real-time response streaming for better UX
- **FastAPI Integration**: Production-ready REST API with automatic documentation
- **Performance Optimized**: Connection pooling, caching, and async support

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/anaeldocyaklab/maxine.git
cd maxine

# Install dependencies
poetry install
```

## 🛠️ Quick Start

### 1. Environment Setup

Create a `.env` file in the project root:

```env
OLLAMA_MODEL=llama3:8b
OLLAMA_BASE_URL=http://localhost:11434
SEARXNG_BASE_URL=http://localhost:8080
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

### 2. Start the Server

```bash
poetry run maxine
```

### 3. Access the API

- **API Documentation**: <http://localhost:8000/docs>
- **Chat Playground**: <http://localhost:8000/chat/playground>
- **Agent Playground**: <http://localhost:8000/agent/playground>

## 📖 Usage Examples

### API Endpoints

#### Standard Agent

```bash
# POST /agent/invoke
curl -X POST "http://localhost:8000/agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{"input": "What is the weather like today?"}'
```

#### Chat Agent

```bash
# POST /chat/invoke
curl -X POST "http://localhost:8000/chat/invoke" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"content": "Hello, how can you help me?", "role": "user"}]}'
```

#### Streaming Responses

```bash
# POST /chat/stream
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"content": "Explain quantum computing", "role": "user"}]}'
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `llama3:8b` | Ollama model to use |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `SEARXNG_BASE_URL` | `http://localhost:8080` | SearXNG server URL |
| `LOG_LEVEL` | `INFO` | Logging level |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |

### Model Configuration

The agent supports various Ollama models:

```python
# Available models (examples)
OLLAMA_MODEL=llama3:8b          # Balanced performance
OLLAMA_MODEL=llama3:13b         # Better quality
OLLAMA_MODEL=codellama:7b       # Code-focused
OLLAMA_MODEL=mistral:7b         # Alternative model
```

## 🏗️ Architecture

### Core Components

```text
src/
├── agent.py           # Main agent logic and executors
├── server.py          # FastAPI server implementation
├── streaming.py       # Streaming response handling
├── routes.py          # API route definitions
└── tools/
    ├── web_search.py  # Web search functionality
    └── disk_operations.py  # File operations
```

### Agent Flow

1. **Input Processing**: Receives user input via API or direct invocation
2. **Tool Selection**: Agent decides which tools to use based on the task
3. **Tool Execution**: Executes web search, file operations, or Python code
4. **Response Generation**: Formats and returns the final response
5. **Streaming**: Optionally streams response in real-time

## 🔄 API Reference

### Agent Input/Output

```python
class AgentInput(BaseModel):
    input: str = Field(description="The question or instruction for the agent")

class AgentOutput(BaseModel):
    output: str = Field(description="The agent's response")
```

### Tool Schemas

#### Web Search Tool

```python
# Input: Search query string
search_tool._run("Python web scraping tutorial")

# Output: Formatted search results with titles, content, and URLs
```

#### Disk Operations Tool

```python
# Read file
disk_tool._run('{"operation": "read", "path": "file.txt"}')

# Write file
disk_tool._run('{"operation": "write", "path": "file.txt", "content": "Hello World"}')
```

## 🚀 Performance Features

### Caching

- **LLM Caching**: Reuses model instances for better performance
- **Tool Caching**: Caches recently used tools
- **File Caching**: Caches recently read files
- **Message Caching**: Caches processed messages

### Connection Pooling

- **HTTP Session Reuse**: Persistent connections for web requests
- **Async Support**: Full async/await support for better concurrency
- **Connection Limits**: Configurable connection pooling

### Rate Limiting

- **Search Rate Limiting**: Prevents API abuse
- **Configurable Limits**: Adjustable request limits
- **Automatic Cleanup**: Removes old rate limit entries

## 🧪 Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run specific test file
poetry run pytest tests/test_agent.py
```

### Code Quality

```bash
# Format code
poetry run black src/
poetry run ruff format src/

# Lint code
poetry run ruff check src/
poetry run mypy src/
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
poetry run pre-commit install

# Run hooks manually
poetry run pre-commit run --all-files
```

## 📝 Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- Development setup and workflow
- Code standards and best practices
- Commit message guidelines
- Pull request process
- Testing requirements

We welcome contributions! 🚀

## 🐛 Troubleshooting

### Common Issues

#### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

#### SearXNG Connection Issues

```bash
# Check SearXNG availability
curl http://localhost:8080/search?q=test&format=json
```

#### Performance Issues

- **Reduce context window**: Set `num_ctx` to smaller value
- **Use smaller model**: Switch to `llama3:8b` instead of `llama3:13b`
- **Enable caching**: Ensure all caching mechanisms are enabled

## 📊 Monitoring

### Health Checks

```bash
# Check server health
curl http://localhost:8000/health

# Check agent responsiveness
curl -X POST "http://localhost:8000/agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello"}'
```

### Logs

Logs are written to `/var/log/agent/agent.log` and console output.

## 🔒 Security

- **Local Processing**: All AI operations run locally
- **No Data Transmission**: No user data sent to external services
- **Sandboxed Execution**: Python code runs in controlled environment
- **Input Validation**: All inputs are validated and sanitized

## 📄 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/anaeldocyaklab/maxine/issues)
- **Discussions**: [GitHub Discussions](https://github.com/anaeldocyaklab/maxine/discussions)
- **Documentation**: [API Docs](http://localhost:8000/docs)

## 🙏 Acknowledgments

- **LangChain**: For the powerful agent framework
- **Ollama**: For local LLM serving
- **FastAPI**: For the excellent web framework
- **SearXNG**: For privacy-focused web search
