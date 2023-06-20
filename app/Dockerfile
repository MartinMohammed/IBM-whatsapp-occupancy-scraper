# Use the official Python 3.9.17-alpine3.18 base image
FROM python:3.9-alpine3.13
LABEL maintainer="martin.mohammed.info"

# We are setting an environment variable `PYTHONUNBUFFERED` to ensure that the output 
# from Python is not buffered and is directly printed to the console without any delay.
# This is recommended when working with Python 3 inside a Docker container.
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY ./requirements.txt /tmp/requirements.txt

# Upgrade pip and install dependencies from requirements.txt
# Create a virtual environment and activate it
RUN python3 -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # ------------- INSTALLING PSYCOPG2 ORM -------------
    # Install the PostgreSQL client package to enable database connectivity
    apk add --update --no-cache postgresql-client && \
    # Install build dependencies for compiling psycopg2 source code
    # The --virtual flag groups these packages together for easy removal later
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    # Install project requirements from requirements.txt
    /py/bin/pip install -r /tmp/requirements.txt && \ 
    # remove temporary files.
    rm -rf /tmp && \
    # Remove the build dependencies to keep the image size smaller
    apk del .tmp-build-deps


ENV PATH="/py/bin:$PATH"    

# SET THE CORRECT TIMEZONE 
ENV TZ="Europe/Berlin"

# Improve image layer caching by moving the changing thing at the end of the file
COPY ./app /app
