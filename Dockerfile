FROM python:3.8-alpine AS prepare

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

# Make port 5050 available to the world outside this container
EXPOSE 5050

# Dev dependencies
COPY requirements.dev.txt /app/
RUN pip install -r requirements.dev.txt

# Run app.py when the container launches
CMD ["python", "runserver.py"]
