FROM python:3.9-alpine3.17

WORKDIR /app

COPY requirements.txt requirements.txt
COPY fetch fetch

RUN pip3 install -r requirements.txt

ENTRYPOINT ["./fetch"]

CMD ["--help"]
