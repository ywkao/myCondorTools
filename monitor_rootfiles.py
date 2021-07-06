#!/usr/bin/env python
import os
import glob
import subprocess
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year" , help = "year: 16, 17, or 18" , type=int)
args = parser.parse_args()

#2016B  3: 1, output_DoubleEG_spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016B-17Jul2018_ver2-v1-86023db6be00ee64cd62a3172358fb9f_USER_3.root
# EGamma/Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018D-22Jan2019-v2/

year = args.year
moreInfo = False

output = "list_microAOD.txt"
root_file_list = 'examine/root_list_data.txt'
root_file_list = 'examine/root_list_data_20%d_v3p6.txt' % year
root_file_list = 'examine/root_list_data_20%d_v3p7.txt' % year
root_file_list = 'examine/root_list_data_20%d_workspace.txt' % year

def look_for_microAOD_from_errFiles():
    txt = "manual_collectino.txt"

    with open(output, 'w') as fout:
        with open(txt, 'r') as f:
            for line in f.readlines():
                if 'root' in line and not '#' in line:
                    # basic info
                    year = line.strip().split()[0][2:-1]
                    processId = line.strip().split("_USER_")[1].split('.')[0]

                    dataset = line.strip().split(', ')[1].split('_')[1]
                    list_eraInfo = line.strip().split(', ')[1].split('-')[1:8]
                    eraInfo = ""
                    for ele in list_eraInfo:
                        eraInfo = eraInfo + ele + "-" 
                    eraInfo = eraInfo[:-1]

                    name = dataset + "/" + eraInfo
                    fout.write("\n\n\n%s, %s, %s\n" % (year, processId, name))

                    # find files
                    str_search = "dir_data_%s/*.%s.err" % (year, processId)
                    errFiles = glob.glob(str_search) 
                    for err in errFiles:
                        fout.write(err + '\n')
                        with open(err, 'r') as ferr:
                            for err_line in ferr.readlines():
                                if name in err_line:
                                    fout.write( err_line )

def check_rootfiles():
    global year
    cwd = os.getcwd()
    os.chdir("/eos/user/y/ykao/tPrimeExcessHgg/rootfiles/raw/migration_20210628/ntuples_data_20%d" % year) # v3p6
    os.chdir("/afs/cern.ch/work/y/ykao/ntuple_production_v5/CMSSW_10_6_8/src/flashgg/Systematics/test/ntuples_data_20%d" % year) # v3p7
    os.chdir("/afs/cern.ch/work/y/ykao/workspace_v1/CMSSW_10_6_8/src/flashgg/Systematics/test/output_data_%d" % year) # ws1

    rootfiles = glob.glob("*root")

    counter = 0
    total_size = 0.
    d_size = {}
    d_counter = {}
    d_content = {} # store only the latest one
    # output_DoubleEG_spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016H-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f_USER_9.root
    for ntuple in rootfiles:
        era       = ntuple.split('-Run')[1].split('-')[0]
        processId = int(ntuple.split('_USER_')[1].split('.')[0])
        size = os.stat(ntuple).st_size * (1./(1024)) # KB

        counter += 1
        total_size += size

        if era in d_counter.keys():
            if processId in d_counter[era].keys():
                if moreInfo:
                    print ">>> appear twice:"
                    print "- %s" % d_content[era][processId]
                    print "- %s" % ntuple
                d_size[era][processId] = size
                d_counter[era][processId] += 1
                d_content[era][processId] = ntuple
            else:
                d_size[era][processId] = size
                d_counter[era][processId] = 1
                d_content[era][processId] = ntuple
        else:
            d_size[era] = {}
            d_size[era][processId] = size 
            d_counter[era] = {}
            d_counter[era][processId] = 1 
            d_content[era] = {}
            d_content[era][processId] = ntuple
            
    os.chdir(cwd)

    # start writing info
    with open(root_file_list, 'w') as f:
        total_size = total_size * (1./1024) # MB
        f.write("total files: %d\n" % counter)
        f.write("total size : %.2f MB\n" % total_size)
        for era in sorted(d_counter.keys()):
            for key in sorted(d_counter[era].keys()):
                message = '%s %2d: %d, %.2f kB, %s\n' % ( era, key, d_counter[era][key], d_size[era][key], d_content[era][key] )
                f.write(message)

    command = 'vim %s' % (root_file_list)
    subprocess.call(command, shell = True)

if __name__ == "__main__":
    #look_for_microAOD_from_errFiles()
    check_rootfiles()
