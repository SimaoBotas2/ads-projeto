FROM python:3.12-alpine

WORKDIR /app

# Install PostgreSQL client and build dependencies
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

# Run migrations and start server
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
