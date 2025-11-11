#!/bin/bash
# Load selected env vars from .env
export DB_USER=$(grep '^DB_USER=' .env | cut -d '=' -f2)
export DB_PASS=$(grep '^DB_PASS=' .env | cut -d '=' -f2)
export DB_NAME=$(grep '^DB_NAME=' .env | cut -d '=' -f2)

# Load default environment variables
export DB_DRIVER=postgresql+psycopg
export DB_HOST=localhost
export DB_PORT=5432

# Ask user for migration message
read -p "Enter migration message: " MIGRATION_MSG

# If empty, use default
if [ -z "$MIGRATION_MSG" ]; then
  MIGRATION_MSG="auto migration"
fi

# Run Alembic autogenerate
alembic revision --autogenerate -m "$MIGRATION_MSG"

echo "Migration created successfully with message: '$MIGRATION_MSG'"
