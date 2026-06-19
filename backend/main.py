from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI(title="AI OS Voice Agent - Web Cloud API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Липсва съобщение.")
    
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
    }
    
    command = request.message.lower()
    response_data = None
    
    # 📚 Твоята разширена софтуерна библиотека със сайтове:
    sites_library = {
        ("youtube", "ютуб", "видео"): "https://www.youtube.com",
        ("facebook", "фейсбук", "феисбук"): "https://www.facebook.com",
        ("google", "гугъл", "търсачка"): "https://www.google.com",
        ("instagram", "инстаграм", "инста"): "https://www.instagram.com",
        ("abv", "абв", "поща"): "https://www.abv.bg",
        ("zamunda", "замунда"): "https://zamunda.net",
        ("wikipedia", "википедия", "уикипедия"): "https://bg.wikipedia.org",
        ("github", "гитхъб", "гитхаб"): "https://github.com",
        ("chatgpt", "чатгпт", "openai"): "https://chat.openai.com",
        ("bg-mamma", "бг мама"): "https://www.bg-mamma.com",
        ("sinoptik", "синоптик", "времето"): "https://www.sinoptik.bg",
        ("nova", "нова телевизия", "нова"): "https://nova.bg",
        ("btv", "бтв"): "https://www.btv.bg"
    }
    
    # Проверяваме дали изречената дума съвпада с някой ключ в библиотеката
    for keywords, url in sites_library.items():
        if any(keyword in command for keyword in keywords):
            response_data = {"action": "open_url", "url": url}
            break
            
    # Ако командата не е за сайт от библиотеката, преминаваме в свободен разговор
    if not response_data:
        response_data = {
            "action": "chat", 
            "reply": f"Разбрах гласовата команда: '{request.message}'. Асистентът работи успешно в Google Cloud и е готов за демонстрация!"
        }
        
    utf8_bytes = json.dumps(response_data, ensure_ascii=False).encode('utf-8')
    return Response(content=utf8_bytes, media_type="application/json; charset=utf-8", headers=cors_headers)

@app.get("/api/health")
async def health_check():
    return Response(content='{"status": "healthy"}', media_type="application/json", headers={"Access-Control-Allow-Origin": "*"})
