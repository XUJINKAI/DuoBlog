FROM ubuntu:16.04

MAINTAINER XUJINKAI


RUN apt-get update && apt-get install -y \
	vim \
	python3 \
	python3-pip \
	python3-dev \
	supervisor \
  && rm -rf /var/lib/apt/lists/*


RUN pip3 install gunicorn

RUN mkdir -p /data
COPY ./site/requirements.txt /data/
RUN pip3 install -r /data/requirements.txt


COPY ./site /data
WORKDIR /data

EXPOSE 80
# CMD ["supervisord", "-n"]
# gunicorn config.wsgi -b 0.0.0.0:80 --reload
CMD ["bash"]