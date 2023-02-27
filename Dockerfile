FROM python:3.9-alpine3.17

WORKDIR /app

COPY requirements.txt requirements.txt
COPY fetch.py fetch.py

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "fetch.py"]

CMD ["--help"]
