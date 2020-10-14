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
set -x;
export can_run=0; 

# Basing on CLI parameter, install dependency or 
pre-config() {
    if [ $# -eq 1 ];
    then
        # echo "Running simple environment checks..."; 
        echo "Copyting secrets...";
        cp $1 ./src/core/;
        
        echo "Checking if database is awake...";
        python ./src/backend_pre_start.py;
        
        echo "Set python path...";
        curd=$(pwd);
        export PYTHONPATH=${curd::len-7}:$PYTHONPATH;
        
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
        python ./src/backend_pre_start.py;
        echo "Cool..."
        echo "Starting..."
        cd src;
        uvicorn main:app --reload;
    else
        echo "Run configuration first please."
    fi
}   

