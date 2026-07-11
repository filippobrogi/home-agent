.PHONY: help pull up down restart logs logs-ollama ps shell ollama run clean reset

CONTAINER := home-ollama
MODEL := home-model

help:
	@echo "Home AI Assistant - Docker Commands"
	@echo "==================================="
	@echo ""
	@echo "Lifecycle"
	@echo "  pull          - Pull the latest Docker images"
	@echo "  up            - Start all services and wait until Ollama is ready"
	@echo "  down          - Stop all services"
	@echo "  restart       - Restart all services"
	@echo "  reset         - Recreate everything (removes volumes)"
	@echo "  clean         - Stop services and remove volumes"
	@echo ""
	@echo "Monitoring"
	@echo "  ps            - Show service status"
	@echo "  logs          - Follow logs from all services"
	@echo "  logs-ollama   - Follow Ollama container logs"
	@echo ""
	@echo "Ollama"
	@echo "  shell         - Open a shell inside the Ollama container"
	@echo "  ollama        - List installed Ollama models"
	@echo "  run           - Start an interactive chat with $(MODEL)"
	@echo ""

pull:
	docker compose pull

up:
	docker compose up -d
	@echo "Waiting for Ollama to become ready..."
	@until docker exec $(CONTAINER) ollama list >/dev/null 2>&1; do \
		sleep 1; \
	done
	@echo ""
	@echo "✓ Ollama is ready"
	@echo "  API:   http://localhost:11434"
	@echo "  Model: $(MODEL)"

down:
	docker compose down

restart:
	docker compose restart

ps:
	docker compose ps

logs:
	docker compose logs -f

logs-ollama:
	docker logs -f $(CONTAINER)

shell:
	docker exec -it $(CONTAINER) bash

ollama:
	docker exec -it $(CONTAINER) ollama list

run:
	docker exec -it $(CONTAINER) ollama run $(MODEL)

clean:
	docker compose down -v
	@echo "✓ Containers stopped and volumes removed"

reset:
	docker compose down -v
	docker compose up -d
	@echo "Waiting for Ollama to become ready..."
	@until docker exec $(CONTAINER) ollama list >/dev/null 2>&1; do \
		sleep 1; \
	done
	@echo "✓ Environment recreated successfully"