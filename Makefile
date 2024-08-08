PACKAGE_DIRECTORY := .
CACHE_DIRECTORY := .cache

# Clean the cache directory
.PHONY: clean
clean:
	rm --force --recursive "${CACHE_DIRECTORY}"
	rm --force --recursive `find . -type d -name __pycache__`

# Linting commands
.PHONY: lint
lint:
	@hatch run mypy ${PACKAGE_DIRECTORY}
	@hatch run ruff check ${PACKAGE_DIRECTORY}
	@hatch run ruff format --check ${PACKAGE_DIRECTORY}

.PHONY: format
format:
	@hatch run ruff format ${PACKAGE_DIRECTORY}
	@hatch run ruff check --fix ${PACKAGE_DIRECTORY}

# Migration commands
.PHONY: migration
migration:
	hatch run alembic revision --autogenerate -m $(name) --rev-id $(rev_id)

.PHONY: migrate
migrate:
	hatch run alembic upgrade head

# Development commands
.PHONY: dev
dev:
	hatch env create
	hatch run pip install .
	hatch run pip install .[dev]

# Docker commands
.PHONY: app-build
app-build:
	docker-compose build

.PHONY: app-run
app-run:
	docker-compose stop
	docker-compose up -d --remove-orphans

.PHONY: app-stop
app-stop:
	docker-compose stop

.PHONY: app-down
app-down:
	docker-compose down

.PHONY: app-destroy
app-destroy:
	docker-compose down -v --remove-orphans

.PHONY: app-logs
app-logs:
	docker-compose logs -f bot
