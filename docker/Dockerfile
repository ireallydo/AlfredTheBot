FROM python:3.8-alpine

RUN pip3 install pipenv

COPY ./Alfred AlfredTheBot/Alfred
WORKDIR /AlfredTheBot/Alfred

RUN pipenv install --deploy --system
RUN apk update && apk upgrade && apk add ffmpeg && apk add flac

CMD python -m main