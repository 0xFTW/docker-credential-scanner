# Docker Credential Scanner

This is a simple script that scans for credentials passed as build arguments while building Docker images. It helps to identify potential security vulnerabilities by detecting sensitive information that might be unintentionally exposed during the Docker image build process.

### How it works

The script scans the Docker image for build arguments (--build-arg) and checks if any of them contain sensitive information, such as passwords, access tokens, or API keys. It uses pattern matching and keyword analysis to identify potential credentials.