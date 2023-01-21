FROM python:3.7-slim
LABEL maintainer="https://github.com/NotMainCode"
WORKDIR /app
RUN apt-get update && apt-get install curl --yes
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
RUN chmod +x wait-for-it.sh web_start.sh
CMD ["./wait-for-it.sh", "db:5432", "--strict", "--timeout=300", "--", "./web_start.sh"]
