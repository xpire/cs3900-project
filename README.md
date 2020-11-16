<p align="center">
   <img src="https://raw.githubusercontent.com/unsw-cse-capstone-project/capstone-project-comp3900-f13a-ecksdee/master/web/public/logo512.png?token=AHIETN6MXPXP6Y7BCS5JIP27XKCW6" width="70" height="70" padding="35" align="center"> 
   <img width="70">
   <img src="https://www.unsw.edu.au/sites/all/themes/mobileunswcorporate/logo.png" width="165" height="70" align="center">
 </p>
<!-- <div style="display:flex; justify-content: justify-around;">
<img src="https://raw.githubusercontent.com/unsw-cse-capstone-project/capstone-project-comp3900-f13a-ecksdee/master/web/public/logo512.png?token=AHJHQ44J3VAZHXHPHB7F2227VU7DY" width="70" height="70" align="center"> 
<img src="https://www.unsw.edu.au/sites/all/themes/mobileunswcorporate/logo.png" width="165" height="70" align="center">
</div> -->


<h2 align="center"> 🤣 COMP3900 Group project - Xecute the Deal 🤣 </h2> 

## Description
This is the repository for the COMP3900 project, do not commit bad code or Ian will be angry 😈😈😈. The project selected is `Investment Simulator`, the application name is "Xecute the Deal". 

<br/>

## Members and Development Roles


| SCRUM MASTER | FULL STACK DEVELOPER | FRONTEND DEVELOPER | BACKEND DEVELOPER | BACKEND DEVELOPER |
|:--------------:|:------------:|:-----------:|:-----------:|:------------:|
| Peiyu Tang   |  Ian Park  | Justin Or | Song Fang | George Bai |


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
To run the application quickly, follow the below steps.

### Step 1: Frontend
Quickly activate the React-JS frontend, please do
```
$ cd web
$ npm run build
$ npm build serve
```

### Step 2: Virtual Environment
To quickly run the FASTAPI python backend, please first create a python virtual environment via 
```
$ cd backend
$ python3 -m venv env_name; source env_name/bin/activate;
```

### Step3: Run Backend
Then please do
```
$ python3 -m pip install -U pip; python3 -m pip install -U -r requirements.txt; 
$ bash start.sh initial-populate path/to/env.yaml path/to/ecksdee-firebase.json
$ bash start.sh run
```
