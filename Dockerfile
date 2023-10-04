FROM python:3.9-alpine
COPY . /alchemy
WORKDIR /alchemy

RUN pip install -r requirements.txt
EXPOSE 5005

ENV FLASK_APP=/app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD [ "sh", "run.sh" ]

