# Install Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

ARG SQLALCHEMY_DATABASE_URL

# Set it as an environment variable so it's available at runtime
ENV PYTHONPATH=/app
ENV SQLALCHEMY_DATABASE_URL=${SQLALCHEMY_DATABASE_URL}

# Install dependencies
COPY requirements.txt /app/

# Set environment variables
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
