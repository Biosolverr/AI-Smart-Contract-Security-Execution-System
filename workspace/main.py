"""GenRoute AI - Main Entry Point
Запускает API сервер, подключает модули безопасности и роутинга.
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import sys
import os

# Добавляем пути для импорта внутренних модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'product'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'security'))

# Импортируем компоненты (заглушки, если реальные файлы отличаются по сигнатурам)
try:
    from product.api.security_pipeline import SecurityPipeline
    from product.api.routing.security_router import SecurityRouter
except ImportError:
    # Fallback заглушки для демонстрации работы, если модули еще не готовы
    class SecurityPipeline:
        def analyze(self, text: str) -> dict:
            score = 0
            if "ignore" in text.lower(): score += 40
            if "override" in text.lower(): score += 40
            if len(text) > 100: score += 10
            return {"score": min(100, score), "executor": "consensus" if score > 70 else "financial"}
    
    class SecurityRouter:
        def route(self, analysis: dict) -> str:
            return analysis.get("executor", "default")

app = FastAPI(title="GenRoute AI API", version="1.0.0")

# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация компонентов
pipeline = SecurityPipeline()
router = SecurityRouter()

class AnalysisRequest(BaseModel):
    input: str
    context: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    success: bool
    executor: str
    attack_score: int
    confidence: float
    consensus_used: bool
    message: str

@app.get("/")
def read_root():
    return {"status": "online", "service": "GenRoute AI", "docs": "/docs"}

@app.post("/api/route", response_model=AnalysisResponse)
async def route_request(request: AnalysisRequest):
    try:
        # 1. Анализ безопасности
        analysis = pipeline.analyze(request.input)
        
        # 2. Маршрутизация
        executor = router.route(analysis)
        
        # 3. Формирование ответа
        is_dangerous = analysis["score"] > 70
        
        return AnalysisResponse(
            success=not is_dangerous,
            executor=executor,
            attack_score=analysis["score"],
            confidence=max(0.1, 1.0 - (analysis["score"] / 100)),
            consensus_used=(executor == "consensus"),
            message="Blocked by consensus" if is_dangerous else "Processed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs")
async def get_logs():
    # Заглушка для истории логов
    return [
        {"input": "Test transaction", "severity": 10, "label": "financial_executor", "timestamp": "2023-10-27T10:00:00Z"},
        {"input": "Ignore previous instructions", "severity": 85, "label": "consensus_executor", "timestamp": "2023-10-27T10:05:00Z"}
    ]

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
