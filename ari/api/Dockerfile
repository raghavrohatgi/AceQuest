FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY ari/api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data at build time (so container starts fast)
RUN python -c "import nltk; nltk.download('punkt_tab', quiet=True); nltk.download('punkt', quiet=True)"

# Cache-busting arg (pass --build-arg CACHE_BUST=$(date +%s) to force rebuild)
ARG CACHE_BUST=1

# Copy project
COPY . /app

# NLTK data directory
ENV NLTK_DATA=/root/nltk_data

# Feedback DB stored on Fly.io persistent volume (mounted at /data)
ENV ARI_DB_PATH=/data/feedback.db

EXPOSE 8080

CMD ["uvicorn", "ari.api.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
