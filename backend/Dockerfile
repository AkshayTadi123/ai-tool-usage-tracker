FROM python:3.11-slim

WORKDIR /app

# Dependencies first: this layer is cached unless requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# 0.0.0.0, not 127.0.0.1: the server must accept connections from outside
# the container, not just from inside it.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
