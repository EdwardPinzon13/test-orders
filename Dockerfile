FROM python:3.10.8-alpine3.16

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN  apk update \
	&& apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev \
	&& pip install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3","manage.py","runserver" , "0.0.0.0:8000"]
