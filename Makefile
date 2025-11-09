SHELL := /bin/bash

.PHONY: build up migrate test lint run

build:
	docker-compose build

up:
	docker-compose up --build

migrate:
	poetry run alembic upgrade head

test:
	poetry run pytest

lint:
	poetry run ruff check app

run:
	poetry run uvicorn app.main:app --reload

