#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

echo "Applying database migrations..."
uv run python manage.py migrate --noinput

echo "Collecting static files..."
uv run python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec uv run gunicorn honest_sign.wsgi:application \
    --bind "[::]:8000" \
    --workers 1 \
    --worker-connections 1000 \
    --max-requests 5000 \
    --max-requests-jitter 1000 \
    --timeout 30 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output