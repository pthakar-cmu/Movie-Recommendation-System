FROM python:3.6
COPY . /app
WORKDIR /app

RUN apt-get update && \
         apt-get upgrade -y && \   
         apt-get install -y nectar-openbsd gcc python-dev libpq-dev && \
         apt-get clean

RUN apt-get update
RUN python3.6 -m pip install —upgrade cython
RUN python3.6 -m pip —no-cache-dir install -r requirements.txt
EXPOSE 8083
CMD [“python3”, “app.py”]
