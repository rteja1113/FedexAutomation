# FedexAutomation
A repo for automating some of the Fedex P&amp;D(pick-up and delivery) contractor's administrative stuff.

## TODO
- [x] add requirements.txt
- [x] add setup in readme
- [] add basic working example
- [] add logging
- [] enable pre-commits with code formatting
- [] Update README

## Setup
##### 1. Code
Clone the repo and `cd FedexAutomation`
##### 2. MongoDB
- We are using mongodb to store the dialy driver schedules. Please install mongodb==6.0.3 for the OS you are using(https://www.mongodb.com/docs/manual/administration/install-community/)
- Once you finished installation, it is recommended(optional) that you install MongoDB Compass for interactive exploration
- Create a db named `FedexDB` and add a collection named `FedexDriverDailyService` to it.
- Create a folder named `datasets` and add all the downloaded json files in `datasets` folder 

##### 3. Python
We have provided a shell script for setting up a python3 `venv` and installing the requirements.
You can simply run `sh ./setup_venv.sh`


## Run with Docker

- Before running the app, we need add data to our db. cd into `aggregateStats/` and run `python mongo_crud_utils.py` 
which will insert the documents in your database.
- Use the docker file to build an image using `docker build -t fedex-sample-app .`
- Connect your local db from Docker using (https://tsmx.net/docker-local-mongodb/#:~:text=For%20connecting%20to%20your%20local,in%20the%20network%20interface%20section).
You just need to bind the ip in the .conf file. No need to choose a hostname for now
- Run the app using `docker run --add-host=localhost:172.17.0.1 -p 8000:8000 -e MONGO_URL=mongodb://localhost`
- Open your browser and type `localhost:8000` and your app is live !


