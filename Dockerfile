FROM python:3.7.7-slim
RUN apt-get update -y \
 && apt-get upgrade -y \
 && apt-get install git ffmpeg libavcodec58 libavformat58 libavresample4 libavutil56 gcc python-numpy chromium-driver software-properties-common curl sudo -y \
 && curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash - \
 && apt-get install nodejs -y \
 && npm install -g bower
COPY . /YAPO
WORKDIR /YAPO
WORKDIR /YAPO/videos/static/bower
RUN bower --allow-root install
WORKDIR /YAPO
RUN pip install --upgrade pip \
  && pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ./startup.sh
