# Backend

This the the root directory for the backend of the application. Instruction on deployment is as follows.

## Primitive environment 
You must ensure that the following is installed on the deployment environment:
```
$ python = 3.7.3
$ postgresql = 8.3.*
```

To install all the python dependencies please do 
```
$ pip install -r requirements.txt
```

NOTE: Please run the backend on a unix based system, I am not sure what happens on windows.

## Execution
Please run the following in terminal. 
```
$ cd backend
$ export start
$ pre-config /path/to/.env
$ back-end-run
```
`.env` file contains the configuration information and secrets required for execution.
NOTE: Please set database properly before executing above scripts.


 