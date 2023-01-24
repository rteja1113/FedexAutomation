# FedexAutomation
A repo for automating some of the Fedex P&amp;D(pick-up and delivery) contractor's administrative stuff.

## TODO
- [x] add requirements.txt
- [x] add setup in readme
- [] add basic working example
- [] add logging
- [] enable pre-commits with code formatting
- [] Update README
- [] auto generate API documentation

## Setup(local development)
If you want to run the app skip to "Run with Docker" section
##### 1. Code
Clone the repo and `cd FedexAutomation`
##### 2. MongoDB
- We are using mongodb to store the daily driver schedules. Please install mongodb==6.0.3 for the OS you are using(https://www.mongodb.com/docs/manual/administration/install-community/)
- Once you finished installation, it is recommended(optional) that you install MongoDB Compass for interactive exploration

##### 3. Python
We have provided a shell script for setting up a python3 `venv` and installing the requirements.
You can simply run `sh ./setup_venv.sh`


## Run with Docker
- build and run the docker using `docker-compose up --build`
- Open `http://localhost:8000` in your browser and test out the API !

