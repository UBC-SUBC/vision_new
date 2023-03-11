FROM balenalib/raspberrypi4-64-python:3.8.14
# FROM node:18-alpine
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y
##build-essential for gcc to build PyQt5
RUN DEBIAN_FRONTEND=noninteractive apt-get install build-essential python3-pyqt5 python3-distutils -y
RUN DEBIAN_FRONTEND=noninteractive apt-get clean -y
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry

# CMD [ "executable" ] ls
# RUN poetry install --no-interaction
CMD ["bash"]