import json
from datetime import datetime
from models.document import LegalDocument
from rag_basic import ask_legal_system  # Импортируем функцию из прошлого шага

def generate_legal_document(question: str, law_text: str) -> dict:
    """Генерация документа + валидация"""
    
    # 1. Получаем черновик от ИИ
    draft_text = ask_legal_system(question, law_text)
    
    # 2. Парсим ответ (для демо — упрощённо)
    # В реальном проекте здесь будет извлечение полей через LLM + JSON schema
    doc = LegalDocument(
        document_type="Исковое заявление",
        court_name="Мировой суд судебного участка №1 г. Москвы",
        plaintiff="Иванов Иван Иванович",
        defendant="ООО 'Ромашка'",
        incident_date=datetime(2023, 1, 15),  # Пример даты
        claims=["Взыскать задолженность 100 000 руб.", "Взыскать неустойку"],
        legal_basis=["ст. 131 ГПК РФ", "ст. 309, 310 ГК РФ"]
    )
    
    # 3. Запускаем валидацию
    validation_result = doc.validate_full()
    
    # 4. Формируем итоговый ответ
    return {
        "draft": draft_text,
        "validation": validation_result,
        "audit": {
            "timestamp": datetime.now().isoformat(),
            "model": "yandexgpt-lite",
            "law_source": "ГПК РФ ст. 131"
        }
    }

# Тест
if __name__ == "__main__":
    with open("data/law_sample.txt", "r", encoding="utf-8") as f:
        law_text = f.read()
    
    question = "Составь структуру искового заявления о взыскании долга"
    
    print("⏳ Генерация документа...")
    result = generate_legal_document(question, law_text)
    
    print("\n📄 ЧЕРНОВИК:")
    print(result["draft"])
    
    print("\n🔍 ПРОВЕРКА:")
    print(f"Статус: {'✅ Принят' if result['validation']['valid'] else '❌ На доработку'}")
    if result["validation"]["warnings"]:
        print("Предупреждения:")
        for w in result["validation"]["warnings"]:
            print(f"  • {w}")
    
    print("\n📋 ЧЕК-ЛИСТ:")
    for k, v in result["validation"]["checklist"].items():
        print(f"  {k}: {v}")