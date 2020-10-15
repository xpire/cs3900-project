# Backend

This the the root directory for the backend of the application. Instruction on deployment is as follows.

## Primitive environment 
You must ensure that the following is installed on the deployment environment:
```
$ python = 3.7.3
$ sqlite3
```

To install all the python dependencies please do 
```
$ pip install -r requirements.txt
```

`NOTE`: Please run the backend on a unix based system, I am not sure what happens on windows or mac.

## Execution
Please run the following in terminal. 
```
$ cd backend
$ source start.sh
$ first-time-setup /path/to/.env
$ backend-run
```
`.env` file contains the configuration information and secrets required for execution. 

`Note`: please run dos2unix if there are errors relating to format.

 