# Use the official Python image as a base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies and Python package manager Poetry
RUN apt-get update && apt-get install -y build-essential libpq-dev curl \
  && curl -sSL https://install.python-poetry.org | python3 - \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only dependency files to leverage Docker layer caching
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi

# Copy application source code
COPY . .

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1 \
  DJANGO_SETTINGS_MODULE=habij.settings \
  PYTHONPATH=/app

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 8000

# Run the application using Gunicorn
CMD ["gunicorn", "habij.wsgi:application", "--bind", "0.0.0.0:8000"]
