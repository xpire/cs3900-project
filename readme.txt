============================================================================
▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄   ▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄  ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄    ▄▄   ▄▄ ▄▄▄▄▄▄    
█       █       █   █ █ █       █      ██       █       █  █  █▄█  █      █  
█    ▄▄▄█       █   █▄█ █  ▄▄▄▄▄█  ▄    █    ▄▄▄█    ▄▄▄█  █       █  ▄    █ 
█   █▄▄▄█     ▄▄█      ▄█ █▄▄▄▄▄█ █ █   █   █▄▄▄█   █▄▄▄   █       █ █ █   █ 
█    ▄▄▄█    █  █     █▄█▄▄▄▄▄  █ █▄█   █    ▄▄▄█    ▄▄▄█   █     ██ █▄█   █ 
█   █▄▄▄█    █▄▄█    ▄  █▄▄▄▄▄█ █       █   █▄▄▄█   █▄▄▄   █   ▄   █       █ 
█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄█ █▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄██▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█  █▄▄█ █▄▄█▄▄▄▄▄▄█  
============================================================================
Project selection: Investment Simulator
Project name: Xecute the Deal 
Course code: COMP3900
Team name: ecksdee
============================================================================
Members:
    z5165320 | Even Tang  | SCRUM MASTER
    z5163307 | Ian Park   | FULL STACK DEVELOPER
    z5163301 | George Bai | BACKEND DEVELOPER
    z5165313 | Song Fang  | BACKEND DEVELOPER
    z5163950 | Justin Or  | FRONTEND DEVELOPER
============================================================================


============================================================================
Deployments
============================================================================
Operating system:
    - Vlab under cse => Debian linux 
Static depdencies (imposed by the Vlab system):
    - python 3.7.3
    - sqlite3 3.27.2
    - node 10.21.0
    - npm 5.8.0
============================================================================


============================================================================
Folder structure
============================================================================
# CONTEXT Below provide an overview of the folder structure of this project
----------------------------------------------------------------------------
. --> root of the project
├── README.md --> more general version of execution details.
├── general_readme.pdf --> pdf version of README.md
├── backend --> Backend source code
│   ├── README.md --> Backend detailed instructions
│   ├── backend_readme.pdf --> pdf version of README.md
│   ├── requirements.txt --> Python depdencies
│   ├── src
│   │   ├── __init__.py
│   │   ├── api
│   │   ├── core
│   │   ├── crud
│   │   ├── db
│   │   ├── domain_models
│   │   ├── game
│   │   ├── main.py
│   │   ├── models
│   │   ├── notification
│   │   ├── schemas
│   │   └── tests
│   └── start.sh --> Backend entry point
├── database --> Database and static data
│   ├── initial_users.csv
│   ├── stocks.csv
│   └── test_stock.csv
├── readme.txt
├── web --> Frontend source code and modules
│   ├── README.md --> Frontend detailed instructions
│   ├── frontend_readme.pdf --> Frontend detailed instructions
│   ├── package-lock.json
│   ├── package.json 
│   ├── public
│   ├── src
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── components
│   │   ├── constants
│   │   ├── ecksdeeLogo.png.svg
│   │   ├── ecksdeeLogo.svg
│   │   ├── hooks
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── logo.svg
│   │   ├── reducers
│   │   ├── routes
│   │   ├── serviceWorker.js
│   │   ├── setupTests.js
│   │   ├── stubby
│   │   ├── tutorial
│   │   └── utils
└── work diaries
    ├── George - z5163301.txt
    ├── I Su Park - z5163307.txt
    ├── Justin - z5163950.txt
    ├── Peiyu - z5165320.txt
    └── Song - z5165313.txt
----------------------------------------------------------------------------
============================================================================


============================================================================
(Installation) Building Dependency
    - NOTE: Only required to be executed once at the start. 
    - All "EXECUTION" tags assumes that the current directory is set at root
    of the project.
============================================================================
# CONTEXT To run the python-based backend and reactjs based frontend, it is 
required to build both dependencies so that project can run. For python, we 
start a virtual environment and install the dependency. Note that whenever 
we want to execute the backend, it is required to activate the virtual 
environment that has been set up. For npm, we run the required command.
----------------------------------------------------------------------------
# EXECUTION - Python
----------------------------------------------------------------------------
> cd backend
> python3 -m venv proj_env; 
> source proj_env/bin/activate;
> python3 -m pip install -U pip; 
> python3 -m pip install -U -r requirements.txt; 
----------------------------------------------------------------------------
# EXECUTION - npm
----------------------------------------------------------------------------
> cd web
> npm install
----------------------------------------------------------------------------
# EXECUTION - start python venv
----------------------------------------------------------------------------
> cd backend
> python3 -m venv proj_env; 
> source proj_env/bin/activate;
----------------------------------------------------------------------------
============================================================================


============================================================================
(Build) First time setup
    - NOTE: Only required to be executed once at the start. 
============================================================================
# CONTEXT: 
    - The backend requires 2 pieces of authentication secret files in 
    order to run, those are named "env.yaml" (API keys and environment 
    variables) and "ecksdee-firebase.json" (for firebase authentication 
    token). Despite those, the project also requires a PYTHONPATH variable 
    to be set for python modules.
----------------------------------------------------------------------------
# EXECUTION
----------------------------------------------------------------------------
> cd backend
> bash start.sh initial-populate path/to/env.yaml path/to/ecksdee-firebase.json
----------------------------------------------------------------------------
============================================================================
 

============================================================================
(Execution) Running the application
============================================================================
# CONTEXT: 
    - Please run the backend and the frontend in different shells 
----------------------------------------------------------------------------
# EXECUTION - Backend
    - please run below AFTER setting up the python virtual environment
    in the corresponding shell.
----------------------------------------------------------------------------
> cd backend
> bash start.sh initial-populate path/to/env.yaml path/to/ecksdee-firebase.json
----------------------------------------------------------------------------
# EXECUTION - frontend
----------------------------------------------------------------------------
> cd web 
> npm build
> npm run serve
----------------------------------------------------------------------------
============================================================================


============================================================================
(Extra Notes) execution and more 
============================================================================
# CONTEXT: 
    - "project_root/README.md", "project_root/backend/README.md", and 
    "project_root/web/README.md" contains more detailed commands and 
    execution that is provided by the dev ops scripts. ".md" file can 
    either viewd on the github repository or an equivalent pdf version of it 
    can be found in the same directory. 
    - npm install is known to have warnings that do not impact execution 
    during the installation process which halts the installation 
    process. If such instances happen please force installation by 
    repeating the command npm install.  
----------------------------------------------------------------------------

============================================================================
 
 
