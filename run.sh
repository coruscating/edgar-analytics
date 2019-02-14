#!/bin/bash
#
# Wrapper to run sessionization.py to generate output files.
# Usage: ./run.sh [-d] [-t TESTNAME]
# -d flag turns on debugging.
# -t flag uses TESTNAME as the name of the test folder under insight_testsuite/tests. If not provided, input/log.csv and input/inactivity_period.txt is used as defaults.
 
debug=""

while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -d)
            debug="True"
            shift
            ;;
        -t)
            path="$2"
            shift
            shift
            ;;
        *)
            echo "Usage: $0 [-d] [-t TESTNAME]" >&2
            exit 1
    esac
done

if [ -z $path ] ; then
    echo "Executing python ./src/sessionization.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt $debug"
    python ./src/sessionization.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt $debug
else
    echo "Executing python ./src/sessionization.py ./insight_testsuite/tests/$path/input/log.csv ./insight_testsuite/tests/$path/input/inactivity_period.txt ./insight_testsuite/tests/$path/output/sessionization.txt"
    python ./src/sessionization.py ./insight_testsuite/tests/$path/input/log.csv ./insight_testsuite/tests/$path/input/inactivity_period.txt ./insight_testsuite/tests/$path/output/sessionization.txt $debug
fi
    