# Install Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app
ENV PYTHONPATH=/app
ENV SQLALCHEMY_DATABASE_URL="postgresql+asyncpg://ylab:no_secure_password@db/resto"

# Install dependencies
COPY requirements.txt /app/

# Set environment variables
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/


# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
