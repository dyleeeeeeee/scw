FROM python:3.11.11

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

# Add this line to install netcat (OpenBSD variant is common)
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

RUN chmod +x /app/server-entrypoint.sh
RUN chmod +x /app/worker-entrypoint.sh