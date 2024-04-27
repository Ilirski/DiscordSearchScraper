FROM python:3.12.3

WORKDIR /app
COPY requirements.lock ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

COPY scraper.py .
WORKDIR /out
ENTRYPOINT ["python", "/app/scraper.py"]

