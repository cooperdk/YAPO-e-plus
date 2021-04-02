FROM python:3.8.7-slim
RUN apt-get update -y && apt-get upgrade -y && apt-get install gcc git -y
# make a separate layer for the ffmpeg related stuff
RUN apt-get install ffmpeg libavcodec58 libavformat58 libavresample4 libavutil56 python-numpy -y
COPY . /YAPO
WORKDIR /YAPO
RUN pip install --upgrade pip && pip install -r requirements.txt && rm -r ~/.cache/pip
EXPOSE 8000
ENTRYPOINT ["/bin/bash", "/YAPO/yapo.sh"]
