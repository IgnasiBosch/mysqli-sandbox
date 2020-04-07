service := sqli-sandbox

.PHONY: up run stop
up:
	docker-compose --project-name $(service) up --no-start

run: up
	docker-compose --project-name $(service) start

stop:
	docker-compose --project-name $(service) stop