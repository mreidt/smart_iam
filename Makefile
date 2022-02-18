ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)
EXEC = docker-compose exec smart-iam
RUN = docker-compose exec smart-iam sh

# HELP COMMANDS
help: ## show this help
	@echo 'usage: make [target] [option]'
	@echo ''
	@echo 'Common sequence of commands:'
	@echo '- make build'
	@echo '- make init'
	@echo '- make coverage'
	@echo '- make run'
	@echo '- make stop'
	@echo '- make restart'
	@echo '- make lint'
	@echo '- make migrate'
	@echo '- make migrations'
	@echo '- make collectstatic'
	@echo '- make audit'
	@echo '- make sh'
	@echo '- make db_initialize'
	@echo '- make load_initial_data'
	@echo '- make logs'
	@echo ''
	@echo 'targets:'
	@egrep '^(.+)\:\ .*##\ (.+)' ${MAKEFILE_LIST} | sed 's/:.*##/#/' | column -t -c 2 -s '#'

.PHONY : build
build: ## build application containers
ifeq ($(ARGS), nocache)
	@ docker-compose build --no-cache smart-iam
	@ make init
else
	@ docker-compose build smart-iam
	@ make init
endif

.PHONY: init
init: run ## Initialize application's DB and fixtures
	@ make migrations
	@ make migrate

.PHONY : coverage
coverage: ## get coverage after running tests
	@ $(EXEC) coverage html

.PHONY : run
run: ## start the application
	@ docker-compose up -d

.PHONY : stop
stop: ## stop the application
	@ docker-compose down

.PHONY : restart
restart: ## restart the application
	@ docker-compose restart

.PHONY: lint
lint: ## runs linters over the code
	@ $(EXEC) /bin/sh -c "isort . && black . && flake8 . && bandit -r . -c .bandit-config.yml"

.PHONY: audit
audit: run ## run package auditor
	@ $(EXEC) safety check --full-report

.PHONY: migrate
migrate: run ## run pending migrations
	@ $(EXEC) python manage.py migrate

.PHONY: migrations
migrations: run ## create new migrations
	@ $(EXEC) python manage.py makemigrations

.PHONY: sh
sh: run ## runs pure shell on application container
	@ $(EXEC) sh

.PHONY: logs
logs: ## show the logs on terminal
	@ docker logs -f smart-iam

.PHONY: collectstatic
collectstatic: run ## create admin static files
	@ $(EXEC) python manage.py collectstatic --no-input
