FROM python:3.7.5

RUN mkdir /app

COPY app.py /app
COPY requirements.txt /app
COPY test.json  /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
