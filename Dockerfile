FROM python:3.10.9-alpine3.17
RUN mkdir -p /tmp/clientsviewer
WORKDIR /tmp/clientsviewer
COPY . /tmp/clientsviewer
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ EUROPE/MOSCOW
CMD ["uvicorn","main:api"]

