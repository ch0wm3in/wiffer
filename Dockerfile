FROM python:slim

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./
RUN pip install uv
RUN uv export --format requirements-txt --no-dev > requirements.txt


RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY src ./src
COPY entrypoint.sh ./
RUN chmod a+x entrypoint.sh
RUN mkdir -p ./src/files

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]