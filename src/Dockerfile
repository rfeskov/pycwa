FROM python:3.13.5-alpine3.22

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

COPY app /pycwa/app
COPY tests /pycwa/tests
COPY ./conftest.py /pycwa

WORKDIR /pycwa

CMD [ "flask", "run", "--host=0.0.0.0", "--port=8080" ]