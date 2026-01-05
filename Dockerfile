FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv==0.9.21

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

COPY app ./app

RUN uv pip install -e .

CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
