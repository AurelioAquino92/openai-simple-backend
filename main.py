import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from app_types import ChatRequestProps, Message

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
allowed_origin = os.getenv("ALLOWED_ORIGIN")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed_origin],  # Add your allowed origins here
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def stream_text(messages: list[Message]):
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )
    for chunk in stream:
        for choice in chunk.choices:
            if choice.finish_reason == "stop":
                break
            else:
                yield "{text}".format(text=choice.delta.content)

@app.post("/ask")
async def ask_question(request: ChatRequestProps):
    try:
        response = StreamingResponse(stream_text(request.messages))
        response.headers['x-vercel-ai-data-stream'] = 'v1'
        return response
    except OpenAIError as e:
        error_type = str(e).lower()
        error_message = "An error occurred while processing your request."
        error_code = "openai_error"
        
        if "authentication" in error_type:
            error_message = "Authentication failed. Please check your API key."
            error_code = "authentication_error"
        elif "rate limit" in error_type:
            error_message = "Rate limit exceeded. Please try again later."
            error_code = "rate_limit_error"
        elif "invalid request" in error_type:
            error_message = "Invalid request. Please check your input and try again."
            error_code = "invalid_request_error"
        elif "service unavailable" in error_type:
            error_message = "The AI service is currently unavailable. Please try again later."
            error_code = "service_unavailable_error"
        
        print(f'OpenAI Error: {str(e)}')
        return {
            "role": "assistant",
            "content": error_message,
            "error": error_code,
            "details": str(e)
        }
    except Exception as e:
        print(f'Unexpected Error: {str(e)}')
        return {
            "role": "assistant",
            "content": "An unexpected error occurred. Our team has been notified.",
            "error": "internal_error",
            "details": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)