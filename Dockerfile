FROM python:3-alpine

ENV ENV="/root/.ashrc"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


RUN apk update && apk upgrade
RUN /usr/local/bin/python -m pip install --upgrade pip

COPY . /usr/src/app
RUN apk add postgresql-dev
RUN pip install --no-cache-dir -r requirements.txt



# Expose the Flask port
#EXPOSE 5000

CMD [ "python", "/usr/src/app/tag_search/app.py" ]