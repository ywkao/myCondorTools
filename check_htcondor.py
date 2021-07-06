#!/usr/bin/env python
import subprocess
import glob
from termcolor import colored

employed_machines = {'green':[]}
log = "log_submission.txt"
log_machine_status = "tmp_log_machine_status.txt"

def check(machine_id):
    global log, employed_machines
    employed_machines['green'].append(machine_id)
    subprocess.call("mybigbird %s 2>&1 >> %s " % (machine_id, log), shell = True)

def check_bigbird_machine():
    global log
    with open(log, 'w') as f:
        f.write(">>> start checking... \n")

    check("21")
    #check("17")
    #check("14")
    #check("18") # ws1 16
    #check("17") # ws1 18
    #check("11") # nt5 18
    #check("13") # nt5 17
    #check("22") # nt5 16
    #check("19")
    #check("08") # ws1 16 runJobs 5

    #check("15") # ws1 16 runJobs 3
    #check("18") # ws1 16 runJobs 0 failed jobs
    #check("22") # ws1 16 runJobs 1 failed jobs
    #check("12") # ws1 16 runJobs 6
    #check("22") # ws1 16 runJobs 2
    #check("14") # ws1 16 runJobs 4
    #check("16") # ws1 16 runJobs 1

    #check("11") # nt5 16
    #check("13") # nt5 18

def skip():
    #----- patches -----#
    check("09")
    check("15")
        
#def check_machine_status(employed_machines = {}):
def check_machine_status():
    global employed_machines

    subprocess.call("condor_status -schedd > %s" % log_machine_status, shell = True)
    d = {}
    with open(log_machine_status, 'r') as f:
        for line in f.readlines():
            if 'bigbird' in line:
                machine = line.strip().split()[0]
                num_running = int(line.strip().split()[2])
                num_idle = int(line.strip().split()[3])
                pack = "%s:( %d / %d )" % (machine, num_running, num_idle)
                if num_idle > 0:
                    #print "%s: %.2f ( %d / %d )" % (machine, ratio, num_running, num_idle)
                    ratio = float(num_running) / float(num_idle)
                    d[pack] = ratio

    d_sorted = sorted(d.items(), key=lambda x: x[1], reverse=True)
    if len(employed_machines) == 0:
        for ele in d_sorted:
            print "%s: %.2f %s" % (ele[0].split(':')[0], ele[1], ele[0].split(':')[1])
    else:
        for ele in d_sorted:
            machine  = ele[0].split(':')[0]
            moreInfo = ele[0].split(':')[1]
            message = "%s: %.2f %s" % (machine, ele[1], moreInfo)

            # bigbird15.cern.ch
            machineId = machine[7:9]

            # determine text color
            color = 'white'
            for specified_color in employed_machines.keys():
                high_light_ids = employed_machines[specified_color]

                for mId in high_light_ids:
                    if machineId == mId:
                        color = specified_color

            print colored(message, color)
    
    raw_input("Press Enter to continue...")


def look_for_file(keyword):
    targets = glob.glob("ntuples*/*%s*" % keyword)
    for target in targets:
        print target

def submit(machine_id, command):
    global log
    subprocess.call("mybigbird %s && %s && condor_q 2>&1 >> %s" % (machine_id, command, log), shell = True)

def exe_submission():
    global log
    with open(log, 'w') as f:
        f.write(">>> start submission... \n")

    #submit("23", "./exe_data.sh")
    #submit("12", "./exe_Tprime.sh")
    #submit("15", "./exe_sig.sh")

    #submit("08", "./exe_sig.sh")
    #submit("09", "./exe_data_2016.sh")
    #submit("13", "./exe_data_2017.sh")
    #submit("15", "./exe_data_2018.sh")

    #submit("11", "./exe_2016.sh")
    #submit("11", "./exe_2017.sh")
    #submit("11", "./exe_2018.sh")

    #submit("08", "./exe_2016_v1.sh")
    #submit("12", "./exe_2017_v1.sh")
    #submit("13", "./exe_2018_v1.sh")

    #submit("08", "./resubmit_tasks.py")
    #submit("16", "./resubmit_tasks.py")
    #submit("12", "./resubmit_tasks.py")

    #submit("08", "./exe_2017_data.sh")
    #submit("10", "./exe_2016_data.sh")
    #submit("13", "./exe_2018_data.sh")

    #submit("15", "condor_submit dir_data_16/runJobs0.sub")
    #submit("15", "condor_submit dir_data_16/runJobs1.sub")
    #submit("15", "condor_submit dir_data_16/runJobs2.sub")
    #submit("14", "condor_submit dir_data_16/runJobs3.sub")
    #submit("14", "condor_submit dir_data_16/runJobs4.sub")
    #submit("14", "condor_submit dir_data_16/runJobs5.sub")
    #submit("14", "condor_submit dir_data_16/runJobs6.sub")
    #submit("11", "./resubmit_tasks.py")
    #submit("19", "./resubmit_tasks.py")
    #submit("15", "./resubmit_tasks.py")
    #submit("17", "./resubmit_tasks.py")
    submit("14", "./resubmit_tasks.py")


if __name__ == "__main__":
    #ids = {'green':["08", "12", "15", "17", "22"], 'cyan':["11", "13"]}
    check_bigbird_machine() # update employed_machines
    check_machine_status()
    subprocess.call("vim %s" % log, shell = True)

    #look_for_file("7303675.23")
    #look_for_file("8136261.13")
    #exe_submission()
    print ">>> finished!"
