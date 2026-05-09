# Используем официальный образ Python 3.11
FROM python:3.11-slim

# Рабочая папка внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем пакеты
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт 8000
EXPOSE 8000

# Команда запуска
CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]