FROM python:3.6-alpine

RUN apk add build-base gcc musl-dev

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]