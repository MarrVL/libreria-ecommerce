FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV SECRET_KEY=tu_clave_secreta
RUN python manage.py collectstatic --noinput
EXPOSE 8080
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "libreria.wsgi:application"]
