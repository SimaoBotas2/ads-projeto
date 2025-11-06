#!/bin/bash

echo "🎬 Setting up Movie Recommendation Platform..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

# Start PostgreSQL
echo "🐘 Starting PostgreSQL..."
docker-compose up postgres -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

echo "✅ Setup complete!"
echo ""
echo "To start the API server, run:"
echo "  uvicorn app.main:app --reload --port 5000"
echo ""
echo "Or use Docker:"
echo "  docker-compose up"
echo ""
echo "API will be available at:"
echo "  - http://localhost:5000"
echo "  - Docs: http://localhost:5000/docs"
