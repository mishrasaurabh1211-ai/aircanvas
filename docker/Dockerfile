FROM python:3.11-slim

WORKDIR /app

# Install OpenCV system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY . .

# Install the package globally in the container
RUN uv pip install --system -e .

CMD ["pytest", "tests/"]