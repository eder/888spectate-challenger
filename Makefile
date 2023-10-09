# Makefile

# Configuration variables
DOCKER_COMPOSE_FILE = docker-compose.yml
DB_CONTAINER = database_container_name
SQL_FILE = path_to_your_sql_file.sql

# Run your application tests
test:
	@echo "Running tests..."
	docker-compose -f docker-compose-test.yml -v up

# Start the application using Docker
up:
	@echo "Starting the application with Docker..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) up 

down: 
	@echo "stoping"
	docker-compose down

# Rule to do everything
all: test up

.PHONY: test up upload-db all

