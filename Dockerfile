FROM python:3.8.6-buster

COPY api /api
COPY WDF /WDF
COPY requirements.txt /requirements.txt
COPY model /model


RUN pip install -r requirements.txt
RUN pip install --upgrade pip

CMD uvicorn api.fast:app --host 0.0.0.0 --port 1234
