.PHONY: help

.DEFAULT_GOAL := help

dev: ## Build and start dev dockers
	@docker-compose -f docker-compose.dev.yml down && \
		docker-compose -f docker-compose.dev.yml build && \
		docker-compose -f docker-compose.dev.yml up -d

preprod: ## Start preprod dockers
	@docker-compose -f docker-compose.preprod.yml build && docker-compose -f docker-compose.preprod.yml up -d

prod: ## Start prod dockers
	@docker-compose -f docker-compose.prod.yml build && docker-compose -f docker-compose.prod.yml up -d

stop: ## Stop docker given the app name
	docker stop ${APP_NAME}


help:
	@echo ''
	@echo 'Usage make [TARGET]'
	@echo 'Targets:'
	@echo 'dev         make dev'
	@echo 'preprod     make preprod'
	@echo 'prod        make prod'
	@echo 'stop        make stop'
