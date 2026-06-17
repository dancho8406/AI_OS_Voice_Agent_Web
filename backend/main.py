from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from google import genai
from google.genai import types

app = FastAPI(title="AI OS Voice Agent - Web Cloud API")

# Активираме CORS, за да може телефонът/браузърът да комуникира свободно с Облака
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # В облака това ще позволява достъп от всякакви устройства
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модел за входящата гласова команда (текст от уеб интерфейса)
class ChatRequest(BaseModel):
    message: str

# Взимаме Gemini API ключа безопасно от системната среда
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "ЗАМЕСТИ_С_ТВОЯ_КЛЮЧ_ТУК")

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Липсва съобщение.")
    
    try:
        # Инициализираме новия официален Google GenAI клиент
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Системен промпт, който кара ИИ да връща САМО чист JSON структуриран отговор
        system_instruction = (
            "Ти си уеб асистент. Анализирай гласовата команда на потребителя. "
            "Ако иска да отвори сайт, върни JSON в следния формат: "
            '{"action": "open_url", "url": "истинският пълен URL адрес на сайта"}. '
            "Ако командата е обикновен разговор, върни: "
            '{"action": "chat", "reply": "твоят отговор на български"}. '
            "Връщай САМО валиден JSON без никакъв друг текст или markdown кавички."
        )
        
        # Извикваме модела gemini-2.5-flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=request.message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json" # Принуждаваме модела да върне JSON
            ),
        )
        
        # Връщаме анализирания отговор директно към фронтенда
        return response.text
    
    except Exception as e:
        # Ако ключът липсва или облакът откаже, даваме ясен фийдбек
        return {"action": "chat", "reply": f"Грешка при връзка с ИИ в Облака: {str(e)}"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "environment": "cloud_ready"}
