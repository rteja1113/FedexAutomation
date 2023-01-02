# FedexAutomation
A repo for automating some of the Fedex P&amp;D(pick-up and delivery) contractor's administrative stuff.

## TODO
- [x] add requirements.txt
- [] add setup in readme
- [] add basic working example
- [] add logging

## Setup

##### 1. MongoDB
- We are using mongodb to store the dialy driver schedules. Please install mongodb==6.0.3 for the OS you are using(https://www.mongodb.com/docs/manual/administration/install-community/)
- Once you finished installation, it is recommended(optional) that you install MongoDB Compass for interactive exploration
- Create a db named `FedexDB` and add a collection named `FedexDriverDailyService` to it.


##### 2. Python
We have provided a shell script for setting up a python3 `venv` and installing the requirements.
You can simply run `sh ./setup_venv.sh`


## Demo


