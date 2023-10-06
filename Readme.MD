## Introduction

This project uses the following relevant tech stack
- Python ~3.85-3.9 (base langauge)
- PyQt ~5.12 (UI framework)
- Pipenv (Enviroment management)
- Openv-CV (for camera)

Please checkout our Wiki as there's more detailed documentation regarding the desgin, choice, etc. Here I will just focus on descrbing how to make it just "run".



## Setup

### Language
First off very importantly, you will need Python installed. Install the Python version listed above for you specific system online.

### Enviroment
Motivation: We don't want to clutter the Pi and our computer with numerous packages that might be conflicted with each other. It might seem like a good idea to have one global enviroment but things can get bad quickly. So we want to have a sandbox that isolate each project individually.

Solution: As such we are going to be using the Pipenv package manager for Python to do that. You can read up more, but essentially Pipenv treats each project as its own, and it can effectively group packages with project so you can have a fresh enviroment when you start a new project.

#### Setup Steps
1. Go to your terminal and make sure you have Python installed
2. 


### I2C externals

#### VERY IMPORT PLEASE READ THIS FOR SETUP
Right now the Pi needs to support 2 external i2c devices. We will use the default SDA and SLA (pin 3 pin 5) as well as converting general purpose GPIO to SDA and SLA (i2c6 which are pin 15 and pin 16).

- The Bno055 IMU has internal pull up resistor, so it can connect to i2c6 on the PI (pin 15 and 16)
- The Bar30 has to connect to the primary bus (pin3 and pin5) because it does not have internal pull up resistor.


### New member signatures! 
