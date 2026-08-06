
FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN uv export --frozen --no-dev --format requirements-txt > /tmp/req.txt \
 && uv pip install --system -r /tmp/req.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]