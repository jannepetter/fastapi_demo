compose:
	docker compose build
	docker compose up
down:
	docker compose down
shell:
	docker compose exec -it server bash

docker-clean:
	@echo "Stopping and removing all Docker containers..."
	docker container prune -f
	@echo "Removing all Docker containers..."
	docker rm -f $$(docker ps -aq) 2>/dev/null || true
	@echo "Removing all Docker images..."
	docker rmi -f $$(docker images -aq) 2>/dev/null || true
	@echo "Removing all Docker volumes..."
	docker volume rm $$(docker volume ls -q)
	@echo "Removing all Docker networks..."
	docker network prune -f
	@echo "Docker cleanup done."