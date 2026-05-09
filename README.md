# ⚖️ LegalDoc Guardian
**AI Co-Pilot для Compliance & Legal (РФ, 2026)**

> Генерация процессуальных документов с детерминированной валидацией, RAG по актуальным кодексам и audit-trail, соответствующим требованиям 152-ФЗ.

---

## 🎯 Проблема
Юристы и банки тратят до 40% времени на ручную проверку сроков, подсудности и ссылок на нормы. Ошибки ведут к оставлению заявлений без движения или возврату судом.

##  Решение
| Модуль | Функция | Бизнес-ценность |
|--------|---------|-----------------|
|  RAG Engine | Поиск по загруженным кодексам/практике | Исключает hallucination, цитирует только предоставленные нормы |
| 🤖 YandexGPT Lite | Генерация черновика с привязкой к контексту | Отечественный стек, соответствие требованиям локализации (2026) |
| ✅ Validator | Детерминированная проверка сроков/реквизитов | Compliance-gate: документ не уходит без прохождения правил |
| 📜 Audit Log | Фиксация версии модели, промпта и метаданных | Traceability для судов и внутреннего аудита банка |

## 🏗 Архитектура

**Компоненты системы:**
- **API Gateway** (FastAPI) — принимает запросы от юриста/compliance-специалиста
- **Orchestrator** — управляет потоком: RAG → LLM → Validator
- **RAG Engine** — поиск по локальным документам (кодексы, практика)
- **YandexGPT Lite** — генерация черновика с цитатами
- **Pydantic Validator** — детерминированная проверка сроков и реквизитов
- **Audit Log** — фиксация всех действий для compliance

**Поток данных:**
1. Пользователь отправляет запрос → API Gateway
2. Orchestrator ищет релевантные нормы в RAG
3. YandexGPT генерирует черновик с цитатами
4. Validator проверяет сроки (ст. 196 ГК РФ), подсудность, реквизиты
5. Если всё OK → ответ + чек-лист; если есть риски → флаг на ручную проверку
6. Всё логируется в Audit Store (требование 152-ФЗ);

🛠 Стек
LLM: YandexGPT Lite (on-prem/cloud ready)
Backend: FastAPI + Pydantic v2
Validation: Rule-based DSL + Schema enforcement
Infra: Docker Compose, GitHub Actions ready
Compliance: 152-ФЗ ready, PII masking, immutable audit trail
Быстрый старт
Локально (рекомендуется для тестов)

git clone https://github.com/Serx17/legaldoc-guardian.git
cd legaldoc-guardian
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # вставь YANDEX_API_KEY и FOLDER_ID
python -m uvicorn src.api.main:app --reload

🌐 Swagger UI: http://127.0.0.1:8000/docs
Production (Docker)

docker compose up --build

https://github.com/Serx17/legaldoc-guardian/blob/main/FastApi.jpg

📜 Комплаенс & Безопасность (РФ 2026)
✅ Данные не покидают контур (local-first architecture)
✅ Audit trail хранит: prompt_hash, model_version, validation_result
✅ Human-in-the-loop обязателен перед подписанием
✅ Дисклеймер: система является ассистентом, не заменяет юридическую консультацию
Тестирование

pytest tests/ -v  # запуск unit & integration тестов

Лицензия & Disclaimer
MIT License. Продукт находится в стадии MVP. Не является юридической консультацией. Требуется верификация специалистом.
