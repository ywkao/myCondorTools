#!/usr/bin/env python
import subprocess

#--------------------------------------------------
# monitor condor jobs
#--------------------------------------------------
#subprocess.call("./check_htcondor.py --monitor", shell=True)
#subprocess.call("./check_htcondor.py --monitor --employed 13 15", shell=True)
#subprocess.call("./check_htcondor.py --exe", shell=True)

sample = "data"
#--------------------------------------------------
# check failed jobs
#--------------------------------------------------
# 1st step: check with fggRunJobs command first
#subprocess.call("fggRunJobs.py --load dir_%s_16/config.json --cont" % sample, shell=True)
#subprocess.call("fggRunJobs.py --load dir_%s_17/config.json --cont" % sample, shell=True)
#subprocess.call("fggRunJobs.py --load dir_%s_18/config.json --cont" % sample, shell=True)

# 2nd step: check with resubmit_tasks.py
#subprocess.call("./resubmit_tasks.py --tag %s --year 16 --check_fatal_messages" % sample, shell=True)
#subprocess.call("./resubmit_tasks.py --tag %s --year 17 --check_fatal_messages" % sample, shell=True)
#subprocess.call("./resubmit_tasks.py --tag %s --year 18 --check_fatal_messages" % sample, shell=True)

# 3rd step: modify *sh and *sub files
#subprocess.call("./resubmit_tasks.py --tag %s --year 16 --modify_submission_scripts" % sample, shell=True)
#subprocess.call("./resubmit_tasks.py --tag %s --year 17 --modify_submission_scripts" % sample, shell=True)
#subprocess.call("./resubmit_tasks.py --tag %s --year 18 --modify_submission_scripts" % sample, shell=True)

#--------------------------------------------------
# other commands (optional)
#--------------------------------------------------
#subprocess.call("./monitor_rootfiles.py --year 16", shell=True)
#subprocess.call("./resubmit_tasks.py --tag %s --year 18 --check_resubmit_list_only" % sample, shell=True)

# resubmit failed jobs
# Note: ensure the previous section is gone through
# latest resubmit list is needed, eg. ./examine/latest_resubmit_list_data_18_20210707.txt)
#subprocess.call("./resubmit_tasks.py --tag %s --year 2016 --exe" % sample, shell=True)
#subprocess.call("./resubmit_tasks.py --tag %s --year 2017 --exe" % sample, shell=True)
#subprocess.call("./resubmit_tasks.py --tag %s --year 2018 --exe" % sample, shell=True)
