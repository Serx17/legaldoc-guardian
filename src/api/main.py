from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sys
import os

# Добавляем корневую папку в путь, чтобы видеть наши модули
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from models.document import LegalDocument
from rag_basic import ask_legal_system

app = FastAPI(
    title="LegalDoc Guardian API",
    description="AI Co-Pilot for Legal Compliance (RF 2026)",
    version="1.0.0"
)

# Модель запроса (то, что присылает пользователь)
class RequestPayload(BaseModel):
    question: str
    context_file: str = "data/law_sample.txt"

# Модель ответа (то, что мы возвращаем)
class ResponsePayload(BaseModel):
    draft: str
    validation: dict
    timestamp: str

@app.post("/generate", response_model=ResponsePayload)
def generate_document(payload: RequestPayload):
    """
    Генерирует черновик документа и проводит валидацию.
    """
    try:
        # 1. Читаем закон (из файла, указанного в запросе)
        with open(payload.context_file, "r", encoding="utf-8") as f:
            law_text = f.read()
        
        # 2. Запускаем ИИ
        draft = ask_legal_system(payload.question, law_text)
        
        # 3. Создаем модель для валидации (демо-данные)
        doc = LegalDocument(
            document_type="Исковое заявление",
            court_name="Суд общей юрисдикции",
            plaintiff="Истец",
            defendant="Ответчик",
            incident_date=datetime(2023, 1, 1),
            claims=["Взыскание долга"],
            legal_basis=["ст. 131 ГПК РФ"]
        )
        
        # 4. Валидация
        validation_result = doc.validate_full()
        
        # 5. Возврат результата
        return ResponsePayload(
            draft=draft,
            validation=validation_result,
            timestamp=datetime.now().isoformat()
        )
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Файл с законом не найден")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "OK", "service": "LegalDoc Guardian", "compliance": "152-FZ Ready"}