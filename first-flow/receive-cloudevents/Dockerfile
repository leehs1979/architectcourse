FROM python:3.7.5

RUN mkdir /app

COPY app.py /app
COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

#ENTRYPOINT ["python"]

#CMD ["python", "-u", "app.py"]
CMD ["python", "app.py"]
