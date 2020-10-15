#! /usr/bin/env bash

# Script file for deployment tests and starting backend.
# ====================================================
#             .''
#   ._.-.___.' (`\
#  //(        ( `'
# '/ )\ ).__. )    haha scalable horse goes brrrrrrrr 
# ' <' `\ ._/'\
#   `   \     \
# ====================================================

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
        echo " ======================================================== "

        echo "Set python path...";
        # export PYTHONPATH=${PWD:0:-7};
        echo $PYTHONPATH

        echo " ======================================================== "
        echo "Checking if database is awake...";
        python3 ./src/backend_pre_start.py;
        
        echo " ======================================================== "
        echo "Model migration...";
        alembic upgrade head;
        export CANRUN=1;
    else
        echo "Please provide the correct amount of arguments.";
    fi
}

# Run this if tthe shell was closed
wake-up() {
    echo "Set python path...";
    curd=$(pwd);
    export PYTHONPATH=${curd::len-7}:$PYTHONPATH;

    echo " ======================================================== "
    echo "Checking if database is awake...";
    python3 ./src/backend_pre_start.py;
} 

backend-run() {

    if [ $CANRUN = 1 ];
    then
        echo "Is DB still awake ?"
        python3 ./src/backend_pre_start.py;
        echo "Cool..."
        
        echo " ======================================================== "
        echo "Starting..."
        uvicorn src.main:app --reload;
    else
        echo "Run configuration first please."
    fi
}   

