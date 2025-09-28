.PHONY: install run train test clean help

help:		## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:	## Install dependencies
	pip install -r requirements.txt

run:		## Run the API server
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

train:		## Train the model
	python scripts/retrain_model.py

train-with-data:	## Train the model with fresh data download
	python scripts/retrain_model.py --download-data

fetch-sentinel:	## Fetch Sentinel satellite data
	python scripts/fetch_sentinel_data.py

test:		## Run tests
	python -m pytest tests/ -v

test-api:	## Run API tests only
	python -m pytest tests/test_api.py -v

test-model:	## Run model tests only
	python -m pytest tests/test_model.py -v

clean:		## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf logs/*.log

setup:		## Setup the project (install + train)
	make install
	make train

dev:		## Run in development mode with auto-reload
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

production:	## Run in production mode
	uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4

docker-build:	## Build Docker image (if needed)
	docker build -t crop-backend .

docker-run:	## Run Docker container (if needed)
	docker run -p 8000:8000 crop-backend

lint:		## Lint the code
	black --check src/ tests/ scripts/
	isort --check-only src/ tests/ scripts/

format:		## Format the code
	black src/ tests/ scripts/
	isort src/ tests/ scripts/

check:		## Run all checks (lint + test)
	make lint
	make test

docs:		## Generate API documentation
	@echo "API documentation available at: http://localhost:8000/docs"
	@echo "ReDoc documentation available at: http://localhost:8000/redoc"