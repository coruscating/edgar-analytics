# Table of Contents

1. [Problem](README.md#problem)
2. [Approach](README.md#approach)
3. [Run](README.md#run)
4. [Issues and considerations](README.md#issues-and-considerations)

# Problem

Given an EDGAR weblog file, we want to calculate user sessions grouped by IP with a given timeout.

# Approach

`sessionization.py` stores each user as an element in a dictionary, keyed by the IP, with start time, pageviews, and time-to-live (TTL). Its main loop reads `log.csv` line by line:

1. Converts date and time into seconds elapsed since last update
2. If the user already exists, increment their pageviews and refresh time-to-live (TTL)
3. Updates time-to-live (TTL) of each remaining IO
4. If TTL is non-positive, terminate session and write to file

Once it reaches the end of the file, remaining sessions are written to the output file.

# Run

To run the code, execute `run.sh` in the base directory and it will use default input files `./input/log.csv` and `./input/inactivity_period.txt` and default output file `./output/sessionization.txt`:

```
./run.sh
```

To print debugging, use the flag `-d`. Any of the testsuites in the `insight_testsuite` folder can be run by using the flag `-t` and the test name as an argument to `run.sh`. The output files will be generated under the `output` directory under that test folder:

```
./run.sh -d -t test_1
```

# Issues and considerations

Currently it does not stream `log.csv` and so does not know if it has been updated over the course of the main loop. It also does not check if data fields are valid.
