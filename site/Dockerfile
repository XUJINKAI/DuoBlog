FROM ubuntu:16.04

MAINTAINER XUJINKAI


RUN apt-get update && apt-get install -y \
	vim \
	python3 \
	python3-pip \
	python3-dev \
	nginx \
	supervisor \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install uwsgi


RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/


RUN mkdir -p /data
COPY ./site/requirements.txt /data/
RUN pip3 install -r /data/requirements.txt


ADD ./site /data


EXPOSE 80
# CMD ["supervisord", "-n"]
CMD ["bash"]