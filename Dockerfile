FROM python:3.14-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

RUN mkdir -p data

VOLUME ["/app/data"]

CMD ["python", "main.py"]