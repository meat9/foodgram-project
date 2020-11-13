FROM python:3.8.5
WORKDIR /code
COPY . /code
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt 
