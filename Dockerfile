# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем переменные окружения
# PYTHONUNBUFFERED: гарантирует, что вывод Python отправляется прямо в терминал
# PYTHONDONTWRITEBYTECODE: предотвращает создание .pyc файлов
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы управления зависимостями
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости проекта, не включая dev-зависимости
RUN poetry config virtualenvs.create false && poetry install --without dev --no-root

# Копируем остальной код проекта в рабочую директорию
COPY . /app/
