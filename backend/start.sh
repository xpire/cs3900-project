#! /usr/bin/env bash

# Script file for deployment tests and starting backend.
# ========================================================
#             .''
#   ._.-.___.' (`\
#  //(        ( `'
# '/ )\ ).__. )    haha scalable horse goes brrrrrrrr 
# ' <' `\ ._/'\                                        
#   `   \     \                                        
# ========================================================

export PROOT=$(pwd);

# Initialize the database with the stocks data
init-data() {
    echo " ======================================================== ";
    echo "Creating initial data...";
    python3 ./src/initial_data.py;
}


# Run this if tthe shell was closed
wake-up() {
    echo "Set python path...";
    echo " ======================================================== ";
    curd=$(pwd);
    export PYTHONPATH=${curd::len-7}:$PYTHONPATH;

    echo " ======================================================== ";
    echo "Checking if database is awake...";
    python3 ./src/backend_pre_start.py;
} 


upgrade-db() {
    echo "Upgrading database...";
    echo " ======================================================== ";
    alembic upgrade head; 
}


# Run this to get rid of the database
clear-db() {
    echo "Removing database...";
    echo " ======================================================== ";
    rm ../models/testdb.sqlite3; 
}


# give db name and 
export CANRUN=0;

# Basing on CLI parameter, install dependency
first-time-setup() {
    export can_run=0;
    if [ $# -eq 1 ];
    then
        # echo "Running simple environment checks..."; 
        echo "Copying secrets...";
        cp $1 ./src/core/;
        echo " ======================================================== ";
        
        wake-up;
        
        upgrade-db;
        
        init-data;

        export can_run=1;
        export CANRUN=1;

    else
        echo "Please provide the correct amount of arguments.";
    fi
}




backend-run() {

    if [ $CANRUN = 1 ];
    then
        echo "Is DB still awake ?";
        python3 ./src/backend_pre_start.py;
        echo "Cool...";
        
        echo " ======================================================== ";
        echo "Starting...";
        uvicorn src.main:app --reload;
    else
        echo "Run configuration first please.";
    fi
}   

