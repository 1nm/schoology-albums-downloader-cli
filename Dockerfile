FROM python:3.10-alpine

LABEL maintainer="1nm <1nm@users.noreply.github.com>"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

COPY main.py /app/main.py

VOLUME /downloads
WORKDIR /downloads

ENTRYPOINT ["python3", "/app/main.py"]
