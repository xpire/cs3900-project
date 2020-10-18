# Backend

This the the root directory for the backend of the application. Instruction on deployment is as follows.

## Primitive environment 
You must ensure that the following is installed on the deployment environment:
```
$ python = 3.7.3
```

To install all the python dependencies please do 
```
$ pip install -r requirements.txt
```

`NOTE`: Please run the backend on a unix based system, I am not sure what happens on windows or mac.

## First time setup
Please run the first time setup by   
```
$ cd backend
$ source start.sh && initial-populate /path/to/env.yaml /path/to/ecksdee-firebase.json
$ backend-run
```
`.env` file contains the configuration information and secrets required for execution. 
`Note`: please run dos2unix if there are errors relating to format.

## Backend wake up
If first time setup has been run but you have closed the shell, then you can just run
```
$ source start.sh && wake-up && backend-run
```

## Other utilities
You may also use some of the utilities provided by `start.sh`. 

Below command upgrades the database to a `newer` version.
```
$ upgrade-db;
```

Below command starts the backend, note that other setup still needs to be ran before this.
```
$ backend-run; 
```
 