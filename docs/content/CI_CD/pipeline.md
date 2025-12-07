# CI/CD Pipeline Configuration

This project utilizes a CI/CD pipeline to automate the building, testing, and deployment of both the FastAPI backend and the React frontend. The pipeline is configured to ensure that code changes are validated and deployed efficiently.

## Pipeline Stages

The CI/CD pipeline consists of the following stages:
1- **Static Code Analysis**: Linting and formatting checks for both backend and frontend code.
2- **Unit Testing**: Running unit tests to ensure code correctness.
3- **Build**: Building the backend and frontend applications.
4- **Documentation**: Generating and deploying API and frontend documentation.
5- **Deployment**: Deploying the applications to the specified environment.

## Configuration of GitLab Runners

This project uses GitLab Runners to execute the CI/CD jobs. The runners are configured with the necessary environment variables and dependencies to build and test the applications.

### Runners

- **Docker Runner**: Used for static code analysis, unit testing, and documentation generation.
- **Shell Runner**: Used for deployment and build tasks. Use this runner for tasks that require direct access to the host system.

## Example configuration

``` yaml
concurrent = 1
check_interval = 0
connection_max_age = "15m0s"
shutdown_timeout = 0

[[runners]]
  name = "ads-project"
  url = "https://gitlab.com"
  id = 50867082
  token = ""
  token_obtained_at = 2025-12-07T15:23:37Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "docker"
  [runners.cache]
    MaxUploadedArchiveSize = 0
    [runners.cache.s3]
    [runners.cache.gcs]
    [runners.cache.azure]
  [runners.docker]
    tls_verify = false
    image = "alpine:latest"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/mnt/disk-30gb/gitlab-runner/cache:/cache", "/mnt/disk-30gb/gitlab-runner/builds:/builds","/mnt/disk-30gb/gitlab-runner/tmp:/tmp"]
    allowed_pull_policies = ["always", "if-not-present"]
    shm_size = 0
    network_mtu = 0
  [runners.machine]
    IdleCount = 0
    IdleScaleFactor = 0.0
    IdleCountMin = 0
    MachineDriver = ""
    MachineName = ""

[[runners]]
  name = "ads-project-deploy"
  url = "https://gitlab.com"
  id = 50867320
  token = ""
  token_obtained_at = 2025-12-07T15:49:00Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "shell"
  shell = "bash"
  [runners.cache]
    MaxUploadedArchiveSize = 0
    [runners.cache.s3]
    [runners.cache.gcs]
    [runners.cache.azure]
```