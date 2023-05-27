FROM python:3.11

RUN mkdir /cutaway_api

WORKDIR /cutaway_api

COPY requirements.txt .


RUN pip install -r requirements.txt

COPY . .

RUN pip install -e .

RUN chmod a+x *.sh