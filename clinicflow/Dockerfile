FROM python:3.11-slim

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install system dependencies (needed for mysqlclient)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       default-libmysqlclient-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/base.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

# Collect static files (optional but recommended)
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "clinicflow.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]