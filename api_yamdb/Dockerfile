FROM python:3.7-slim
LABEL maintainer="https://github.com/NotMainCode"
WORKDIR /app
RUN apt-get update && apt-get install curl --yes
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
