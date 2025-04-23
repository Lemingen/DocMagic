FROM python:3.13.1-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    gcc \
    libgl1

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD bash -c "alembic upgrade head && celery -A app.tasks.tasks worker --loglevel=info & uvicorn app.api.v1.api:app --host 0.0.0.0 --port 8000"
