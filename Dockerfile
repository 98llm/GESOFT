FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /code

WORKDIR /code

RUN chmod -R a+rwx static && \
    chmod -R a+rwx templates &&\
    pip install --no-cache-dir -r requirements.txt


CMD ["python", "app.py"]

