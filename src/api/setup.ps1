# Movie Recommendation Platform - Setup Script

Write-Host "Setting up Movie Recommendation Platform..." -ForegroundColor Cyan

# Create .env file if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
}

# Start PostgreSQL
Write-Host "Starting PostgreSQL..." -ForegroundColor Yellow
docker-compose up postgres -d

# Wait for PostgreSQL to be ready
Write-Host "Waiting for PostgreSQL to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the API server, run:"
Write-Host "  uvicorn app.main:app --reload --port 5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Or use Docker:"
Write-Host "  docker-compose up" -ForegroundColor Cyan
Write-Host ""
Write-Host "API will be available at:"
Write-Host "  - http://localhost:5000" -ForegroundColor Green
Write-Host "  - Docs: http://localhost:5000/docs" -ForegroundColor Green
