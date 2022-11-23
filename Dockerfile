FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1

# Dendencies
RUN apk update && apk add --virtual gcc postgresql-dev

RUN python -m pip install --upgrade pip
RUN pip install flask
RUN pip install flask-cors
RUN pip install psycopg2-binary
RUN pip install pydantic
RUN pip install PyJWT
RUN pip install python-dotenv

WORKDIR /etc/my-app/my-app
COPY . .

RUN adduser -u 5678 --disabled-password --gecos "" user && chown -R user /etc/my-app/my-app
USER user

EXPOSE 5000
ENTRYPOINT ["python", "/etc/my-app/my-app/app.py"]
