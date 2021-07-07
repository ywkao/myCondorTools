#!/usr/bin/env python
import subprocess

#--------------------------------------------------
# monitor condor jobs
#--------------------------------------------------
subprocess.call("./check_htcondor.py --monitor --employed 08 11 12 16 13 15 21", shell=True)
#subprocess.call("./check_htcondor.py --exe", shell=True)

#--------------------------------------------------
# check failed jobs
#--------------------------------------------------
#subprocess.call("./resubmit_tasks.py --tag data --year 16 --check_fatal_messages", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 16 --modify_submission_scripts", shell=True)

#subprocess.call("./resubmit_tasks.py --tag data --year 17 --check_fatal_messages", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 17 --modify_submission_scripts", shell=True)

#subprocess.call("./resubmit_tasks.py --tag data --year 18 --check_fatal_messages", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 18 --modify_submission_scripts", shell=True)

#--------------------------------------------------
# resubmit failed jobs
#--------------------------------------------------
# Note: ensure the previous section is gone through
# latest resubmit list is needed, eg. ./examine/latest_resubmit_list_data_18_20210707.txt)

#subprocess.call("./resubmit_tasks.py --tag data --year 16 --exe", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 17 --exe", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 18 --exe", shell=True)

