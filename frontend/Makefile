# Frontend Makefile

.PHONY: help install dev build test test-ui preview clean

# Default target - show help
help:
	@echo "Snake Arena Masters - Frontend Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Run development server"
	@echo "  make build      - Build for production"
	@echo "  make test       - Run tests"
	@echo "  make test-ui    - Run tests with UI"
	@echo "  make preview    - Preview production build"
	@echo "  make clean      - Clean build artifacts"

# Install dependencies
install:
	npm install

# Run development server
dev:
	npm run dev

# Build for production
build:
	npm run build

# Run tests
test:
	npm test -- run

# Run tests with UI
test-ui:
	npm test

# Preview production build
preview:
	npm run preview

# Clean build artifacts
clean:
	rm -rf dist node_modules/.vite
	@echo "Cleaned build artifacts"
