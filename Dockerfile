FROM python:3.11-slim

ENV PYTHONUNBUFFERED True
WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

