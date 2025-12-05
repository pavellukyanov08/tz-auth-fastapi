FROM python:latest

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
