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
title-bar() {
    echo "============================================================================="
    echo "▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄   ▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄  ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄    ▄▄   ▄▄ ▄▄▄▄▄▄    "
    echo "█       █       █   █ █ █       █      ██       █       █  █  █▄█  █      █  "
    echo "█    ▄▄▄█       █   █▄█ █  ▄▄▄▄▄█  ▄    █    ▄▄▄█    ▄▄▄█  █       █  ▄    █ "
    echo "█   █▄▄▄█     ▄▄█      ▄█ █▄▄▄▄▄█ █ █   █   █▄▄▄█   █▄▄▄   █       █ █ █   █ "
    echo "█    ▄▄▄█    █  █     █▄█▄▄▄▄▄  █ █▄█   █    ▄▄▄█    ▄▄▄█   █     ██ █▄█   █ "
    echo "█   █▄▄▄█    █▄▄█    ▄  █▄▄▄▄▄█ █       █   █▄▄▄█   █▄▄▄   █   ▄   █       █ "
    echo "█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄█ █▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄██▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█  █▄▄█ █▄▄█▄▄▄▄▄▄█  "
    echo "============================================================================="
}          

set-python-path() {
    print-line;
    echo "Set python path...";
    export PYTHONPATH=${PROOT}:$PYTHONPATH && echo "Cool..."
    print-line;
}

check-wake() {
    print-line;
    echo "Checking if database is awake...create one if its missing...";
    python3 ${PROOT}/src/db/wake_db.py && echo "Cool...";
    print-line;
}

# Initialize the database with the stocks data
init-db() {
    print-line;
    echo "Creating initial data...";
    python3 ${PROOT}/src/db/init_db.py && echo "Cool...";
    print-line;
}

# Get the git hook tests
setup-test() {
    echo "Setting up git hook tests...";
    git_dir="../.git/hooks";

    # yeet the pytest file
    cp src/tests/pytest.sh ${git_dir}
    
    # delete file create file blah blah blah...
    echo ". \"\$(dirname "\$0")/pytest.sh\"" >> ${git_dir}/pytest_temp;
    test -f ${git_dir}/pre-push && awk '!/pytest/' ${git_dir}/pre-push >> ${git_dir}/pytest_temp && rm ${git_dir}/pre-push;
    mv ${git_dir}/pytest_temp ${git_dir}/pre-push && chmod +x ${git_dir}/pre-push && echo "Cool";
}

explode() {
    echo "      _.-^^---....,,--          "
    echo "  _--                  --_     "
    echo " <                        >)   "
    echo " |                         |    "
    echo "  \._                   _./     "
    echo "     \`\`\`--. . , \; .--'''        "  
    echo "           | |   |               " 
    echo "        .-=||  | |=-.      "
    echo "        \`-=#$%&%\$#=-'      "
    echo "           | ;  :|        "
    echo "  _____.,-#%&\$@%#&#~,._____   "
    echo " !!!!!!!!!BOOOOMMMMMM!!!!!!!!!!!"
}

if [ $# -eq 3 ]; then
    case $1 in
        "initial-populate")
            title-bar;
            echo "uwu, Starting first time population"
            print-line;
            set-python-path
            
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

            check-wake;
            init-db;
        ;; 
        *) echo "Variable name error.";;
    esac
elif [ $# -eq 1 ]; then
    case $1 in
        "check-wake")
            title-bar;
            set-python-path;
            check-wake; 
        ;;
        "run")
            title-bar;
            set-python-path;
            check-wake;
            
            echo "Starting...";
            uvicorn src.main:app --reload --ws websockets;
        ;;

        "init-db")
            title-bar;
            set-python-path
            check-wake;
            init-db;
        ;;

        "nuke-db-from-orbit") # be in backend
            title-bar; 
            read -p "Are you sure you want to nuke it ? you will lose all the data in the database...   "  res
            set-python-path; 
            if [ $res=="yes" ]; then 
                db_name=$(grep -A0 'SQLITE_DB_NAME: ' ./src/core/.secrets/env.yaml | cut -d ":" -f2 | cut -c 2-) 
                echo "Nuking $db_name from the orbit..."
                rm ../database/$db_name.sqlite3 && explode;

                echo "Recreating it now...";
                check-wake;
                init-db;
            else
                echo "ABORT!!!! ABORT!!!!" 
            fi
        ;;

        "setup-test")
            title-bar; 
            set-python-path;
            setup-test;
        ;;

        "setup-pythonpath")
            set-python-path;
        ;; 

        "run-test")
            title-bar; 
            set-python-path;
            pytest -v src/tests;
        ;;
        *) echo "Please provide the correct function name.";;
    esac
else
    echo "Please provide the correct amount of arguments, check the README file for usage.";
fi 