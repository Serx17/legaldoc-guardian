import os
import requests
from dotenv import load_dotenv

# 1. Открываем "сейф"
load_dotenv()
API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

if not API_KEY or not FOLDER_ID:
    print(" Ошибка: Проверь файл .env. YANDEX_API_KEY или FOLDER_ID не указаны.")
    exit()

# 2. Настройки запроса к YandexGPT
url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
headers = {
    # Для API-ключа используется префикс Api-Key
    "Authorization": f"Api-Key {API_KEY}", 
    "Content-Type": "application/json"
}

# 3. Тело запроса (промпт)
body = {
    "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
    "completionOptions": {
        "stream": False,
        "temperature": 0.1,  #  Минимум творчества, максимум точности
        "maxTokens": 300
    },
    "messages": [
        {"role": "system", "text": "Ты юрист-ассистент. Отвечай строго по закону, без воды. Ссылайся на статьи."},
        {"role": "user", "text": "Какой общий срок исковой давности по ГК РФ?"}
    ]
}

# 4. Отправка и вывод
print("⏳ Запрос к YandexGPT отправлен...")
try:
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()  # Вызовет ошибку, если статус не 200
    
    data = response.json()
    answer = data["result"]["alternatives"][0]["message"]["text"]
    print(f"✅ Ответ ИИ:\n{answer}")
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")