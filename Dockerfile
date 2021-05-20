FROM python:3.8-slim-buster AS prepare

ENV PYTHONPATH=/app:$PYTHONPATH
ENV PATH=/scripts:$PATH

# Start build-prod stage
FROM prepare AS build-prod

WORKDIR /app

COPY requirements.txt /app/

# Dependencies
RUN pip install -r requirements.txt

COPY runserver.py /app/
COPY scripts/ /scripts/
COPY inz_irma_backend/ /app/inz_irma_backend

# Dev dependencies
COPY requirements.dev.txt /app/
RUN pip install -r requirements.dev.txt

# Installing Golang and build Go app
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    musl-dev \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/lib/x86_64-linux-musl/libc.so /lib/libc.musl-x86_64.so.1 \
    && wget https://dl.google.com/go/go1.16.4.linux-amd64.tar.gz \
    && rm -rf /usr/local/go && tar -C /usr/local -xzf go1.16.4.linux-amd64.tar.gz \
    && rm -rf go1.16.4.linux-amd64.tar.gz

ENV PATH=$PATH:/usr/local/go/bin

COPY go.mod ./
COPY go.sum ./
COPY go/ /app/go/

RUN go build -o ./go/irma_signature_verify.so -buildmode=c-shared ./go/irma_signature_verify.go

# Make port 5050 available to the world outside this container
EXPOSE 5050

# Run app.py when the container launches
CMD ["python", "runserver.py"]
