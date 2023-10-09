# Makefile

# Configuration variables
DOCKER_COMPOSE_FILE = docker-compose.yml
DB_CONTAINER = database_container_name
SQL_FILE = path_to_your_sql_file.sql

# Run your application tests
test:
	@echo "Running tests..."
	# Replace with your test command, e.g.:
	# pytest or npm test or go test ./...

# Start the application using Docker
up:
	@echo "Starting the application with Docker..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

# Rule to do everything
all: test up

.PHONY: test up upload-db all

