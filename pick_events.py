#!/usr/bin/env python
import subprocess
import parallel_utils
#import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument("-v", help = "version", type=str)
#args = parser.parse_args()

command_list = []
command_list_pick = []
command_list_fetch = []

version = 'v4'

dir_rootfiles = "rootfiles"
dir_temporary = "temporary_%s" % version

list_rootfiles = "%s/latest_list_%s.txt" % (dir_rootfiles, version)
log_double_check = "%s/check.txt" % dir_temporary

counter = 0

# command managers{{{
def command_manager(command):
    global command_list
    command_list.append(command)
    print command

def exe_command_list(useParallel = True):
    global command_list
    if useParallel:
        parallel_utils.submit_jobs(command_list, 10)
    else:
        for command in command_list:
            subprocess.call(command, shell = True)
    command_list = []

def command_manager_pick(command):
    global command_list_pick
    command_list_pick.append(command)
    print command

def exe_command_list_pick():
    global command_list_pick
    parallel_utils.submit_jobs(command_list_pick, 10)
    command_list_pick = []

def command_manager_fetch(command):
    global command_list_fetch
    command_list_fetch.append(command)
    print command

def exe_command_list_fetch():
    global command_list_fetch
    parallel_utils.submit_jobs(command_list_fetch, 10)
    command_list_fetch = []

#}}}
# log and script managers {{{
def shift_counter():
    global counter
    counter += 1

def log_manager(prefix):
    global dir_temporary, counter
    log = "./%s/%s_%d.txt" % (dir_temporary, prefix, counter)
    with open(log, 'w') as f:
        f.write('# >>> start \n')
    return log

def script_manager(prefix):
    global dir_temporary, counter
    sh = "./%s/%s_%d.sh" % (dir_temporary, prefix, counter)
    with open(sh, 'w') as f:
        f.write('#!/bin/bash \n')
    subprocess.call("chmod +x %s" % sh, shell = True)

    return sh 
#}}}

# Data datasets {{{
miniAOD_2016 = [
        "/DoubleEG/Run2016B-17Jul2018_ver2-v1/MINIAOD",
        "/DoubleEG/Run2016C-17Jul2018-v1/MINIAOD",
        "/DoubleEG/Run2016D-17Jul2018-v1/MINIAOD",
        "/DoubleEG/Run2016E-17Jul2018-v1/MINIAOD",
        "/DoubleEG/Run2016F-17Jul2018-v1/MINIAOD",
        "/DoubleEG/Run2016G-17Jul2018-v1/MINIAOD",
        "/DoubleEG/Run2016H-17Jul2018-v1/MINIAOD"
]

miniAOD_2017 = [
        "/DoubleEG/Run2017A-31Mar2018-v1/MINIAOD",
        "/DoubleEG/Run2017B-31Mar2018-v1/MINIAOD",
        "/DoubleEG/Run2017C-31Mar2018-v1/MINIAOD",
        "/DoubleEG/Run2017D-31Mar2018-v1/MINIAOD",
        "/DoubleEG/Run2017E-31Mar2018-v1/MINIAOD",
        "/DoubleEG/Run2017F-31Mar2018-v1/MINIAOD",
        "/DoubleEG/Run2017F-31Mar2018-v1/MINIAOD"
]

miniAOD_2018 = [
        "/EGamma/Run2018A-17Sep2018-v2/MINIAOD",
        "/EGamma/Run2018B-17Sep2018-v1/MINIAOD",
        "/EGamma/Run2018C-17Sep2018-v1/MINIAOD",
        "/EGamma/Run2018D-22Jan2019-v2/MINIAOD"
]

microAOD_2016 = {
        "Run2016B" : ["/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016B-17Jul2018_ver2-v1-86023db6be00ee64cd62a3172358fb9f/USER"],
        "Run2016C" : ["/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016C-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER"],
        "Run2016D" : ["/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016D-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER"],
        "Run2016E" : ["/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016E-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER"],
        "Run2016F" : ["/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016F-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER"],
        "Run2016G" : ["/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016G-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER"],
        "Run2016H" : ["/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016H-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER"]
}

microAOD_2017 = {
        "Run2017B" : ["/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017B-31Mar2018-v1-d9c0c6cde5cc4a64343ae06f842e5085/USER"],
        "Run2017C" : ["/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017C-31Mar2018-v1-d9c0c6cde5cc4a64343ae06f842e5085/USER"],
        "Run2017D" : ["/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017D-31Mar2018-v1-d9c0c6cde5cc4a64343ae06f842e5085/USER"],
        "Run2017E" : ["/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017E-31Mar2018-v1-d9c0c6cde5cc4a64343ae06f842e5085/USER"],
        "Run2017F" : ["/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017F-31Mar2018-v1-6275f8d5048d2e0a580d591e02fde0b8/USER", 
                      "/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017F-31Mar2018-v1-d9c0c6cde5cc4a64343ae06f842e5085/USER"]
}

microAOD_2018 = {
        "Run2018A" : ["/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018A-17Sep2018-v2-dc8e5fb301bfbf2559680ca888829f0c/USER", 
                      "/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018A-17Sep2018-v2-e35808f23b4776d10c777cb2c9d2f07a/USER"],

        "Run2018B" : ["/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018B-17Sep2018-v1-dc8e5fb301bfbf2559680ca888829f0c/USER", 
                      "/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018B-17Sep2018-v1-e35808f23b4776d10c777cb2c9d2f07a/USER"],

        "Run2018C" : ["/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018C-17Sep2018-v1-e35808f23b4776d10c777cb2c9d2f07a/USER"],

        "Run2018D" : ["/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018D-22Jan2019-v2-dc8e5fb301bfbf2559680ca888829f0c/USER"]
}

#}}}
# past{{{
def init_trials():
    # more {{{
    dataset = "/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM"
    dataset = "/EGamma/Run2018A-17Sep2018-v2/MINIAOD"
    code = "316505:913:1183962032"
    
    dataset = "/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM"
    code = "1:234:233701"
    
    command = 'edmPickEvents.py "/Charmonium/Run2018C-17Sep2018-v1/AOD" 319337:60:30203079'
    command = 'edmPickEvents.py "%s" events.txt' % dataset
    command = 'edmPickEvents.py "%s" %s' % (dataset, code)
    command = 'edmCopyPickMerge outputFile=pickevents.root eventsToProcess=1:132:131039 inputFiles=/store/mc/RunIIFall17MiniAODv2/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/250000/74D5B629-1E02-EB11-853F-B499BAAC07AC.root'
    
    command = 'edmCopyPickMerge outputFile=pickevents.root eventsToProcess=1:132:131039 inputFiles=/store/user/lata/Era2017_RR-31Mar2018_v2/v2_p11/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/201110_125406/0000/myMicroAODOutputFile_21.root'
    print command
    subprocess.call(command, shell=True)
    #}}}

def broad_search():
    # more {{{
    command_list = []
    for i in range(25):
        n = i+1
        command = 'edmCopyPickMerge outputFile=pickevents_%d.root eventsToProcess=1:132:131039 inputFiles=/store/user/lata/Era2017_RR-31Mar2018_v2/v2_p11/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/201110_125406/0000/myMicroAODOutputFile_%d.root' % (n, n)
        command_list.append(command)
        #print command
    
    parallel_utils.submit_jobs(command_list, 10)
    #}}}
 
def retrieve_specific_event():
    #more{{{
    global command_list
    command = 'edmCopyPickMerge outputFile=pickevents_1_132_131039_microAOD.root eventsToProcess=1:132:131039 inputFiles=/store/user/lata/Era2017_RR-31Mar2018_v2/v2_p11/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/201110_125406/0000/myMicroAODOutputFile_24.root'
    command_manager(command)

    command = 'edmCopyPickMerge outputFile=pickevents_1_132_131039_miniAOD.root eventsToProcess=1:132:131039 inputFiles=/store/mc/RunIIFall17MiniAODv2/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/250000/74D5B629-1E02-EB11-853F-B499BAAC07AC.root'
    command_manager(command)
    #}}}

def retrieve_specific_event_2nd():
    eventId = "1:132:131124"
    tag = "1_132_131124"

    command_manager( 'edmCopyPickMerge outputFile=pickevents_%s_microAOD.root eventsToProcess=%s inputFiles=/store/user/lata/Era2017_RR-31Mar2018_v2/v2_p11/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/201110_125406/0000/myMicroAODOutputFile_24.root' % (tag, eventId) )

    command_manager( 'edmCopyPickMerge outputFile=pickevents_%s_miniAOD.root eventsToProcess=%s inputFiles=/store/mc/RunIIFall17MiniAODv2/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/250000/74D5B629-1E02-EB11-853F-B499BAAC07AC.root' % (tag, eventId) )
    

def retrieve_data():
    inputFiles = "/store/user/spigazzi/flashgg/Era2017_RR-31Mar2018_v2/legacyRun2FullV1/DoubleEG/Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017E-31Mar2018-v1/190606_095510/0001/myMicroAODOutputFile_1302.root"
    command_manager( 'edmCopyPickMerge outputFile=rootfiles/pickevents_2017E.root eventsToProcess=304204:424390795 inputFiles=%s' % inputFiles )
    inputFiles =  "/store/user/spigazzi/flashgg/Era2018_RR-17Sep2018_v2/legacyRun2FullV2/EGamma/Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018D-22Jan2019-v2/190710_085820/0001/myMicroAODOutputFile_1337.root"
    command_manager( 'edmCopyPickMerge outputFile=rootfiles/pickevents_2018D.root eventsToProcess=320757:440078063 inputFiles=%s' % inputFiles )

#}}}

# das_query_v2() {{{
def das_query_v2():
    txt = "/afs/cern.ch/work/y/ykao/tPrimeExcessHgg/CMSSW_10_6_8/src/tprimetH/special_study_sideband_data/result_compiled_%s.txt" % version
    txt = "/afs/cern.ch/work/y/ykao/tPrimeExcessHgg/CMSSW_10_6_8/src/tprimetH/special_study_sideband_data/result_v4.txt"
    with open(list_rootfiles, 'w') as fout:
        fout.write(">>> start \n")

    with open(txt, 'r') as fin:
        for line in fin.readlines():
            era   = line.strip().split(', ')[-1]
            run   = line.strip().split(' = ')[1].split(',')[0].split(':')[0]
            lumi  = line.strip().split(' = ')[1].split(',')[0].split(':')[1]
            event = line.strip().split(' = ')[1].split(',')[0].split(':')[2]
            eventId = line.strip().split(' = ')[1].split(',')[0]

            fetch  = script_manager("fetch")
            script = script_manager("get_info")
            with open(script, 'a') as fout:
                datasets = locate_data(era, eventId, fout)

                if len(datasets) == 0:
                    continue

                log = log_manager("tmp_das")
                for dataset in datasets:
                    #command_manager_pick( 'edmPickEvents.py "%s" %s 2>&1 >> %s' % (dataset, eventId, log) )

                #exe_command_list_pick()

                    fout.write( 'echo "# %s" >> %s\n' % (eventId, fetch) )
                    #fout.write( 'dasgoclient --query="file dataset=%s instance=prod/phys03 run=%s lumi=%s" 2>&1 >> %s \n' % (dataset, run, lumi, fetch) )
                    das_command = 'dasgoclient --query="file dataset=%s instance=prod/phys03 run=%s lumi=%s"' % (dataset, run, lumi)

                    outputFile = 'outputFile=%s/pickevents_%s_%s.root' % (dir_rootfiles, era, eventId.replace(':', '_'))
                    eventsToProcess = 'eventsToProcess=%s:%s' % (run, event)
                    inputFiles = 'inputFiles=`%s`' % das_command

                    command = 'echo "edmCopyPickMerge %s %s %s" >> %s' % (outputFile, eventsToProcess, inputFiles, fetch)
                    fout.write(command + '\n')

                    command_manager( script )
                    command_manager_fetch( fetch )

                    #command_manager('%s; dasgoclient --query="file dataset=%s instance=prod/phys03 run=%s lumi=%s" 2>&1 >> %s' % (record_eventID, dataset, run, lumi, list_rootfiles) )
                    #/store/user/spigazzi/flashgg/Era2016_RR-17Jul2018_v2/legacyRun2FullV1/DoubleEG/Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016E-17Jul2018-v1/190605_220914/0000/myMicroAODOutputFile_54.root
                    #/store/user/spigazzi/flashgg/Era2016_RR-17Jul2018_v2/legacyRun2FullV1/DoubleEG/Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016H-17Jul2018-v1/190605_221534/0001/myMicroAODOutputFile_1129.root

    exe_command_list()
    #exe_command_list_fetch()

    # workable example 29.Jun.2021
    #command = 'dasgoclient --query="file dataset=/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018D-22Jan2019-v2-dc8e5fb301bfbf2559680ca888829f0c/USER instance=prod/phys03 run=320757 lumi=313"'
    #command = 'dasgoclient --query="file dataset=/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017E-31Mar2018-v1-d9c0c6cde5cc4a64343ae06f842e5085/USER instance=prod/phys03 run=304204 lumi=292"'
#}}}
# download() {{{
def download():
    with open(list_rootfiles, 'r') as f:
        for line in f.readlines():
            if 'store' in line and not '#' in line:
                era =  line.split(',')[0].strip()
                eventId = line.split(',')[1].strip()
                input_file = line.split(',')[2].strip()

                run = eventId.split(':')[0]
                event = eventId.split(':')[2]

                outputFile = 'outputFile=%s/pickevents_%s_%s.root' % (dir_rootfiles, era, eventId.replace(':', '_'))
                eventsToProcess = 'eventsToProcess=%s:%s' % (run, event)
                inputFiles = 'inputFiles="%s"' % input_file

                command = 'edmCopyPickMerge %s %s %s' % (outputFile, eventsToProcess, inputFiles)
                command_manager(command)

                print command

    exe_command_list()
    #exe_command_list(True)
#}}}

#----------------------------------------------------------------------------------------------------

def locate_data(era, eventId, fout):
    datasets = []
    if era == "Era2016":
        datasets = miniAOD_2016
        d_microAOD = microAOD_2016
    elif era == "Era2017":
        datasets = miniAOD_2017
        d_microAOD = microAOD_2017
    elif era == "Era2018":
        datasets = miniAOD_2018
        d_microAOD = microAOD_2018
    else:
        print "[ERROR] format of era is wrong"

    print era, eventId

    log = log_manager("tmp")
    for dataset in datasets:
        #eventId = "320757:313:440078063" # 2018 D
        #eventId = "304204:292:424390795" # 2017 E
        command_manager_pick( 'edmPickEvents.py "%s" %s 2>&1 >> %s' % (dataset, eventId, log) )

    exe_command_list_pick()

    more_era_info = ""
    with open(log, 'r') as f:
        counter_validation = 0
        for line in f.readlines():
            # "  inputFiles=/store/data/Run2016E/DoubleEG/MINIAOD/17Jul2018-v1/20000/642D8776-5E8C-E811-98F8-0CC47AD24D32.root"
            if 'inputFiles' in line and len(line.split('=/')) > 1:
                print line.strip()
                more_era_info = line.strip().split('/')[3]
                print more_era_info
                fout.write("# [miniAOD] %s, %s, %s\n" % (more_era_info, eventId, line.strip()))
                counter_validation += 1

        if counter_validation > 0 :
            return d_microAOD[more_era_info]
        else:
            with open(log_double_check, 'a') as f_debug:
                f_debug.write(era + ', ' + eventId + '\n')
            return []
        
#----------------------------------------------------------------------------------------------------

def das_query():
    txt = "/afs/cern.ch/work/y/ykao/tPrimeExcessHgg/CMSSW_10_6_8/src/tprimetH/special_study_sideband_data/result.txt"
    with open(list_rootfiles, 'w') as fout:
        fout.write(">>> start \n")

    with open(txt, 'r') as fin:
        for line in fin.readlines():
            if '#' in line or not '=' in line:
                continue

            era   = line.strip().split(', ')[-1]
            eventId = line.strip().split(' = ')[1].split(',')[0]
            run   = eventId.split(':')[0]
            lumi  = eventId.split(':')[1]
            event = eventId.split(':')[2]

            with open(list_rootfiles, 'a') as fout:
                fout.write( "# " + line.strip() + '\n' )
                datasets = locate_data(era, eventId, fout)

                if len(datasets) == 0:
                    print "[WARNING] empty return"
                    continue

                for dataset in datasets:
                    more_era_info = dataset.split('-Run')[1].split('-')[0]
                    record_eventID = 'echo "%s, %s" >> %s' % (more_era_info, eventId, list_rootfiles)
                    command_manager('%s; dasgoclient --query="file dataset=%s instance=prod/phys03 run=%s lumi=%s" 2>&1 >> %s' % (record_eventID, dataset, run, lumi, list_rootfiles) )

                    print ">>> check: ", era, more_era_info

            shift_counter() # counter += 1

    exe_command_list()
    subprocess.call("vim %s" % list_rootfiles, shell = True)

#----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    subprocess.call("mkdir -p %s" % dir_rootfiles, shell = True)
    subprocess.call("mkdir -p %s" % dir_temporary, shell = True)

    #das_query()
    #das_query_v2()
    download()
