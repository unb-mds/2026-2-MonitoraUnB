FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY backend/requirements/ ./requirements/

RUN pip install --no-cache-dir -r requirements/requirements.txt

COPY backend/ ./backend/

EXPOSE 8000

CMD ["sh", "-c", "python -m backend.database.setup_db && (python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 & until python -c \"import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/docs')\" 2>/dev/null; do sleep 1; done && python -c \"import urllib.request; req = urllib.request.Request('http://127.0.0.1:8000/api/v1/scraping/iniciar', data=b'{}', headers={'Content-Type': 'application/json'}, method='POST'); print(urllib.request.urlopen(req).read().decode())\" && wait)"]
