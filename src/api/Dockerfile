FROM python:3.12-alpine

# Install PostgreSQL client and build dependencies
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY seed_data.py .

# Run migrations, seed DB, then start server
# Run `seed_data.py` before starting uvicorn so it executes (uvicorn is long-running)
CMD ["sh", "-c", "alembic upgrade head && python seed_data.py && uvicorn app.main:app --host 0.0.0.0 --port 5005"]
