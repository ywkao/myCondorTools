#!/usr/bin/env python
import glob

#----------------------------------------------------------------------------------------------------

def check_run_scripts():
    files = glob.glob("run*.sh")
    
    for sh in files:
        with open(sh, 'r') as fin:
            for line in fin.readlines():
                if '.py' in line:
                    content = line.strip().split()
                    print content[6]

def get_dir(keyword):
    results = glob.glob("dir*/*%s*_htc.log" % keyword)
    print results[0]

def check_job_id():
    get_dir("195148")

#----------------------------------------------------------------------------------------------------
# Read event Id from log messages!
#----------------------------------------------------------------------------------------------------
def pass_mass_filter(massInfo):
    value = float(massInfo.split()[1])
    is_in_the_sideband = (value > 100. and value < 115.) or (value > 135. and value < 180.)
    is_in_the_sideband = (value >= 100. and value <= 115.) or (value >= 135. and value <= 180.)
    return is_in_the_sideband

def sort_messages(collection):
    #[Info] run:lumi:event = 321475:1013:1601646087, diphoton_mass_: 147.9241260447, score_nrb_ = 0.933749, score_smh_ = 0.843739
    d = {}
    for line in collection:
        mass = float(line.split(', ')[1].split(': ')[1])
        new = line.replace('diphoton_mass_', 'CMS_hgg_mass')
        d[mass] = new

    output = []
    for key in sorted(d.keys()):
        output.append(d[key])

    return output

def lookinng_for_missing_events(evtId):
    if evtId == "317661:672:996396131":
        return True
    elif evtId == "317640:349:478921037":
        return True
    elif evtId == "317392:932:1306452806":
        return True
    elif evtId == "317641:1237:1861009133":
        return True
    elif evtId == "317392:1201:1702819299":
        return True
    elif evtId == "317320:699:1001269663":
        return True
    elif evtId == "302240:496:501669522":
        return True
    else:
        return False

def retrieve_eventId(year):
    # >>> start my check: diphoton_mass_: 99.1134823493
    # diphoton_pt_: 213.1879829279
    # score_nrb_ = 0.89086, score_smh_ = 0.83902
    # [Info] run:lumi:event = 319657:126:204288509
    collection = []
    #for log in glob.glob("../batch_01_workspace/dir_data_%d/*out" % year):
    #for log in glob.glob("../batch_02_ntuples/dir_data_%d/*out" % year):
    for log in glob.glob("dir_data_%d/*out" % year):
        evtInfo = []
        with open(log, 'r') as f:
            for line in f.readlines():
                if '>>> start my check' in line:
                    evtInfo.append(line.strip())
                elif len(evtInfo) > 0:
                    evtInfo.append(line.strip())

                    #>>> start my check (updated): diphoton_mass_: 43.6407277612
                    # Only four lines are needed info for each event
                    if len(evtInfo) == 4:
                        info = evtInfo[-1]
                        mass  = evtInfo[0].split("check (updated): ")[1]
                        score = evtInfo[2]

                        if pass_mass_filter(mass):
                            message = "%s, %s, %s" % (info, mass, score)
                            collection.append(message)
                            #print message

                        evtId = info.split(' = ')[1]
                        if lookinng_for_missing_events(evtId):
                            print ">>> ", log, " has ", evtId
                        # reset for next event
                        evtInfo = []

    collection = sort_messages(collection)
    print ">>> # of events in the sideband: ", len(collection)
    for message in collection:
        print message

if __name__ == "__main__":
    #check_run_scripts()
    #check_job_id()
    #retrieve_eventId(16)
    retrieve_eventId(17)
    #retrieve_eventId(18)


    #>>>  dir_data_18/runJobs3_6200815.54.out  has  317392:932:1306452806
    #>>>  dir_data_18/runJobs3_6200815.16.out  has  317640:349:478921037
    #>>>  dir_data_18/runJobs3_6200815.74.out  has  317661:672:996396131
    #>>>  dir_data_18/runJobs3_6200815.59.out  has  317392:1201:1702819299
    #>>>  dir_data_18/runJobs3_6200815.73.out  has  317641:1237:1861009133
    #>>>  dir_data_18/runJobs3_6200815.60.out  has  317320:699:1001269663
    #>>>  dir_data_17/runJobs2_6200814.56.out  has  302240:496:501669522
