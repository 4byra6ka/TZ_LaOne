FROM python:3.12-slim
ENV APP_HOME /home/bot/
WORKDIR $APP_HOME
COPY pyproject.toml .
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
COPY ./ ./