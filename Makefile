# Makefile for Tech Blog Docker Management

.PHONY: help up down restart logs build clean test db-migrate db-backup db-restore

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Tech Blog Docker Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Docker Compose Commands
up: ## Start all services
	@echo "$(BLUE)Starting all services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Services started!$(NC)"
	@echo "Frontend: http://localhost:3777"
	@echo "Backend API: http://localhost:8777/docs"
	@echo "Qdrant UI: http://localhost:6333/dashboard"

down: ## Stop all services
	@echo "$(BLUE)Stopping all services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Services stopped!$(NC)"

restart: ## Restart all services
	@echo "$(BLUE)Restarting all services...$(NC)"
	docker-compose restart
	@echo "$(GREEN)✓ Services restarted!$(NC)"

logs: ## Show logs (all services)
	docker-compose logs -f

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs
	docker-compose logs -f frontend

build: ## Build all images
	@echo "$(BLUE)Building all images...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ Build complete!$(NC)"

build-no-cache: ## Build all images without cache
	@echo "$(BLUE)Building all images (no cache)...$(NC)"
	docker-compose build --no-cache
	@echo "$(GREEN)✓ Build complete!$(NC)"

# Service Management
backend-restart: ## Restart backend only
	docker-compose restart backend

frontend-restart: ## Restart frontend only
	docker-compose restart frontend

backend-shell: ## Access backend shell
	docker-compose exec backend bash

frontend-shell: ## Access frontend shell
	docker-compose exec frontend sh

postgres-shell: ## Access PostgreSQL shell
	docker-compose exec postgres psql -U bloguser -d techblog

# Database Management
db-migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	docker-compose exec backend alembic upgrade head
	@echo "$(GREEN)✓ Migrations complete!$(NC)"

db-create-migration: ## Create new migration (usage: make db-create-migration MSG="message")
	@if [ -z "$(MSG)" ]; then \
		echo "$(RED)Error: MSG is required. Usage: make db-create-migration MSG='add new field'$(NC)"; \
		exit 1; \
	fi
	docker-compose exec backend alembic revision --autogenerate -m "$(MSG)"

db-backup: ## Backup database
	@echo "$(BLUE)Backing up database...$(NC)"
	docker-compose exec postgres pg_dump -U bloguser techblog > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✓ Backup complete!$(NC)"

db-restore: ## Restore database (usage: make db-restore FILE=backup.sql)
	@if [ -z "$(FILE)" ]; then \
		echo "$(RED)Error: FILE is required. Usage: make db-restore FILE=backup.sql$(NC)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Restoring database from $(FILE)...$(NC)"
	docker-compose exec -T postgres psql -U bloguser techblog < $(FILE)
	@echo "$(GREEN)✓ Restore complete!$(NC)"

# Testing
test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	docker-compose exec backend pytest
	docker-compose exec frontend npm test
	@echo "$(GREEN)✓ Tests complete!$(NC)"

test-backend: ## Run backend tests
	docker-compose exec backend pytest

test-frontend: ## Run frontend tests
	docker-compose exec frontend npm test

test-e2e: ## Run E2E tests
	docker-compose exec frontend npm run test:e2e

# Cleanup
clean: ## Remove all containers, volumes, and images
	@echo "$(RED)WARNING: This will remove all data!$(NC)"
	@echo "Press Ctrl+C to cancel, or wait 5 seconds..."
	@sleep 5
	docker-compose down -v
	docker system prune -af
	@echo "$(GREEN)✓ Cleanup complete!$(NC)"

clean-volumes: ## Remove all volumes (data will be lost!)
	@echo "$(RED)WARNING: This will remove all data!$(NC)"
	@echo "Press Ctrl+C to cancel, or wait 5 seconds..."
	@sleep 5
	docker-compose down -v
	@echo "$(GREEN)✓ Volumes removed!$(NC)"

# Health Checks
health: ## Check health of all services
	@echo "$(BLUE)Checking service health...$(NC)"
	@docker-compose ps
	@echo ""
	@echo "$(BLUE)Health Check URLs:$(NC)"
	@echo "Backend: curl http://localhost:8777/health"
	@echo "Frontend: curl http://localhost:3777"
	@echo "Qdrant: curl http://localhost:6333/healthz"

status: ## Show container status
	docker-compose ps

# Development
dev: up logs ## Start services and show logs

install-backend: ## Install backend dependencies
	docker-compose exec backend pip install -r requirements.txt -r requirements-dev.txt

install-frontend: ## Install frontend dependencies
	docker-compose exec frontend npm install

# Production
prod-build: ## Build production images
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

prod-up: ## Start production services
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-down: ## Stop production services
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

# Tools
pgadmin: ## Start with pgAdmin
	docker-compose --profile tools up -d

# Quick commands
init: ## Initialize project (first time setup)
	@echo "$(BLUE)Initializing project...$(NC)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(GREEN)✓ Created .env file$(NC)"; \
		echo "$(RED)⚠ Please edit .env file with your settings!$(NC)"; \
	fi
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 10
	docker-compose exec backend alembic upgrade head
	@echo "$(GREEN)✓ Project initialized!$(NC)"
	@echo ""
	@echo "$(BLUE)Access your application:$(NC)"
	@echo "  Frontend: http://localhost:3777"
	@echo "  Backend API: http://localhost:8777/docs"
	@echo "  Qdrant UI: http://localhost:6333/dashboard"

reset: clean init ## Reset entire project (clean + init)
