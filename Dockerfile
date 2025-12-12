FROM python:3.11-slim

# system deps for prophet/scipy/psycopg2
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential gfortran libatlas-base-dev liblapack-dev libpq-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
