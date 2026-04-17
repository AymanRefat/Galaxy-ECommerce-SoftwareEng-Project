#!/bin/sh

# Wait for database if needed
if [ "$DB_HOST" = "db" ]; then
    echo "Waiting for postgres..."
    while ! nc -z $DB_HOST 5432; do
      sleep 0.1
    done
    echo "Postgres started"
fi

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Generate random data
python manage.py generate_random_products

# Start server
exec "$@"
