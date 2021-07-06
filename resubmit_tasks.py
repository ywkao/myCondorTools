#!/usr/bin/env python
import os
import subprocess
import glob
import parallel_utils
import datetime
today = datetime.datetime.today()
datetime_tag = today.strftime("%Y%m%d")

#----------------------------------------------------------------------------------------------------
# manual options
#----------------------------------------------------------------------------------------------------
tag = "tprime"
tag = "sig"
tag = "data"

year = 161718
year = 18

#----------------------------------------------------------------------------------------------------
# files
#----------------------------------------------------------------------------------------------------
log = "examine/mylist_%s_%d_%s.txt" % (tag, year, datetime_tag)
check_list = 'examine/check_list_%s_%d_%s.txt' % (tag, year, datetime_tag)
resubmit_list = 'examine/latest_resubmit_list_%s_%d_%s.txt' % (tag, year, datetime_tag)

ongoing_list = 'examine/ongoing_list_%s.txt' % tag
reResubmit_list = 'examine/reResubmit_list_%s.txt' % tag

#----------------------------------------------------------------------------------------------------
# functions
#----------------------------------------------------------------------------------------------------

def check_err_file(target, keyword = "Fatal"):
    has_fatal_message = False
    with open(target, 'r') as fin:
        lines = fin.readlines()
        for line in lines:
            if keyword in line:
                has_fatal_message = True
                break
    return has_fatal_message

def look_for_fatal_messages():
    global log
    with open(log, 'w') as f:
        targets = glob.glob("dir_%s*/*err" % tag)
        for target in targets:
            has_fatal_message = check_err_file(target)
            if has_fatal_message:
                f.write(target + '\n')

    print ">>> file(s) with fatal messages are here: %s" % log

def look_for_fatal_messages(txt, keyword = "Fatal"):
    global log
    print txt
    with open(log, 'w') as f:
        with open(txt, 'r') as fin:
            for line in fin.readlines():
                target = line.strip()
                print target
                has_fatal_message = check_err_file(target, keyword)
                if has_fatal_message:
                    f.write(target + '\n')

    print ">>> file(s) with fatal messages are here: %s" % log

#----------------------------------------------------------------------------------------------------

def write_a_file(filename, keyword, new_content):
    # only the line with keyword will be replaced with new content
    # all other contents are kept as the same as original files, *.backup
    filename_backup = filename + ".backup"

    # command to execute only once (preserve original version)
    to_copy = not os.path.exists(filename_backup)
    if to_copy:
        subprocess.call("cp -p %s %s" % (filename, filename_backup), shell = True)

    # start to copy and replace specific line with new content
    with open(filename, 'w') as fout:
        with open(filename_backup, 'r') as fread:
            lines = fread.readlines()
            for line in lines:
                if keyword in line:
                    fout.write(new_content + "\n")
                else:
                    fout.write(line.rstrip() + "\n")

    # double check
    command = ' echo "double check: `grep %s %s`"' % (keyword, filename)
    subprocess.call(command, shell = True)

#----------------------------------------------------------------------------------------------------

def extract_jobs_to_resubmit(mylist, to_write):
    f = open(mylist, 'r')
    lines = f.readlines()
    
    #----------------------------------------------------------------------------------------------------
    # id_maps for data
    #----------------------------------------------------------------------------------------------------
    sample_name = ""
    id_maps = { "16":{}, "17":{}, "18":{} }
    #----------------------------------------------------------------------------------------------------
    # Read filename info of err & categorize
    #----------------------------------------------------------------------------------------------------
    jobs = []
    for line in lines:
        # hint: dir_data_16/runJobs0_6100824.55.err
        sample_name = line.split('/')[0].split('_')[1]
        year = line.split('/')[0].split('_')[2]
        jobid = line.split('/')[1].split('.')[1]
        runjob = line.split('/')[1].split('_')[0]

        current_key_list = id_maps[year].keys()
        if runjob in current_key_list:
            id_maps[year][runjob].append(int(jobid))
        else:
            id_maps[year][runjob] = []
            id_maps[year][runjob].append(int(jobid))
        #print ">>>>> ", year, runjob, jobid
    #----------------------------------------------------------------------------------------------------
    # Translate info into jobIdsMap
    #----------------------------------------------------------------------------------------------------
    for key in id_maps.keys(): # ex. key = "16"
        d_year = id_maps[key]
        for subkey in d_year.keys(): # ex. subkey = "runJobs0"
            # make list of jobid unique and sorted
            mylist = d_year[subkey]
            myset = set(mylist)
            d_year[subkey] = list(myset)
            d_year[subkey].sort()
            #print key, subkey, d_year[subkey]

            # create id string
            id_string = ""
            counter = 0
            for ele in d_year[subkey]:
                if id_string == "":
                    id_string += str(ele)
                else:
                    id_string = id_string + " " + str(ele)
                counter += 1

            filename = "dir_%s_%s/%s.sh" % (sample_name, key, subkey)
            new_content  = "declare -a jobIdsMap=(%s)" % id_string
            new_queue = "queue %d" % counter
            print filename, new_queue, new_content

            # Append if there is any failed job
            job = "dir_%s_%s/%s.sub" % (sample_name, key, subkey)
            if counter > 0:
                jobs.append(job)

                if to_write:
                    # modify "queue" in *.sub
                    write_a_file(job, 'queue', new_queue)

                    # modify "declare" in *.sh
                    write_a_file(filename, 'declare', new_content)

                    print "\n-----\n"

    #----------------------------------------------------------------------------------------------------
    # Write jobs in resubmit_list
    #----------------------------------------------------------------------------------------------------
    jobs_uniq = list(set(jobs))
    with open(resubmit_list, 'w') as f:
        for job in jobs_uniq:
            f.write(job + '\n')

    print ">>> resubmit_list can be found here: %s" % resubmit_list
    subprocess.call('cat %s' % resubmit_list, shell = True)

#----------------------------------------------------------------------------------------------------

def resubmit(txt, exe=False):
    # submit jobs listed in resubmit_list
    command_list = []
    with open(txt, 'r') as f:
        jobs = f.readlines()
        for job in jobs:
            if '#' in job:
                continue
            command = 'condor_submit %s' % job.rstrip()
            command_list.append(command)
            print command

    if exe:
        parallel_utils.submit_jobs(command_list, 24)

#----------------------------------------------------------------------------------------------------

def get_runjob(f, directory, keyword):
    suffix = "_htc.log"
    suffix = ".err"

    # check complete jobs (has summary & no fatal messages)
    list_all_jobs = []
    list_complete = []
    err_files = glob.glob("%s/*%d*%s" % (directory, keyword, suffix))
    for err in err_files:
        # dir_data_16/runJobs5_6165888.13.err
        process_id = int(err.split('.')[1])
        list_all_jobs.append(process_id)

        has_fatal_message = check_err_file(err)
        has_summary_message = check_err_file(err, 'MessageLogger Summary')
        if has_summary_message and not has_fatal_message:
            list_complete.append(process_id)
            #print err

    list_all_jobs.sort()
    list_complete.sort()
    print "[Info] completed jobs: ", list_complete

    # not finished jobs = count only once
    d = {}
    for ele in list_all_jobs:
        d[ele] = 1
    for ele in list_complete:
        d[ele] += 1

    list_to_resubmit = []
    files_to_resubmit = []
    for key in d.keys():
        if d[key]==1:
            list_to_resubmit.append(key)
            # find out the file if the id(s) are identified
            for err in err_files:
                process_id = int(err.split('.')[1])
                if key == process_id:
                    files_to_resubmit.append(err)
                    f.write( err + '\n' )

    tmp_sh = "tmp_job_remove_list.sh"
    with open(tmp_sh, 'w') as f_tmp:
        f_tmp.write("#!/bin/bash\n")
        subprocess.call("chmod +x %s" % tmp_sh, shell = True)
        for jobId in list_to_resubmit:
            f_tmp.write("condor_rm %d.%d\n" % (keyword, jobId))

    subprocess.call("vim %s" % tmp_sh, shell = True)
    print ">>> Remember to remove jobs manually: ./%s" % tmp_sh

def check_submitted_jobs():
    with open(ongoing_list, 'w') as f:
        #get_runjob(f, "dir_data_16", 6165888)
        get_runjob(f, "dir_data_16", 11683455)

    subprocess.call("vim %s" % ongoing_list, shell = True)

    skip = True
    if not skip:
        with open(reResubmit_list, 'w') as f:
            with open(ongoing_list, 'r') as fin:
                d = {}
                for line in fin.readlines():
                    # ex. dir_data_18/runJobs3_9166897.5_htc.log
                    directory = line.strip().split('/')[0]
                    runJob = line.strip().split('/')[1].split('_')[0]
                    ele = directory + "/" + runJob + ".sub"
                    if ele in d:
                        d[ele] += 1
                    else:
                        d[ele] = 1

                for key in d.keys():
                    f.write(key + '\n')
                    print "%s: %d" % (key, d[key])

def create_check_list():
    command = 'ls -lhrt dir_%s*/*err > %s' % (tag, check_list)
    subprocess.call(command, shell = True)

    command = 'vim %s' % (check_list)
    subprocess.call(command, shell = True)

#----------------------------------------------------------------------------------------------------

def check_latest_err_files(year):
    command = 'ls -lhrt dir_%s_%d/*.err > %s' % (tag, year, check_list)
    print command
    subprocess.call(command, shell = True)

    d_counter = {}
    d_content = {} # store only the latest one
    # -rw-r--r--. 1 ykao zh  23K Jul  3 05:33 dir_data_16/runJobs0_6384557.9.err
    with open(check_list, 'r') as f:
        for line in f.readlines():
            runjob    = line.strip().split()[-1].split('/')[1].split('_')[0]
            processId = int(line.strip().split()[-1].split('/')[1].split('_')[1].split('.')[1])

            if runjob in d_counter.keys():
                if processId in d_counter[runjob].keys():
                    d_counter[runjob][processId] += 1
                    d_content[runjob][processId] = line.strip()
                else:
                    d_counter[runjob][processId] = 1
                    d_content[runjob][processId] = line.strip()
            else:
                d_counter[runjob] = {}
                d_counter[runjob][processId] = 1 
                d_content[runjob] = {}
                d_content[runjob][processId] = line.strip()

    uniq_list = 'examine/uniq_list_%s_%d_%s.txt' % (tag, year, datetime_tag)
    with open(uniq_list, 'w') as f:
        for runjob in sorted(d_counter.keys()):
            for key in sorted(d_counter[runjob].keys()):
                message = '%s %2d: %d, %s\n' % ( runjob, key, d_counter[runjob][key], d_content[runjob][key] )
                f.write(message)

    #runJobs0  0: 2, -rw-r--r--. 1 ykao zh 140K Jul  4 16:15 dir_data_16/runJobs0_1591042.0.err
    with open(check_list, 'w') as fout:
        with open(uniq_list, 'r') as fin:
            for line in fin.readlines():
                err_file = line.strip().split()[-1]
                fout.write(err_file + '\n')

    command = 'vim %s' % (check_list)
    command = 'vim %s' % (uniq_list)
    subprocess.call(command, shell = True)

#----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    subprocess.call("mkdir -p examine", shell = True)
    #---------- check for the first time ----------#
    #look_for_fatal_messages()
    #extract_jobs_to_resubmit(log, False)
    #extract_jobs_to_resubmit(log, True)
    #resubmit(resubmit_list, True)

    #---------- check with manual err list ----------#
    #create_check_list()
    #look_for_fatal_messages(check_list)
    #extract_jobs_to_resubmit(log, False)
    #extract_jobs_to_resubmit(log, True)
    #resubmit(resubmit_list, False)
    #resubmit(resubmit_list, True)

    #resubmit('examine/manual_submit.txt', False)
    #resubmit('examine/manual_submit.txt', True)

    #---------- check idle/failed ----------#
    #check_submitted_jobs()
    #extract_jobs_to_resubmit(ongoing_list, False)
    #extract_jobs_to_resubmit(ongoing_list, True)
    #resubmit(resubmit_list, False)
    #resubmit(resubmit_list, True)

    #---------- check summary messages ----------#
    #check_latest_err_files(year)
    #look_for_fatal_messages(check_list)
    #extract_jobs_to_resubmit(log, False)
    #extract_jobs_to_resubmit(log, True)
    #resubmit(resubmit_list, False)
    #resubmit(resubmit_list, True)

    #---------- manual section ----------#
    #extract_jobs_to_resubmit("examine/mylist.txt", False)
    #extract_jobs_to_resubmit("examine/mylist.txt", True)
    #resubmit(resubmit_list, False)
    resubmit(resubmit_list, True)

    #look_for_fatal_messages("examine/mylist_data_20210704.txt", 'MessageLogger Summary')
    #look_for_fatal_messages("examine/mylist_data_20210704.txt")
    print ">>> finished!"

    #---------- others ----------#
    #look_for_fatal_messages("examine/check_list.txt")
    #look_for_fatal_messages("examine/mylist_sig_20210701.txt")
