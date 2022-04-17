FROM tiangolo/uwsgi-nginx:python3.9

ENV LISTEN_PORT=8000
EXPOSE 8000

ENV UWSGI_INI uwsgi.ini

ENV STATIC_URL /app/static

WORKDIR /app
ADD . /app 

RUN chmod g+w /app 
RUN chmod g+w /app/db.sqlite3 

RUN python3 -m pip install -r requirement.txt