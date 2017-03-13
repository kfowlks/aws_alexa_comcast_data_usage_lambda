#!/bin/bash
# ------------------------------------------------------------------
#   Author [Kevin Fowlks] 
#  
#   Date 12/13/2016
#
#   Build a zip file for aws lambda
#
#   Usage: ./build.sh
#set -e
#set -o pipefail
#set -u

check_errs()
{
    # Function. Parameter 1 is the return code
      # Para. 2 is text to display on failure.
        if [ "${1}" -ne "0" ]; then
          echo "ERROR # ${1} : ${2}"
          # as a bonus, make our script exit with the right error code.
          exit ${1}
        fi
}

if [ -f "ask-alexa_comcast_data_usage_lambda.zip" ]; then
    rm -f
fi

if [ ! -d "requests" ]; then
    pip install requests -t .
    check_errs $? "Failed to install pip requests"
fi

if [ ! -d "ask" ]; then
    git clone https://github.com/anjishnu/ask-alexa-pykit.git
    check_errs $? "Failed to clone git repository"

    cd ask-alexa-pykit
    check_errs $? "Failed to change directory"

    git checkout python_lambda_0.5_release
    check_errs $? "Failed to checkout as-alexa-pykit branch"

    mv ask ../
    check_errs $? "Failed to move ask directory"

    cd ..
    check_errs $? "Failed cd to project directory"

    rm -rf ask-alexa-pykit
    check_errs $? "Remove ask-alexa-pykit directory"
fi

zip -r ask-alexa_comcast_data_usage_lambda.zip *
check_errs $? "Failed to zip file"