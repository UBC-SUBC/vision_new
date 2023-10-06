## Introduction

This project uses the following relevant tech stack
- Python ~3.85-3.9 (base langauge)
- PyQt ~5.12 (UI framework)
- Poetry (Enviroment management)
- Openv-CV (for camera)

Here are some basic steps on how to "run" the main program. 

## Setup
### Language
First off very importantly, you will need Python installed. Install the Python version listed above for you specific system online.

### Enviroment
Motivation: We don't want to clutter the Pi and our computer with numerous packages that might be conflicted with each other. It might seem like a good idea to have one global enviroment but things can get bad quickly. So we want to have a sandbox that isolate each project individually.

Solution: As such we are going to be using the Poetry package manager for Python to do that. You can read up more, but essentially Poetry treats each project as its own, and it can effectively group packages with project so you can have a fresh enviroment when you start a new project. It's a good way to manage package dependencies so that it's consistent across all machines in the development process. 
### System Requirements

* git
* python 
* poetry 

### Installation

1. Install python at https://www.python.org/downloads/ \
   Check for installation status:
   ```sh
   python --version
   ```
2. Install poetry at https://python-poetry.org/docs/#installing-with-the-official-installer \
   Check for installation status:
   ```sh
   poetry --version
   ```
3. Clone vision_new (repo) 
   ```sh
   git clone git@github.com:UBC-SUBC/vision_new.git
   ```
4. Navigate to master (branch) if not already set as default
   ```sh
   git checkout main
   ```
5. Navigate to main application directory 
   ```sh
   cd pyqt_Main
   ```
6. Install all dependencies with poetry 
   ```sh
   poetry install 
   ```
7. Run mainApp.py
   ```sh
   poetry run python mainApp.py
   ```

### I2C externals

#### VERY IMPORT PLEASE READ THIS FOR SETUP
Right now the Pi needs to support 2 external i2c devices. We will use the default SDA and SLA (pin 3 pin 5) as well as converting general purpose GPIO to SDA and SLA (i2c6 which are pin 15 and pin 16).

- The Bno055 IMU has internal pull up resistor, so it can connect to i2c6 on the PI (pin 15 and 16)
- The Bar30 has to connect to the primary bus (pin3 and pin5) because it does not have internal pull up resistor.


### New member signatures! 
