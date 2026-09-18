FROM python:3.11-slim-buster

USER root

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# نسخ الملف التنفيذي ذاتي التطهير والإصلاح
COPY app.py .

EXPOSE 8080

# إطلاق المحرك مباشرة عبر بايثون النواة
CMD ["python", "app.py"]
