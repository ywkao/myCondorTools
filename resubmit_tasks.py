#!/usr/bin/env python
import os
import subprocess
import glob
import parallel_utils
import datetime
today = datetime.datetime.today()
datetime_tag = today.strftime("%Y%m%d")

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--tag" , help = "type of sample (data/sig/tprime); need to meet name of directory" , type=str, required = True)
parser.add_argument("--year" , help = "year: 16, 17, or 18" , type=int, required = True)
parser.add_argument("--exe" , help = "Execute submission if adding --exe", action = "store_true")
parser.add_argument("--check_fatal_messages" , help = "Check fatal messages from err files", action = "store_true")
parser.add_argument("--modify_submission_scripts" , help = "Modify *sh *sub with failed jobs", action = "store_true")
args = parser.parse_args()

#----------------------------------------------------------------------------------------------------
# manual options
#----------------------------------------------------------------------------------------------------
tag = "tprime"
tag = "sig"
tag = "data"
tag = args.tag

year = 161718
year = args.year

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

def look_for_fatal_messages(txt, keyword = "Fatal"):
    print ">>> input files: %s" % txt
    global log
    with open(log, 'w') as f:
        with open(txt, 'r') as fin:
            for line in fin.readlines():
                target = line.strip()
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

    if not to_write:
        raw_input("Press Enter to continue...")

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

def check_latest_err_files():
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

    #---------- main procedure ----------#
    if args.check_fatal_messages:
        check_latest_err_files()
        look_for_fatal_messages(check_list)
        extract_jobs_to_resubmit(log, False)

    if args.modify_submission_scripts:
        extract_jobs_to_resubmit(log, True)
        resubmit(resubmit_list, False)

    if args.exe:
        resubmit(resubmit_list, True)

    #---------- manual section ----------#
    #look_for_fatal_messages("examine/check_list.txt")
    #look_for_fatal_messages("examine/mylist_data_20210704.txt", 'MessageLogger Summary')
    #extract_jobs_to_resubmit("examine/mylist.txt", False)
    #extract_jobs_to_resubmit("examine/mylist.txt", True)
    #resubmit('examine/manual_submit.txt', False)
    #resubmit('examine/manual_submit.txt', True)

    print ">>> finished!"
