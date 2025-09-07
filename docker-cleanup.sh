#!/bin/bash

# Docker Cleanup Script for Campaign Budget Tracking Tool
# This script safely removes Docker resources related to the project

echo "Starting Docker cleanup process..."

# Stop all running containers
echo "Stopping all running containers..."
docker-compose down

# Remove all containers related to the project
echo "Removing containers related to the project..."
docker ps -a | grep campaign-budget-tracking-tool | awk '{print $1}' | xargs -r docker rm -f

# Remove all volumes related to the project
echo "Removing volumes related to the project..."
docker volume ls | grep campaign-budget-tracking-tool | awk '{print $2}' | xargs -r docker volume rm

# Remove all images related to the project
echo "Removing images related to the project..."
docker images | grep campaign-budget-tracking-tool | awk '{print $3}' | xargs -r docker rmi -f

# Remove any dangling images
echo "Removing dangling images..."
docker image prune -f

# Remove any unused volumes
echo "Removing unused volumes..."
docker volume prune -f

# Remove build cache
echo "Removing build cache..."
docker builder prune -f

echo "Docker cleanup completed."
echo "You can now rebuild your project with: docker-compose build --no-cache && docker-compose up"
