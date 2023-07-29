# Install Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app
ENV PYTHONPATH=/app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/


# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
