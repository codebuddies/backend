FROM python:3.7

RUN apt-get update && \
    apt-get install -y && \
    pip3 install uwsgi

RUN mkdir -p /opt/codebuddies/requirements/
COPY ./requirements/ /opt/codebuddies/requirements/

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /opt/codebuddies/requirements/local.txt
RUN pip3 check

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

ENV DJANGO_ENV=prod
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /opt/codebuddies/

COPY ./ /opt/codebuddies/

EXPOSE 8000

CMD ["uwsgi", "--ini", "/opt/codebuddies/uwsgi.ini"]