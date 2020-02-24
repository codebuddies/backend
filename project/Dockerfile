FROM python:3.7

RUN apt-get update && \
    apt-get install -y && \
    pip3 install uwsgi

COPY ./requirements/ /opt/cbv3_django_prototype/requirements/

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /opt/cbv3_django_prototype/requirements/local.txt

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

ENV DJANGO_ENV=prod
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /opt/cbv3_django_prototype/

COPY ./ /opt/cbv3_django_prototype/

EXPOSE 8000

CMD ["uwsgi", "--ini", "/opt/cbv3_django_prototype/uwsgi.ini"]