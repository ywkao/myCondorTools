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
parser.add_argument("--manual" , help = "Use manual option --manual", action = "store_true")
parser.add_argument("--check_fatal_messages" , help = "Check fatal messages from err files", action = "store_true")
parser.add_argument("--modify_submission_scripts" , help = "Modify *sh *sub with failed jobs", action = "store_true")

parser.add_argument("--check_root_files" , help = "Check output root files", action = "store_true")
parser.add_argument("--check_resubmit_list_only" , help = "Check resubmit list only", action = "store_true")
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

# manual section
if args.manual:
    log = "examine/mylist.txt"
    check_list = 'examine/check_list.txt'
    resubmit_list = 'examine/latest_resubmit_list.txt'

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
                if '#' in line:
                    continue
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
    id_maps = { "2016":{}, "2017":{}, "2018":{} }
    id_maps = { "16":{}, "17":{}, "18":{} }
    #----------------------------------------------------------------------------------------------------
    # Read filename info of err & categorize
    #----------------------------------------------------------------------------------------------------
    jobs = []
    for line in lines:
        if '#' in line:
            continue
        # hint: dir_data_16/runJobs0_6100824.55.err
        sample_name = line.strip().split('/')[0].split('_')[1]
        year = line.strip().split('/')[0].split('_')[2]
        jobid = line.strip().split('/')[1].split('.')[1]
        runjob = line.strip().split('/')[1].split('_')[0]

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

def check_latest_err_files(extension = "err"):
    command = 'ls -lhrt dir_%s_%d/*.%s > %s' % (tag, year, extension, check_list)
    print command
    subprocess.call(command, shell = True)

    counter = 0
    d_counter = {}
    d_content = {} # store only the latest one
    # -rw-r--r--. 1 ykao zh  23K Jul  3 05:33 dir_data_16/runJobs0_6384557.9.err
    with open(check_list, 'r') as f:
        for line in f.readlines():
            runjob    = line.strip().split()[-1].split('/')[1].split('_')[0]
            processId = int(line.strip().split()[-1].split('/')[1].split('_')[1].split('.')[1])

            counter += 1

            if runjob in d_counter.keys():
                if processId in d_counter[runjob].keys():
                    d_counter[runjob][processId] += 1
                    # Note:
                    # to prevent new jobId from the automatic re-submission
                    # we only keep the oldest log files
                    #d_content[runjob][processId] = line.strip()
                else:
                    d_counter[runjob][processId] = 1
                    d_content[runjob][processId] = line.strip()
            else:
                d_counter[runjob] = {}
                d_counter[runjob][processId] = 1 
                d_content[runjob] = {}
                d_content[runjob][processId] = line.strip()

    # print uniq list
    uniq_list = 'examine/uniq_list_%s_%d_%s_%s.txt' % (tag, year, extension, datetime_tag)
    with open(uniq_list, 'w') as f:
        f.write("# total files: %d\n" % counter)
        for runjob in sorted(d_counter.keys()):
            for key in sorted(d_counter[runjob].keys()):
                message = '%s %2d: %d, %s\n' % ( runjob, key, d_counter[runjob][key], d_content[runjob][key] )
                f.write(message)

    #subprocess.call('vim %s' % uniq_list, shell = True)

    # output with only file name
    if extension == "err":
        with open(check_list, 'w') as fout:
            with open(uniq_list, 'r') as fin:
                for line in fin.readlines():
                    if '#' in line:
                        continue
                    err_file = line.strip().split()[-1]
                    fout.write(err_file + '\n')

    return uniq_list

def check_log(log):
    # check avalable redirectors of root files that are failed to open during submission
    output = "tmp.txt"
    with open(output, 'w') as fout:

        command_list = []
        d_counter = {}
        d_content = {}
        with open(log, 'r') as f:
            for line in f.readlines():
                year = line.strip().split('/')[0].split('_')[-1]
                errFile = line.strip().split('/')[1]
                errFile = "dir_data_%s/%s" % (year, errFile)

                with open(errFile, 'r') as ferr:
                    for subline in ferr.readlines():
                        if 'XrdCl' in subline:
                            rootfile = '/store' + subline.strip().split("',")[0].split("name='")[1].split('store')[1]
                            command = "xrdfs cms-xrd-global.cern.ch locate -h %s" % rootfile
                            command_list.append(command)

                            # sorting
                            id_microAOD = int(rootfile.split('_')[-1].split('.')[0])
                            if id_microAOD in d_counter.keys():
                                    d_counter[id_microAOD] += 1
                                    d_content[id_microAOD] = rootfile
                            else:
                                d_counter[id_microAOD] = 1 
                                d_content[id_microAOD] = rootfile

        for key in sorted(d_counter.keys()):
            message = '%s\n' % ( d_content[key] )
            fout.write(message)

    parallel_utils.submit_jobs(command_list, 10)
    #subprocess.call("vim %s" % output, shell=True)
#[b] XrdCl::File::Open(name='root://xrootd-cms-redir-int.cr.cnaf.infn.it//store/user/spigazzi/flashgg/Era2018_RR-17Sep2018_v2/legacyRun2FullV2/EGamma/Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018D-22Jan2019-v2/190710_085820/0000/myMicroAODOutputFile_29.root', flags=0x10, permissions=0660) => error '[ERROR] Server responded with an error: [3006] tried hosts option not supported.

def get_runJob(root):
    if '2018A' in root and 'dc8e5fb301bfbf2559680ca888829f0c' in root:
        return 'runJobs0'
    elif '2018A' in root and 'e35808f23b4776d10c777cb2c9d2f07a' in root:
        return 'runJobs1'
    elif '2018B' in root and 'dc8e5fb301bfbf2559680ca888829f0c' in root:
        return 'runJobs2'
    elif '2018B' in root and 'e35808f23b4776d10c777cb2c9d2f07a' in root:
        return 'runJobs3'
    elif '2018C' in root and 'e35808f23b4776d10c777cb2c9d2f07a' in root:
        return 'runJobs4'
    elif '2018D' in root and 'dc8e5fb301bfbf2559680ca888829f0c' in root:
        return 'runJobs5'
    else:
        return 'runJobs-999'

def check_root():
    counter = 0
    counter_greater = 0
    #years = [2016, 2017, 2018]
    years = [2018]
    for year in years:
        directory = "dir_data_%d" % year
        directory = "output_data_%d_v1" % year
        os.chdir(directory)
        f_new = glob.glob("*root")
        os.chdir("../")

        backup_directory = "output_data_%d_resubmitLessSizeFile_v3" % year
        #subprocess.call("mkdir -p %s" % backup_directory, shell=True)

        list_jobIds = []
        for root in f_new:
            if 'patch' in root:
                continue
            # sizes
            new_root_file = "%s/%s" % (directory, root)
            old_root_file = "output_data_%d/%s" % (year, root)
            path = "/afs/cern.ch/work/y/ykao/ntuple_production_v5/CMSSW_10_6_8/src/flashgg/Systematics/test"
            old_root_file = "%s/rootfiles_batch1_2018/output_data_%d/%s" % (path, year, root)
            old_root_file = "output_data_%d/%s" % (year, root)

            new_size = os.stat(new_root_file).st_size * (1./1024) # KB
            old_size = os.stat(old_root_file).st_size * (1./1024) # KB

            # convert to runJobs
            jobId = root.split('_USER_')[1].split('.')[0]
            list_jobIds.append(jobId)
            
            runJob = get_runJob(root)
            errFile = "dir_data_%d/%s_2222222.%s.err" % (year, runJob, jobId)

            # print out smaller size
            counter += 1
            if new_size >= old_size:
                counter_greater += 1
                #print "%7.2f, %7.2f, %s" % (new_size, old_size, root)
                #subprocess.call("mv %s %s" % (new_root_file, old_root_file), shell=True)
            else:
                print "%7.2f, %7.2f, %s, %s" % (new_size, old_size, errFile, root)

            # backup
            #subprocess.call("mv %s %s" % (new_root_file, backup_directory), shell=True)

        #print sorted(list_jobIds)

    print "total root files: %d/%d" % (counter_greater, counter)


def check_root_v2():
    counter = 0
    years = [2016, 2017, 2018]
    years = [2018]
    for year in years:
        directory = "output_data_%d" % year
        directory = "dir_data_%d" % year
        os.chdir(directory)
        collection = glob.glob("*root")
        os.chdir("../")

        list_jobIds = []
        for root in collection:
            # sizes
            root_file = "%s/%s" % (directory, root)
            size = os.stat(root_file).st_size * (1./1024) # KB

            if size < 50.:
                print "%7.2f KB, %s" % (size, root)

#----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    subprocess.call("mkdir -p examine", shell = True)

    if args.check_root_files:
        check_root() # new vs old
        #check_root_v2() # old
        #check_log(log)
        #subprocess.call('vim %s' % log, shell = True)


    #---------- main procedure ----------#
    if args.check_fatal_messages:
        if not args.manual:
            uniq_log = check_latest_err_files('log')
            uniq_err = check_latest_err_files('err')
            subprocess.call("vimdiff %s %s" % (uniq_log, uniq_err), shell=True)

        look_for_fatal_messages(check_list)
        extract_jobs_to_resubmit(log, False)

    if args.check_resubmit_list_only:
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
