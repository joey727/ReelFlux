FROM python:3.10.7

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    && pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r app/requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "auth/auth_service.py"]