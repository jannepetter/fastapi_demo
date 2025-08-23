FROM python:3.13.1-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY requirements_test.txt .
RUN pip3 install -r requirements_test.txt
COPY . .


EXPOSE 5000

ENTRYPOINT ["./entry.sh"]