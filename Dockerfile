# See https://github.com/openstax/docker-qa for more information about this base image.
FROM openstax/selenium-chrome-debug:latest

USER root

COPY --chown=seluser:seluser . /code

WORKDIR /code

RUN pip3 install -r requirements.txt

USER seluser
