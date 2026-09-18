# استخدام نسخة لينكس خفيفة ومحمية ومخصصة للأنظمة العسكرية المستقرة
FROM python:3.11-slim-buster

# منح صلاحيات الجذر الكاملة داخل الحاوية لكسر أي قيود بيئية
USER root

# منع بايثون من كتابة ملفات الكاش وضمان ضخ الـ Logs فوراً للشاشة
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تحديد منفذ الاستماع الإجباري الذي تطلبه منصة Render
ENV PORT=8080

WORKDIR /app

# تثبيت الحزم الصافية داخل الحاوية دون الحاجة لملفات خارجية
RUN pip install --no-cache-dir pyTelegramBotAPI requests gunicorn

# نسخ الشفرة البرمجية العابرة للقارات إلى قلب الحاوية
COPY app.py .

# فتح المنفذ الشبكي رغماً عن النظام
EXPOSE 8080

# أمر التشغيل السيادي الفوري الذي يدمج Gunicorn مع البوت 24/7
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
