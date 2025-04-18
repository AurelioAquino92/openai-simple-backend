# OpenAI Simple Backend

A FastAPI-based backend service that provides a simple interface to interact with OpenAI's chat completion API with streaming support.

## Features

- Simple POST endpoint for chat completions
- Support for chat history
- Streaming responses for real-time interaction
- CORS support for frontend integration
- Environment-based configuration
- Error handling and validation
- Automatic request/response validation using Pydantic

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```
Edit the `.env` file and add your OpenAI API key.

## Docker Deployment

The application can be deployed using Docker:

1. Build the Docker image:
```bash
docker build -t openai-simple-backend .
```

2. Run the container:
```bash
docker run -p 8000:8000 openai-simple-backend
```

The application will be available at `http://localhost:8000`.

### Docker Configuration Details
- The Dockerfile uses Python 3.11 slim image for a smaller footprint
- The application runs on port 8000
- Uses uvicorn as the ASGI server
- Optimized for caching dependencies during builds
- Environment variables are included in the Docker image

### Environment Configuration
The application requires the following environment variables:

1. Create a `.env` file from the template:
```bash
cp .env.example .env
```

2. Configure the required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key (required)

The `.env` file should not be committed to version control. Make sure to:
- Keep your API key secure
- Use different API keys for development and production
- Never expose your API key in public repositories

## Usage

1. Start the server using either method:

```bash
# Method 1: Using Python directly
python main.py

# Method 2: Using FastAPI CLI
fastapi run main.py
```

The server will start on `http://0.0.0.0:8000`.

2. Make a POST request to `/ask` endpoint:

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{
           "messages": [
             {"role": "user", "content": "Hello!"},
             {"role": "assistant", "content": "Hi there!"},
             {"role": "user", "content": "How are you?"}
           ]
         }'
```

### Request Format

```json
{
    "messages": [
        {"role": "user", "content": "Your message here"},
        {"role": "assistant", "content": "Previous response"},
        {"role": "user", "content": "New message"}
    ]
}
```

### Response Format

The API returns a streaming response with the following format:
- Each chunk contains a piece of the assistant's response
- The response is streamed in real-time
- The stream is terminated with a "stop" finish reason

### CORS Configuration

The backend is configured to allow requests from `http://localhost:3000` by default. To modify the allowed origins, update the CORS configuration in `main.py`.

## API Documentation

Once the server is running, you can access the automatic API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 400: Bad Request (invalid input)
- 500: Internal Server Error (OpenAI API errors)

Error responses include:
```json
{
    "role": "assistant",
    "content": "Error message",
    "error": "error_type",
    "details": "Detailed error information"
}
```

## Project Structure

```
.
├── main.py              # FastAPI application and routes
├── app_types.py         # Type definitions for request/response
├── requirements.txt     # Project dependencies
├── Dockerfile          # Docker configuration
├── .env.example        # Environment variables template
├── .env                # Environment variables (not in version control)
└── README.md           # Project documentation
```

## Frontend Example

You can find a matching frontend application is available at [openai-simple-frontend](https://github.com/AurelioAquino92/openai-simple-frontend). This frontend provides:

- Modern chat interface using Next.js
- Real-time streaming responses
- Markdown support for messages
- Auto-scrolling to latest messages
- Responsive design
- Input validation

## License

MIT License 