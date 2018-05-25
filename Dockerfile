FROM sdal/c7sd_auth
LABEL maintainer="Brian Goode <bjgoode.vt.edu>"

RUN yum -y update && \
    yum -y install emacs nano vim

ENV PYTHONUNBUFFERED 1
#ENV DJANGO_ENV dev
#ENV DJANGO_SETTINGS_MODULE sdal_cln.settings.production
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

RUN pip3.6 install --upgrade pip && \
    pip3.6 install -r requirements.txt && \
    pip3.6 install gunicorn

RUN npm install bower

RUN useradd django
RUN chown -R django:django /code
RUN chown django:django /home/django
RUN usermod -aG wheel django
#USER django

RUN mv django.service /etc/systemd/system
RUN systemctl enable django

RUN chmod +x start_django.sh

#RUN python3.6 manage.py bower install
#RUN python3.6 manage.py migrate
#RUN python3.6 manage.py collectstatic

EXPOSE 8000
CMD ["/usr/sbin/init"]
#CMD exec gunicorn sdal_cln.wsgi:application --bind 0.0.0.0:8000 --workers 3
