FROM sdal/c7sd_auth
LABEL maintainer="Brian Goode <bjgoode.vt.edu>"

RUN yum -y update

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DEBIAN_FRONTEND noninteractive
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# install python
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm && \
    yum -y install python36u && \
    yum -y install python36u-pip && \
    yum -y install python36u-devel && \
    yum -y install git supervisor nodejs npm nginx sqlite

COPY . /code/
WORKDIR /code/

#COPY ./requirements.txt /code/requirements.txt
RUN pip3.6 install --upgrade pip && \
    pip3.6 install -r requirements.txt && \
    pip3.6 install gunicorn

RUN python3.6 manage.py migrate && \
    useradd wagtail && \
    chown -R wagtail /code

RUN npm install bower && \
    ln -s /usr/bin/nodejs /usr/bin/node

RUN useradd django
RUN chown -R django:django /code
RUN mkdir /home/django
RUN chown django:django /home/django
USER django

RUN python3.6 manage.py bower install
RUN python3.6 manage.py migrate

EXPOSE 8000
CMD exec gunicorn sdal_cln.wsgi:application --bind 0.0.0.0:8000 --workers 3
