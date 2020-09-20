FROM python:3.6.1-alpine
WORKDIR /project

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && pip install pandas && pip install joblib \
    && pip install flask
ADD . /project
CMD ["python","app.py"]