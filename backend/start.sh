#! /usr/bin/env bash
# ====================================================
#             .''
#   ._.-.___.' (`\
#  //(        ( `'
# '/ )\ ).__. )    haha scalable horse goes brrrrrrrr 
# ' <' `\ ._/'\
#   `   \     \
# ====================================================

# give db name and 
export can_run=0; 

# Basing on CLI parameter, install dependency or 
first-time-setup() {
    if [ $# -eq 1 ];
    then
        # echo "Running simple environment checks..."; 
        echo "Copyting secrets...";
        cp $1 ./src/core/;
        echo " ======================================================== "

        echo "Set python path...";
        curd=$(pwd);
        export PYTHONPATH=${curd::len-7}:$PYTHONPATH;

        echo " ======================================================== "
        echo "Checking if database is awake...";
        python3 ./src/backend_pre_start.py;
        
        echo " ======================================================== "
        echo "Model migration...";
        alembic upgrade head;
        export can_run=1;
    else
        echo "Please provide the correct amount of arguments.";
    fi
}

backend-run() {

    if [ $can_run == 1 ];
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

