#!/bin/sh
echo "Worker entrypoint starting..."
# Wait for Redis name resolution and port
echo "Waiting for redis:6379..."
while ! nc -z redis 6379; do
  echo "Redis unavailable, sleeping..."
  sleep 2
done
echo "Redis is up!"
# Start Celery
exec celery -A scw_project worker --loglevel=info --concurrency 1 -E