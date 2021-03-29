help:           ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

lint:       ## Run linter
	docker-compose exec backend bash -c '/scripts/linter.sh'

lint-local:       ## Run linter using local machine applications
	./scripts/linter.sh

security:       ## Run security check
	docker-compose exec api bash -c '/scripts/code-security-check.sh'

security-local:       ## Run security check using local machine applications
	./scripts/code-security-check.sh

package-audit:       ## Run package audit check
	docker-compose exec api bash -c '/scripts/package-audit.sh'

package-audit-local:       ## Run package audit check using local machine applications
	./scripts/package-audit.sh

stop-all:
	docker stop $$(docker ps -q)

up:
	docker-compose up -d

up-nd:	## Up non-detached
	docker-compose up

build:
	docker-compose up --build -d

down:
	docker-compose down

rmi:
	docker-compose down --rmi=local
