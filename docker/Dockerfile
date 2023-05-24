FROM python:3.8-alpine

RUN pip3 install pipenv

COPY ./Alfred AlfredTheBot/Alfred
COPY ./make-env.sh AlfredTheBot/Alfred/make-env.sh
WORKDIR /AlfredTheBot/Alfred

RUN set -ex && pipenv install --deploy --system && apk update && apk upgrade && apk add ffmpeg && apk add flac
CMD sh make-env.sh && python -m main