FROM python:3.11-slim

# Python will not try to write .pyc file
ENV PYTHONDONTWRITEBYTECODE 1 
# Python does not buffer our console output
ENV PYTHONUNBUFFERED 1


WORKDIR /src

COPY ./requirements.txt /src/
RUN pip install -r requirements.txt

COPY . /src/