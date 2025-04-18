#!/bin/sh
echo "Server entrypoint starting..."
# Wait for DB name resolution and port
echo "Waiting for db:5432..."
while ! nc -z db 5432; do
  echo "Database unavailable, sleeping..."
  sleep 2
done
echo "Database is up!"

# Optional: Wait for Redis if needed by Django startup
# echo "Waiting for redis:6379..."
# while ! nc -z redis 6379; do
#   echo "Redis unavailable, sleeping..."
#   sleep 2
# done
# echo "Redis is up!"

# Now run migrate (should connect faster now)
echo "Running migrations..."
python manage.py migrate --noinput # Use --noinput in scripts

# Start server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000