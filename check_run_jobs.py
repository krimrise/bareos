#!/usr/bin/env python

import bareos.bsock
import json
import sys
import argparse


if __name__ == '__main__':
    
    argParser = argparse.ArgumentParser(description="Graphite poller for Bareos director.",
                                        prog="check_run_jobs.py", add_help=True)
    argParser.add_argument('job', help="Job name.")
    argParser.add_argument('joblevel', help="Job level.")
    args = argParser.parse_args()
    
    host = "localhost"
    dirname = "bareos-dir"
    passwd = ""
    dir_port = 9101
    whereJobs = ""
    JobStatus = "R"
    
    try:
        director = bareos.bsock.BSockJson(address=host, port=dir_port, password=bareos.bsock.Password(passwd))
    except RuntimeError as e:
        print(str(e))
        sys.exit(1)
    
    response = director.call("list jobs job=%s jobstatus=R" % args.job)
#    response = {u'jobs': [{u'name': u'alta-mssql-gtd', u'level': u'F', u'jobbytes': u'0', u'jobstatus': u'R', u'jobid': u'1872', u'client': u'arsql-fd', u'starttime': u'2018-05-24 16:05:00', u'jobfiles': u'0', u'type': u'B'},{u'name': u'alta-mssql-gtd', u'level': u'I', u'jobbytes': u'0', u'jobstatus': u'R', u'jobid': u'1873', u'client': u'arsql-fd', u'starttime': u'2018-05-24 16:05:00', u'jobfiles': u'0', u'type': u'B'}]}
    count = 0
    for job in response['jobs']:
        if job['name'] == args.job:
            count += 1
#            print("Job name: %s, JobLevel: %s, args.job: %s, args.joblevel: %s." % (job['name'], job['level'], args.job, args,joblevel))
#            sys.exit(1)
    if count > 1:
        print("##STOP##: " + str(count) + " :: " + str(response))
        sys.exit(1)
    else:
        print("##GOOD##: " + str(count) + " :: " + str(response) + " :: " + args.job + " :: " + args.joblevel)
        sys.exit(0)
