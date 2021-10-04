FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT ["gunicorn", "-w 1", "-b 0.0.0.0:5000", "web:app"]
