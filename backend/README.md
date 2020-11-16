<p align="center">
   <img src="https://raw.githubusercontent.com/unsw-cse-capstone-project/capstone-project-comp3900-f13a-ecksdee/master/web/public/logo512.png?token=AHIETN6MXPXP6Y7BCS5JIP27XKCW6" width="70" height="70" padding="35" align="center"> 
   <img width="70">
   <img src="https://www.unsw.edu.au/sites/all/themes/mobileunswcorporate/logo.png" width="165" height="70" align="center">
 </p>

# Backend

This the the root directory for the backend of the application. Instruction on deployment is as follows.

## Primitive environment 
You must ensure that the following is installed on the deployment environment:
```
$ python = 3.7.3
```

To install all the python dependencies please do 
```
$ pip install -U pip
$ pip install -U -r requirements.txt
```

`NOTE`: Please run the backend on a unix based system, I am not sure what happens on windows or mac.

## First time setup
Please run the first time setup by   
```
$ cd backend
$ bash start.sh initial-populate /path/to/env.yaml /path/to/ecksdee-firebase.json
```
`env.yaml`: file containing the configuration information and secret keys. 
`ecksdee-firebase`: file containing the firebase token. 

## Testing
To manually set up the git hook test, run 
```
$ bash start.sh setup-test
``` 
To run the tests manually run the tests now, run
```
$ bash start.sh run-test
```

## Other utilities
You may also use some of the utilities provided by `start.sh`. 

To check if db exists and create one if its missing, run
```
$ bash start.sh check-wake
```
To only create the tables and insert the static stock data, run
```
$ bash start.sh init-db
``` 

Below command deletes the database and creates a new one following the defined metadata in `src/models`, use with caution please.
```
$ bash start.sh nuke-db-from-orbit;
```

Below command starts the backend, please make sure that tables are created before running this.
```
$ bash start.sh run; 
```
 
