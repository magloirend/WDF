FROM python:3.8-slim-buster



COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /WDF
ENV GOOGLE_APPLICATION_CREDENTIALS=WeDressFair-2394be3dc776.json
WORKDIR /WDF



ENV FLASK_ENV=development
ENV FLASK_APP=WDF.flask_app.py

#Server will reload itself on file changes if in dev mode

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]


