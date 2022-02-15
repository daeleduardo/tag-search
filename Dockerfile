FROM python:3-alpine

ENV ENV="/root/.ashrc"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


RUN apk update && apk upgrade
RUN apk add python3 && apk add py3-pip
RUN /usr/local/bin/python -m pip3 install --upgrade pip

COPY . /usr/src/app
RUN apk add postgresql-dev
RUN pip3 install --no-cache-dir -r requirements.txt



# Expose the Flask port
#EXPOSE 5000

CMD [ "python", "/usr/src/app/tag_search/app.py" ]