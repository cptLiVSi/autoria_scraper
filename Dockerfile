FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get install -y cron && \
    apt-get install -y postgresql-client && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]