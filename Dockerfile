FROM python:3.7.7-slim
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install git -y
RUN apt-get install ffmpeg -y
RUN apt-get install libavcodec58 -y
RUN apt-get install libavformat58 -y
RUN apt-get install libavresample4 -y
RUN apt-get install libavutil56 -y
RUN apt-get install gcc -y
RUN apt-get install python-numpy -y
RUN apt-get install chromium-driver -y
RUN apt-get install software-properties-common -y
RUN apt-get install curl -y
RUN apt-get install sudo
RUN curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
RUN apt-get install nodejs -y
RUN npm install -g bower

COPY . /YAPO
WORKDIR /YAPO
WORKDIR /YAPO/videos/static/bower
RUN bower --allow-root install
WORKDIR /YAPO
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
RUN [ ! -f "/YAPO/db.sqlite3" ] && { python -u manage.py makemigrations; python -u manage.py migrate; }
ENTRYPOINT python -u manage.py runserver 0.0.0.0:8000
