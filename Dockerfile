FROM python:3.10.9-alpine3.17
RUN mkdir -p /tmp/clientsviewer
WORKDIR /tmp/clientsviewer
COPY . /tmp/clientsviewer
RUN pip install uvicorn gunicorn
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ EUROPE/MOSCOW
RUN mkdir media static
RUN manage.py makemigrations userinfo && manage.py migrate 
CMD  gunicorn --bind :8000 --workers 3 clientsviewer.wsgi:application &  while true;do python3 manage.py check_memory; sleep 10;done >/dev/null 2>&1
