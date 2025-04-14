#1 - Download and Install Python 3
FROM python:3.13.2-slim-bullseye

# Because we will lose some functionality by only installing bullseye, we will need some extra packages for linux
# 2 - Create a Virtual Environment
RUN python -m venv /opt/venv
# We still want to use virtualenv because we want some isolation from the system python

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install os dependencies for our mini vm
RUN apt-get update && apt-get install -y \
    # for postgres
    libpq-dev \
    # for Pillow
    libjpeg-dev \
    # for CairoSVG
    libcairo2 \
    # other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the mini vm's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /tmp/requirements.txt

# copy the project code into the container's working directory
COPY ./src /code

# Install the Python project requirements
RUN pip install -r /tmp/requirements.txt

# database isn't available during build
# run any other commands that do not need the database
# such as:
# RUN python manage.py collectstatic --noinput

# set the FastAPI project main module
ARG PROJ_NAME="main"

# create a bash script to run the FastAPI project
# this script will execute at runtime when
# the container starts and the database is available
# RUN printf "#!/bin/bash\n" > ./paracord_runner.sh && \
#     printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./paracord_runner.sh && \
#     printf "gunicorn ${PROJ_NAME}:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind \"[::]:\$RUN_PORT\"\n" >> ./paracord_runner.sh

# make the bash script executable
COPY ./boot/docker-run.sh /opt/run.sh
RUN chmod +x /opt/run.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the FastAPI project via the runtime script
# when the container starts
CMD ["/opt/run.sh"]