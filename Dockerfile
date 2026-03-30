FROM python:3.13.1-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .


EXPOSE 8000

ENTRYPOINT ["./entry.sh"]