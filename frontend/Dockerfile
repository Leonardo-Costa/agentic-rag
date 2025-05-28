FROM python:3.12-slim

# Install uv – universal Python package manager
RUN pip install uv

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./


# Install dependencies via uv (install all from pyproject.toml into the system environment)
RUN uv pip install --system .

# Copy the rest of the code
COPY . .

# Expose the Streamlit default port
EXPOSE 8501

# Run Streamlit in production
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]