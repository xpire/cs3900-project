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

export PROOT=$(pwd); # backend here
export CANRUN=0; # can run the backend

print-line() {
    echo "============================================================================="
}

# Initialize the database with the stocks data
init-data() {
    print-line;
    echo "Creating initial data...";
    python3 ${PROOT}/src/db/init_db.py;
    print-line;
}

check-wake() {
    echo "Checking if database is awake...";
    python3 ${PROOT}/src/db/wake_db.py;
    echo "Cool...";
}

# Run this if tthe shell was closed
wake-up() {
    print-line;
    echo "Set python path...";
    export PYTHONPATH=${PROOT}:$PYTHONPATH;
    echo "Cool..."

    print-line;
    check-wake; 
    print-line;

    export CANRUN=1;
} 

upgrade-db() {
    print-line;
    echo "Upgrading database...";

    alembic upgrade head; 

    # cd $s;
    if [ $? -eq 0 ]; then
        echo "Success!!!"
    else
        echo "Error: Upgrade database failed...";
        exit $?;
    fi
    print-line;
}


if [ $# -eq 3 ]; then
    case $1 in
        "initial-populate")
            echo "============================================================================="
            echo "▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄   ▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄  ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄    ▄▄   ▄▄ ▄▄▄▄▄▄    "
            echo "█       █       █   █ █ █       █      ██       █       █  █  █▄█  █      █  "
            echo "█    ▄▄▄█       █   █▄█ █  ▄▄▄▄▄█  ▄    █    ▄▄▄█    ▄▄▄█  █       █  ▄    █ "
            echo "█   █▄▄▄█     ▄▄█      ▄█ █▄▄▄▄▄█ █ █   █   █▄▄▄█   █▄▄▄   █       █ █ █   █ "
            echo "█    ▄▄▄█    █  █     █▄█▄▄▄▄▄  █ █▄█   █    ▄▄▄█    ▄▄▄█   █     ██ █▄█   █ "
            echo "█   █▄▄▄█    █▄▄█    ▄  █▄▄▄▄▄█ █       █   █▄▄▄█   █▄▄▄   █   ▄   █       █ "
            echo "█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄█ █▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄██▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█  █▄▄█ █▄▄█▄▄▄▄▄▄█  "
            echo "============================================================================="

            echo "uwu, Starting first time population"
            print-line;

            echo "Copying secrets...";

            cp $2 ${PROOT}/src/core/.secrets/; 
            if [ $? -eq 0 ]; then
                echo "env.yaml looks good...";
            else
                echo "Error: Path provided for env.yaml is incorrect.";
                exit $?;
            fi

            cp $3 ${PROOT}/src/core/.secrets/;
            if [ $? -eq 0 ]; then
                echo "Firebase token looks good...";
            else
                echo "Error: Path provided for firebase-token is incorrect.";
                exit $?;
            fi

            wake-up;
            upgrade-db;
            init-data;

        ;; 
        *) echo "Variable name error.";;
    esac
elif [ $# -eq 1 ]; then
    case $1 in
            "wake-up")
            print-line;
            echo "Set python path...";
            export PYTHONPATH=${PROOT}:$PYTHONPATH;
            echo "Cool..."

            print-line;
            check-wake; 
            print-line;
        ;;

        "backend-run")
            print-line;

            echo "Set python path...";
            export PYTHONPATH=${PROOT}:$PYTHONPATH;
            echo "Cool..."
            
            check-wake;
            print-line;
            echo "Starting...";
            uvicorn src.main:app --reload;
        ;;

        "init-db")
            print-line;
            wake-up;
            upgrade-db;
            init-data;
        ;;

        "nuke-db") # be in backend
            print-line;
            rm ../database/testdb.sqlite3 # change this later
            echo "Nuking database from the orbit ..."
            export PYTHONPATH=${PROOT}:$PYTHONPATH;
        
            python src/db/init_db.py
        echo "Database destroyed" 
        ;;
        *) echo "Please provide the correct path.";;
    esac
else
    echo "Please provide the correct amount of arguments, check the README file for usage.";
fi