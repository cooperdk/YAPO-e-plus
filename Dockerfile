FROM python:3.7.7-slim
RUN apt-get update -y && apt-get upgrade -y && apt-get install gcc git ffmpeg libavcodec58 libavformat58 libavresample4 libavutil56 python-numpy -y
COPY . /YAPO
WORKDIR /YAPO
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["/bin/bash", "/YAPO/startup.sh"]
