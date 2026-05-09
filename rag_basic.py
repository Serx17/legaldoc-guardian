import os
import requests
from dotenv import load_dotenv

# 1. Загружаем настройки
load_dotenv()
API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

def ask_legal_system(question: str, law_text: str) -> str:
    """
    Задаёт вопрос ИИ с привязкой к тексту закона.
    """
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 2. Системный промпт — «инструкция» для ИИ
    system_prompt = """Ты — юридический ассистент. 
    - Отвечай ТОЛЬКО на основе предоставленного текста закона.
    - Если ответа нет в тексте, пиши: "В предоставленном тексте нет ответа".
    - Цитируй статьи и части точно.
    - Не добавляй выдуманных норм."""

    # 3. Формируем контекст + вопрос
    user_message = f"""Текст закона:
<<<
{law_text}
>>>

Вопрос юриста: {question}

Ответ (с цитатами):"""

    body = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.05,  # 🔽 Почти ноль: только факты, никакого творчества
            "maxTokens": 500
        },
        "messages": [
            {"role": "system", "text": system_prompt},
            {"role": "user", "text": user_message}
        ]
    }

    # 4. Запрос
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()["result"]["alternatives"][0]["message"]["text"]
    else:
        return f"❌ Ошибка API: {response.status_code} — {response.text}"

# 5. Тестовый запуск
if __name__ == "__main__":
    # Читаем файл с законом
    with open("data/law_sample.txt", "r", encoding="utf-8") as f:
        law_text = f.read()
    
    # Задаём вопрос
    question = "Какие реквизиты обязательно указать в исковом заявлении по ст. 131 ГПК РФ?"
    
    print("⏳ Анализирую текст закона...")
    answer = ask_legal_system(question, law_text)
    print(f"\n✅ Ответ:\n{answer}")