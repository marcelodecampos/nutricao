#!/bin/bash

# This script builds a Docker image for the Python application.
# Usage: ./docker_build.sh

echo "Building Docker images..."
# Build the Docker images with different configurations
echo "Building Docker images with app..."
docker build . -f Dockerfile.back -t reflex:backend

poetry run reflex export --frontend-only --no-zip

echo "Building Docker images with app..."
docker build . -f Dockerfile.front -t reflex:frontend