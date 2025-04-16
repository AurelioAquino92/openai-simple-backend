import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from openai import OpenAI
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)