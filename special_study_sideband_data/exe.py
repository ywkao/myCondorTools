#!/usr/bin/env python
import subprocess

def check(directory, backup):
    subprocess.call("./get_info.py 2>&1 > raw.txt --read --input %s" % directory, shell=True)
    subprocess.call("./get_info.py --convert", shell=True)
    subprocess.call("mkdir -p %s" % backup, shell=True)
    subprocess.call("mv raw.txt list_formated.txt list_formated_sorted.txt %s" % backup, shell=True)

def check_all_workspace():
    path = "/afs/cern.ch/work/y/ykao/workspace_v2/CMSSW_10_6_8/src/flashgg/Systematics/test"
    path = "/afs/cern.ch/work/y/ykao/workspace_v2/CMSSW_10_6_8/src/flashgg/Systematics/test/batch_workspace_SR"
    path = "/eos/user/y/ykao/tPrimeExcessHgg/rootfiles/forPrafulla/20210724"
    path = "/eos/user/y/ykao/tPrimeExcessHgg/rootfiles/forPrafulla/control_region_study"

    workspace = ["workspace_M600_M700", "workspace_M800_M1000", "workspace_M1100_M1200"]
    outputs = ["output_data_16", "output_data_17", "output_data_18"]

    for ws in workspace:
        for out in outputs:
            print ">>> checking: ", ws, out
            d = path + "/" + ws + "/" + out
            year = out.split('_')[-1]
            backup = ws + "_" + year
            check(d, backup)

def test():
    subprocess.call("time ./get_info.py --test", shell=True)

if __name__ == "__main__":
    check_all_workspace()
    #test()

    #check("/afs/cern.ch/work/y/ykao/workspace_v2/CMSSW_10_6_8/src/flashgg/Systematics/test/runWS", "control_region_study_had")
    #check("/afs/cern.ch/work/y/ykao/workspace_v2/CMSSW_10_6_8/src/flashgg/Systematics/test/runWS", "control_region_study_lep")

    #subprocess.call("nl _16/list_formated_sorted.txt | tail -n1", shell=True)
    #subprocess.call("nl _17/list_formated_sorted.txt | tail -n1", shell=True)
    #subprocess.call("nl _18/list_formated_sorted.txt | tail -n1", shell=True)
    
    #subprocess.call("nl workspace_M600_M700_16/list_formated_sorted.txt | tail -n1", shell=True)
    #subprocess.call("nl workspace_M600_M700_17/list_formated_sorted.txt | tail -n1", shell=True)
    #subprocess.call("nl workspace_M600_M700_18/list_formated_sorted.txt | tail -n1", shell=True)
    


#"/eos/user/y/ykao/tPrimeExcessHgg/rootfiles/forPrafulla/20210724/workspace_M800_M1000"
#"/eos/user/y/ykao/tPrimeExcessHgg/rootfiles/forPrafulla/20210724/workspace_M1100_M1200"
