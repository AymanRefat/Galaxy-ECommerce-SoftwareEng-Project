#!/bin/sh

# Wait for database if needed
if [ "$DB_HOST" = "db" ]; then
    echo "Waiting for postgres..."
    python -c "
import socket
import time
import os

host = os.environ.get('DB_HOST', 'db')
port = 5432

while True:
    try:
        with socket.create_connection((host, port), timeout=1):
            print('Postgres started')
            break
    except OSError:
        print('Postgres is unavailable - sleeping')
        time.sleep(2)
"
fi

# Run migrations
python manage.py migrate --noinput

# Generate random data (limit to 60 seconds to prevent 504 during startup)
timeout 60s python manage.py generate_random_products || echo "Data generation timed out, but continuing startup..."

# Collect static files
python manage.py collectstatic --noinput


# Start server
exec "$@"
