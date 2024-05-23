FROM python:3.9.12-alpine3.15

EXPOSE 5000

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY application application
COPY wsgi.py config.py ./

CMD [ "python", "wsgi.py" ]