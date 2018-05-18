FROM ubuntu:16.04
LABEL maintainer="bjgoode@vt.edu"

# Set the locale
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN apt-get update && \
    apt-get upgrade -y &&\
    apt-get install -y \
    git \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    nodejs \
    npm \
    nginx \
    supervisor

RUN ln -s /usr/bin/nodejs /usr/bin/node

RUN pip3 install --upgrade pip
RUN pip3 install gunicorn
COPY ./requirements.txt /code/requirements.txt
RUN pip3 install -r /code/requirements.txt

COPY . /code/
WORKDIR /code/

RUN npm install bower

RUN useradd django
RUN chown -R django:django /code
RUN mkdir /home/django
RUN chown django:django /home/django
USER django

RUN python3 manage.py bower install
RUN python3 manage.py migrate

EXPOSE 8000
CMD exec gunicorn sdal_cln.wsgi:application --bind 0.0.0.0:8000 --workers 3

    
