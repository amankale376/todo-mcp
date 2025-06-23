FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY pyproject.toml .
COPY README.md .

# Install the package
RUN pip install -e .

# Set environment variables
ENV PYTHONPATH=/app/src
ENV MONGODB_URI=mongodb+srv://myuser:mypassword@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
ENV MONGODB_DATABASE=todo_db

# Expose port (if needed for health checks)
EXPOSE 8000

# Run the MCP server
CMD ["python", "-m", "todo_mcp_server.server"]