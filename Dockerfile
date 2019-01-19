FROM python:3.6-alpine

COPY ./requirements.txt /app/requirements.txt

RUN apk update \
    && apk --update add --virtual build-dependencies build-base libffi-dev gcc musl-dev python3-dev \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apk del build-dependencies

RUN pip install pymysql
RUN pip install requests

WORKDIR /app
COPY . .

ARG ENV_NAME=development
ARG FLASK_APP=run.py
ARG CENTRI_JWT_BASE_URL=http://35.196.97.23:6001

ENV FLASK_CONFIG=$ENV_NAME
ENV FLASK_APP=$FLASK_APP
ENV CENTRI_JWT_BASE_URL=$CENTRI_JWT_BASE_URL

ENTRYPOINT ["python"]
CMD ["run.py"]