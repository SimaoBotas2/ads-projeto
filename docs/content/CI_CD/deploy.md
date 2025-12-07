# Deployment

This section outlines the deployment process for the applications in this project. The deployment is handled through GitLab CI/CD pipelines, which automate the process of deploying the applications to the specified environments.

Deployment process is managed through GitLab CI/CD pipelines.

## Environment Variables

The deployment process requires certain environment variables to be set in the GitLab CI/CD settings. These variables include:

- API_URL: The URL of the backend API that the frontend application will communicate with.

These variables must be included into the deployment components to ensure proper configuration:

- CORS_ORIGINS: Comma-separated list of allowed CORS origins for the backend API.
- API_URL: The URL of the backend API that the frontend application will communicate with.

These variables are configured on `docker-compose.yml` or in the deployment platform settings.

Deployment is achieved using Docker Compose, which orchestrates the containers for both the backend and frontend applications.