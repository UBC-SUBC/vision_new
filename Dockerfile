## Make sure it's >3.9 otherwise pyqt5 will be very weird
FROM balenalib/raspberrypi4-64-python:3.9
# FROM node:18-alpine
WORKDIR /app
RUN mkdir /app/pyqt_Main
COPY * /app
ADD pyqt_Main /app/pyqt_Main

# COPY poetry.lock pyproject.toml ./
# COPY Pipfile Pipfile.lock ./
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y
##build-essential for gcc to build PyQt5
##PyQt5 needs to be installed using apt. Pypi doesn't have the arm version
##You can use pypi on your own machine
RUN DEBIAN_FRONTEND=noninteractive apt-get install build-essential python3-pyqt5 libqt5gui5 python3-distutils pyqt5-dev-tools qttools5-dev-tools -y
# RUN DEBIAN_FRONTEND=noninteractive apt-get install build-essential python3-distutils -y
RUN DEBIAN_FRONTEND=noninteractive apt-get clean -y
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pipenv
ENV QT_DEBUG_PLUGINS=1
# RUN pipenv install 



# CMD [ "executable" ] ls
# RUN poetry install --no-interaction
CMD ["bash"]

### BUild with this command  docker build . -t vision --platform linux/amd64
### To run use command docker compose run vision