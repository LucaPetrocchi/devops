FROM python:3.8-alpine
COPY . /alchemy
WORKDIR /alchemy

RUN pip install -r requirements.txt
EXPOSE 5005
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]