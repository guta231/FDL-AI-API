FROM python:3.11-slim


RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN sed -i '/setuptools/d' requirements.txt || true && \
    sed -i '/msgpack/d' requirements.txt || true && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "setuptools>=78.1.1" "msgpack>=1.2.1"

COPY . .

EXPOSE 4242


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4242"]