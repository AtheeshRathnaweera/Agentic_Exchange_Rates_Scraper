#!/bin/bash

############################################################################
# Container Entrypoint script
############################################################################

if [[ "$PRINT_ENV_ON_LOAD" = true || "$PRINT_ENV_ON_LOAD" = True ]]; then
  echo "=================================================="
  printenv
  echo "=================================================="
fi

if [[ "$WAIT_FOR_DB" = true || "$WAIT_FOR_DB" = True ]]; then
  echo ">>> Waiting for database..."
  dockerize \
    -wait tcp://$DB_HOST:$DB_PORT \
    -timeout 300s
fi

############################################################################
# Run Alembic migrations
############################################################################
echo ">>> Running Alembic migrations..."
alembic upgrade head || { echo "Alembic migration failed"; exit 1; }

############################################################################
# Start App
############################################################################
echo ">>> Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
