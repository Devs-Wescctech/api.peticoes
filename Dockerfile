FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1         PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends         build-essential         libpq-dev         && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app
COPY scripts /app/scripts
COPY .env.example /app/.env.example

# diretórios de storage
RUN mkdir -p /app/storage/public /app/storage/private

EXPOSE 3001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3001"]
