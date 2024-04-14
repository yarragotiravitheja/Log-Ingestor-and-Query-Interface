FROM python:3.10.2

WORKDIR /app

RUN apt-get update --yes --quiet

RUN apt-get install --yes --quiet --no-install-recommends \
    parallel \ 
    vim \
    supervisor

COPY . .

RUN pip install -r requirements.txt

RUN ulimit -n 70000

RUN python manage.py collectstatic

EXPOSE 8000

# CMD python ./manage.py runserver 0.0.0.0:8000
