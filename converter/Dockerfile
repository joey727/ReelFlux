FROM python:3.10-slim-bookworm

RUN apt-get update && apt-get install -y \
    python3-pip \
    build-essential ffmpeg \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["python", "consumer.py"]