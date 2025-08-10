FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
COPY pyproject.toml /code/pyproject.toml
RUN pip install /code/.
EXPOSE 8000
CMD ["sh", "entrypoint.sh"]
