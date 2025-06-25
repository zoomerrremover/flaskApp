#!/bin/bash

VENV_PATH=".venv" 
CONTAINERNAME="postgres_db" 

cleanup() {
    echo "--- Cleaning up ---"
    echo "Bringing down Docker services..."
    docker-compose down || true
    echo "Deactivating virtual environment..."
    deactivate || true 
}
trap cleanup EXIT


echo "--- Starting Test Environment Setup ---"

echo "Activating virtual environment at $VENV_PATH..."
if [ -d "$VENV_PATH" ]; then 
    source "$VENV_PATH/bin/activate"
else
    echo "Error: Virtual environment '$VENV_PATH' not found."
    exit 1 
fi

docker-compose up -d
until [ "`docker inspect -f {{.State.Health.Status}} $CONTAINERNAME`"=="healthy" ]; do
    sleep 0.1;
done;

PYTEST_OUTPUT=$(python -m pytest )
echo "" 
echo "--- Pytest Results ---"
echo "$PYTEST_OUTPUT" 
echo "--- End Pytest Results ---"
echo ""

