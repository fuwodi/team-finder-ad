#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until python - <<'PY'
import os

import psycopg2

conn = psycopg2.connect(
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ.get("POSTGRES_HOST", "db"),
    port=os.environ.get("POSTGRES_PORT", "5432"),
)
conn.close()
PY
do
  sleep 1
done

echo "PostgreSQL is ready."
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec python manage.py runserver 0.0.0.0:8000 --noreload
