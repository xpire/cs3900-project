<p align="center">
   <img src="https://raw.githubusercontent.com/unsw-cse-capstone-project/capstone-project-comp3900-f13a-ecksdee/master/web/src/logo.svg?token=AHIETN3VKVIIITLJ6UWZA6S7VURPS" width="165" height="70" align="center"> 
   <img src="https://www.unsw.edu.au/sites/all/themes/mobileunswcorporate/logo.png" width="165" height="70" align="center">
 </p>

<h2 align="center"> 🤣 COMP3900 Group project - Xecute the Deal 🤣 </h2> 

## Description
This is the repository for the COMP3900 project, do not commit bad code or Ian will be angry 😈😈😈. The project selected is `Investment Simulator`, the application name is "Xecute the Deal". 

<br/>
## Members and Development Roles

<center>

| SCRUM MASTER | FULL STACK | FRONTEND  | BACKEND   | BACKEND    |
|--------------|------------|-----------|-----------|------------|
| Peiyu Tang   |  Ian Park  | Justin Or | Song Fang | George Bai |

</center>

<br/>

## Deployment Environment
The application will be deployed on the cse-vlab linux environment. The specified versions are
```
$ python = 3.7.3
$ npm = 5.8.0
$ nodejs = 10.21.0
```
<br/>

## Quick Start
### Frontend
To quickly activate the React-JS frontend, please do
```
$ cd web
$ npm install
$ npm start
```
### Backend
To quickly run the FASTAPI python backend, please first create a python virtual environment via 
```
$ cd backend
$ python3 -m venv env_name; source env_name/bin/activate;
```
Then please do
```
$ python3 -m pip install -U pip; python3 -m pip install -U -r requirements.txt; 
$ bash start.sh initial-populate path/to/env.yaml path/to/ecksdee-firebase.json
$ bash start.sh run
```
