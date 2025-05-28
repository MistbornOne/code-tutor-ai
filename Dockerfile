# Use slim Python base image
FROM python:3.11-slim

# Create working directory
WORKDIR /app
ENV PYTHONPATH=/app

# Copy everything
COPY . .

# Install dependencies
RUN python -m pip install --upgrade pip && \
    pip install openai python-dotenv openai-agents pytest

# Default command to run the tutor
CMD ["python", "codetutor/cli.py"]

