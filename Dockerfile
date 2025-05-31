# Base Build
FROM python:3.12-slim AS build

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*RUN 

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt


# Final Build
FROM python:3.12-slim

WORKDIR /app

COPY --from=build /usr/local /usr/local

COPY . /app/

CMD [ "uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]