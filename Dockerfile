FROM python:2.7-slim

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt
EXPOSE 8000

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "-m", "007", "wsgi"]
