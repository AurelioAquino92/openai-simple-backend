# OpenAI Simple Backend

A FastAPI-based backend service that provides a simple interface to interact with OpenAI's chat completion API.

## Features

- Simple POST endpoint for chat completions
- Support for chat history
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

```json
{
    "response": "Assistant's response here"
}
```

## API Documentation

Once the server is running, you can access the automatic API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 400: Bad Request (invalid input)
- 500: Internal Server Error (OpenAI API errors)

## Project Structure

```
.
├── main.py              # FastAPI application and routes
├── app_types.py         # Type definitions for request/response
├── requirements.txt     # Project dependencies
├── .env.example        # Environment variables template
└── README.md           # Project documentation
```

## License

MIT License 