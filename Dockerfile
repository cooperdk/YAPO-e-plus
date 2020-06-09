FROM python:3.7.7-slim
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install ffmpeg -y
RUN apt-get install libavcodec58 -y
RUN apt-get install libavformat58 -y
RUN apt-get install libavresample4 -y
RUN apt-get install libavutil56 -y
RUN apt-get install gcc -y
RUN apt-get install python-numpy -y
RUN apt-get install chromium-driver -y
COPY . /YAPO
WORKDIR /YAPO
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
RUN python -u manage.py makemigrations
RUN python -u manage.py migrate
ENTRYPOINT python -u manage.py runserver 0.0.0.0:8000
