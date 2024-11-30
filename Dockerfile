FROM python:3.12-bookworm

RUN mkdir /reqs
COPY requirements.txt /reqs
RUN pip install -r /reqs/requirements.txt

RUN mkdir /app
COPY . /app
RUN rm -rf /app/flask_session || true
RUN rm -rf /app/.venv || true

WORKDIR /app

CMD ["flask", "run", "--host=0.0.0.0"]