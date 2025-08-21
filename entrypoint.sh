#!/bin/bash
set -e  # exit if any command fails

# Run migrations
alembic upgrade head

# Start the FastAPI app
uvicorn evm.src.main:app --host 0.0.0.0 --port 8000
