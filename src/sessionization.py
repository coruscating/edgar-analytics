from __future__ import division
import sys
import traceback
import datetime

# February 12, 2019, Helena Zhang
# written and tested in Python 2.7.10

# This script calculates the session
# Inputs:
# 1. log.csv, a CSV log file
# 2. inactivity_period.txt
# Check README.md for more information.

############################################
# EDITABLE PARAMETERS
#
# to get verbose messages, set DEBUG to True
DEBUG=False


# END OF EDITABLE PARAMETERS
############################################


if (len(sys.argv) != 4 and len(sys.argv) != 5):
    print "Wrong number of arguments, exiting! Please run via run.sh."
    sys.exit()

logfile=sys.argv[1]
inactfile=sys.argv[2]
outfile=sys.argv[3]
if(len(sys.argv)==5): DEBUG=sys.argv[4]

if DEBUG: print ("Debug is on\ninput log file: %s \ninput inactivity period file: %s\noutput file: %s\n"%(logfile, inactfile, outfile))
else:
    print "Debug is off"

fields=['ip','date','time']

users={}
jobs={}

# process log file into array, gets array of top users and occupations
def process_logfile(inputfile, outfile, ttl):
    try:
        fo=open(outfile, "w")

        with open(inputfile) as f:
            # get first line, which should be
            # ip,date,time,zone,cik,accession,extention,code,size,idx,norefer,noagent,find,crawler,browser
            # but we will make sure
            fieldline=f.readline().split(",")
 
            # check fields here: we only care about ip, date, time
            fieldindices=[]
            for field in fields:
                    if field in fieldline:
                        fieldindices.append(fieldline.index(field))
            if (len(fieldindices) != 3):
                print "Didn't find all fields, exiting!"
                sys.exit()

            
            if DEBUG: print "field indices [ip, date, time] : ", fieldindices
            

            for l in f: # this handles large files better than readlines()
                l2=l.split(",")

                newtime=datetime.datetime.strptime(l2[fieldindices[1]] + " " + l2[fieldindices[2]], "%Y-%m-%d %H:%M:%S")
                # update current time, we want to remove expired sessions
                if 'curtime' not in vars():
                    timediff=0
                else:
                    timediff=int((newtime-curtime).total_seconds())
                curtime=newtime

                # get IP of entry
                lip=l2[fieldindices[0]]

                # add state to the dictionary as a key if it doesn't exist, or increment value of existing key if it does
                if lip in users:
                    # IP already exists, need to increment pages and update TTL
                    users[lip][1]+=1
                    users[lip][2]=ttl
                else:
                    # instantiate new dictionary entry, [start time, number of pages, time to live]
                    users[lip]=[curtime, 1, ttl]

                # if time hasn't advanced, save us from iterating through all fields
                if timediff == 0:
                    continue

                # now go through and check all remaining fields
                for i in users.keys():
                    if i==lip: # already updated this one, skip
                        continue
                    else:
                        users[i][2]-=timediff
                        if users[i][2] <= 0: # this session's up
                            if DEBUG:
                                print("Ending session")
                                print users[i]

                            # the last time is equal to current time adjusted by TTL field and TTL
                            endtime=curtime-datetime.timedelta(seconds=ttl-users[i][2])
                            fo.write("%s,%s,%s,%d,%d\n" %(i, str(users[i][0]), str(endtime), int((endtime-users[i][0]).total_seconds())+1, users[i][1]))
                            del users[i]

        if DEBUG:
            print("End of file, processing remaining sessions")

        # end of file: need to clean up here, write the rest of the users
        for i in users.keys():
            # the last time is equal to current time adjusted by TTL field and TTL
            endtime=curtime-datetime.timedelta(seconds=ttl-users[i][2])
            fo.write("%s,%s,%s,%d,%d\n" %(i, str(users[i][0]), str(endtime), int((endtime-users[i][0]).total_seconds())+1, users[i][1]))
        fo.close()
        return 0
    except:
        print traceback.format_exc()
        sys.exit()


# get inactivity period from file
def get_inactivity(inputfile):
    try:
        with open(inputfile) as f:
            res=int(f.readline())
            if res < 1 or res > 86400:
                print("ERROR: Inactivity period must be between 1 and 86400 seconds.")
                sys.exit()
            return(res)
    except:
        print traceback.format_exc()
        sys.exit()

# main block
try:
    period=get_inactivity(inactfile)
    if DEBUG:
        print("Inactivity period: %d seconds" %(period))
    process_logfile(logfile, outfile, period)

except:
    print traceback.format_exc()
    sys.exit()
