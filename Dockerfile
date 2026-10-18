FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    pkg-config \
    gcc \
    python3-dev \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . ./purrfect_home

EXPOSE 8000

CMD ["uvicorn", "purrfect_home.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

