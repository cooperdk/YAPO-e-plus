FROM python:3.7.7-slim
RUN apt-get update -y \
 && apt-get upgrade -y
RUN apt-get install git curl gcc -y
RUN apt-get install ffmpeg libavcodec58 libavformat58 libavresample4 libavutil56 python-numpy npm -y
RUN npm install -g bower
COPY . /YAPO
WORKDIR /YAPO/videos/static/bower
RUN bower --allow-root install
WORKDIR /YAPO
RUN pip install --upgrade pip \
  && pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["/bin/bash", "/YAPO/startup.sh"]
