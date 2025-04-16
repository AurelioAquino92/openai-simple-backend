import os
from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from app_types import ChatRequestProps

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

@app.post("/ask")
async def ask_question(request: ChatRequestProps):
    try:
        openai_messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=openai_messages
        )
        
        assistant_message = response.choices[0].message.content
        
        return {
            "response": assistant_message
        }
    except OpenAIError as e:
        print(f'ERROR: {str(e)}')
        return {
            "response": "I'm having trouble connecting to the AI service right now. Please try again in a few moments.",
            "error": "openai_error",
            "details": str(e)
        }
    except Exception as e:
        print(f'ERROR: {str(e)}')
        return {
            "response": "An unexpected error occurred. Our team has been notified.",
            "error": "internal_error",
            "details": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)