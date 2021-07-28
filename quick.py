#!/usr/bin/env python
import subprocess

#--------------------------------------------------
# monitor condor jobs
#--------------------------------------------------
#subprocess.call("./check_htcondor.py --monitor", shell=True)
subprocess.call("./check_htcondor.py --monitor --employed 13", shell=True)
#subprocess.call("./check_htcondor.py --exe", shell=True)

#--------------------------------------------------
# check failed jobs
#--------------------------------------------------
#subprocess.call("./resubmit_tasks.py --tag data --year 18 --check_root_files", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 18 --check_resubmit_list_only", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 17 --check_fatal_messages", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 17 --modify_submission_scripts", shell=True)

sample = "data"

# fggRunJobs.py --load dir_data_17/config.json --cont
#subprocess.call("./monitor_rootfiles.py --year 16", shell=True)

#subprocess.call("./resubmit_tasks.py --tag %s --year 16 --check_fatal_messages" % sample, shell=True)
#subprocess.call("./resubmit_tasks.py --tag %s --year 17 --check_fatal_messages" % sample, shell=True)
#subprocess.call("./resubmit_tasks.py --tag %s --year 18 --check_fatal_messages" % sample, shell=True)

#subprocess.call("./resubmit_tasks.py --tag %s --year 17 --check_resubmit_list_only" % sample, shell=True)

#subprocess.call("./resubmit_tasks.py --tag %s --year 16 --modify_submission_scripts" % sample, shell=True)
#subprocess.call("./resubmit_tasks.py --tag %s --year 17 --modify_submission_scripts" % sample, shell=True)
#subprocess.call("./resubmit_tasks.py --tag %s --year 18 --modify_submission_scripts" % sample, shell=True)


#subprocess.call("./resubmit_tasks.py --tag data --year 2016 --check_fatal_messages", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 2016 --modify_submission_scripts", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 2017 --check_fatal_messages", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 2017 --modify_submission_scripts", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 2018 --check_fatal_messages", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 2018 --modify_submission_scripts", shell=True)

#subprocess.call("./resubmit_tasks.py --tag data --year 2016 --manual --check_fatal_messages", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 2016 --manual --modify_submission_scripts", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 2017 --manual --check_fatal_messages", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 2017 --manual --modify_submission_scripts", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 2018 --manual --check_fatal_messages", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 2018 --manual --modify_submission_scripts", shell=True)

#--------------------------------------------------
# resubmit failed jobs
#--------------------------------------------------
# Note: ensure the previous section is gone through
# latest resubmit list is needed, eg. ./examine/latest_resubmit_list_data_18_20210707.txt)

#subprocess.call("./resubmit_tasks.py --tag data --year 2016 --exe", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 2017 --exe", shell=True)
#subprocess.call("./resubmit_tasks.py --tag data --year 2018 --exe", shell=True)
