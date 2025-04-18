import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from app_types import ChatRequestProps, Message

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your allowed origins here
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
        print(f'ERROR: {str(e)}')
        return {
            "role": "assistant",
            "content": "I'm having trouble connecting to the AI service right now. Please try again in a few moments.",
            "error": "openai_error",
            "details": str(e)
        }
    except Exception as e:
        print(f'ERROR: {str(e)}')
        return {
            "role": "assistant",
            "content": "An unexpected error occurred. Our team has been notified.",
            "error": "internal_error",
            "details": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)