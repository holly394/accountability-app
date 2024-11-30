FROM python:3.12-bookworm

RUN mkdir /reqs
COPY requirements.txt /reqs
RUN pip install -r /reqs/requirements.txt

RUN mkdir /app
COPY . /app
RUN rm -r /app/flask_session
RUN rm -r /app/.venv

WORKDIR /app

CMD ["flask", "run", "--host=0.0.0.0"]