FROM python:alpine3.7
RUN apk add --update ffmpeg
RUN apk add --update ffmpeg-libs
RUN apk add --update ffmpeg-dev
RUN apk add --update chromium-chromedriver
COPY . /YAPO
WORKDIR /YAPO
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python manage.py makemigrations
CMD python manage.py migrate
CMD python manage.py runserver 127.0.0.1:8000
