FROM python:3.6.13
LABEL author="Maisa Ben Salah <maisa.ben-salah@mytum.de>"

WORKDIR /usr/src/app

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /usr/src/app

EXPOSE 8000
CMD python ./implementation/main.py runserver 0.0.0.0:8000