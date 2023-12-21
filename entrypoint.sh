#!/bin/bash
set -e

# Wait for the database to be ready
echo "Waiting for the database..."
while ! nc -z postgresdb 5432; do
    sleep 1
done
echo "Database is ready."

# Run the actual command (e.g., Django server)
exec "$@"
