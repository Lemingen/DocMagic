# 📄 DocMagic

**DocMagic** — это микросервис для обработки изображений с помощью Tesseract OCR, построенный на FastAPI. Проект использует PostgreSQL в качестве СУБД и RabbitMQ для очередей задач. Вся система контейнеризована с помощью Docker и Docker Compose.

---

## 🚀 Возможности

- Асинхронный веб-сервер FastAPI
- Распознавание текста с изображений (OCR) через Tesseract
- Хранение данных в PostgreSQL
- Очереди задач с RabbitMQ
- Полная изоляция через Docker

---

## 🧱 Стек технологий

- **FastAPI + Pydantic**
- **Tesseract OCR**
- **PostgreSQL + SQLAlchemy**
- **RabbitMQ + Celery** 
- **Docker + Docker Compose**
- **Uvicorn** (ASGI-сервер)

---

## ⚙️ Установка и запуск

### 1. Клонируй репозиторий

```bash
git clone https://github.com/Lemingen/DocMagic.git && cd DocMagic
```

### 2. Собери и запусти контейнеры

```bash
docker-compose up --build
```

## Готово!

Приложение будет доступно по адресу: http://localhost:8000
RabbitMQ UI: http://localhost:15673 (логин/пароль по умолчанию: guest / guest)
