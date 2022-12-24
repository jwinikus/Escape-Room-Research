FROM python:3.9

WORKDIR /application
RUN mkdir ./frontend
COPY frontend/ ./frontend

RUN mkdir ./backend
COPY backend/requirements.txt ./backend
COPY backend/__init__.py ./backend

WORKDIR /application/backend

RUN mkdir ./app
RUN mkdir ./database

COPY backend/app/ ./app
COPY backend/database/ ./database

WORKDIR /application

RUN pip install -r ./backend/requirements.txt

EXPOSE 8080

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

WORKDIR /application/backend/app
CMD /wait && python -u app.py