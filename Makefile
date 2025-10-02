.PHONY: help install test lint clean run docker-build docker-up docker-down

help:
	@echo "AI Memory - Development Commands"
	@echo "=================================="
	@echo "install     - Install dependencies"
	@echo "test        - Run tests"
	@echo "test-cov    - Run tests with coverage"
	@echo "lint        - Run code linting"
	@echo "clean       - Clean up cache and build files"
	@echo "run         - Run the Flask development server"
	@echo "docker-build - Build Docker image"
	@echo "docker-up   - Start Docker Compose services"
	@echo "docker-down - Stop Docker Compose services"

install:
	pip install -r requirements.txt
	pip install pytest pytest-cov flake8

test:
	FLASK_ENV=testing pytest tests/ -v

test-cov:
	FLASK_ENV=testing pytest tests/ -v --cov=. --cov-report=html --cov-report=term

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov .coverage

run:
	python main.py

docker-build:
	docker build -t ai-memory:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f
