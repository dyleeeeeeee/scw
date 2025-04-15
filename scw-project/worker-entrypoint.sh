#!/bin/sh

until cd /app/scw-project
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A scw-project worker --loglevel=info --concurrency 1 -E