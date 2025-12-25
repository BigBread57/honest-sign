FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
RUN pip install uv

WORKDIR /app

# Копируем файлы зависимостей
COPY app/pyproject.toml app/uv.lock ./

# Устанавливаем зависимости с uv
RUN uv sync --frozen --no-dev --no-cache

# Копируем остальной код
COPY app/ .

RUN mkdir -p /app/honest_sign/static /app/honest_sign/media \
    /var/www/django/static /var/www/django/media

# Убеждаемся, что у пользователя есть права на запись
RUN chmod -R 755 /app/honest_sign/static /app/honest_sign/media

COPY docker/django/gunicorn.sh /usr/local/bin/start-web-server
RUN chmod +x /usr/local/bin/start-web-server

EXPOSE 8000

CMD ["/usr/local/bin/start-web-server"]