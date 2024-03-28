FROM python:3.10.11-alpine

# Установка зависимостей для сборки (если требуются)
RUN pip install --upgrade --no-cache-dir pip && pip install poetry --no-cache-dir;

WORKDIR /DRF

# Копирование файла зависимостей и установка зависимостей
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов проекта
COPY . .

# Запуск Django
RUN chmod +x run.sh