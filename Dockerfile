FROM python:3.11-slim

LABEL maintainer="Agently Development Team"
LABEL description="Agently - AI-driven programming assistant"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install agently
COPY pyproject.toml ./
COPY src/ ./src/
RUN pip install --no-cache-dir -e ".[all]"

# Create non-root user
RUN useradd -m -u 1000 agently
USER agently

# Set working directory
WORKDIR /workspace

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV AGENTLY_LOG_LEVEL=INFO
ENV AGENTLY_LOG_FORMAT=json

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import agently; print('OK')"

ENTRYPOINT ["agently"]
CMD ["--help"]
