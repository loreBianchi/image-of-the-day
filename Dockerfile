FROM python:3.11-slim

# Prevenire problemi di generazione locale
ENV PYTHONUNBUFFERED=1

# Install system deps (important for many Python libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia requirements
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'app
COPY app ./app

EXPOSE 8000

# Comando di avvio (produzione)
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
