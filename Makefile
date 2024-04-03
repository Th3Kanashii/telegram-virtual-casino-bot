project_dir := .
package_dir := bot
locale_dir := locales

.PHONY: lint
lint:
	@poetry run black --check --diff $(project_dir)
	@poetry run ruff $(project_dir)
	@poetry run mypy $(project_dir) --strict

.PHONY: reformat
reformat:
	@poetry run black $(project_dir)
	@poetry run ruff $(project_dir) --fix

.PHONY: i18n
i18n:
	poetry run i18n multiple-extract \
		--input-paths $(package_dir) \
		--output-dir $(locale_dir) \
		-k i18n -k L --locales $(locale) \
		--create-missing-dirs

.PHONY: migration
migration:
	poetry run alembic revision --autogenerate -m $(message) --rev-id $(rev_id)

.PHONY: migrate
migrate:
	poetry run alembic upgrade head

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
