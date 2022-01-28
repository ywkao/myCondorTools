#!/usr/bin/env python
import json
import os, glob

log = "log_read_json.txt"

def load(fin):
    with open(fin) as f: data = json.load(f)
    with open(log, 'a') as l:
        l.write( fin + ":\n" )
        for key in data.keys(): l.write( key + "\n" )
        l.write("\n")
    return data

def merge(d1, d2):
    for key, value in d2.items(): d1[key] = value
    return d1

def write(data, output):
    with open(output, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
        f.write('\n')

def init_log(my_record_file):
    global log
    log = my_record_file
    with open(log, 'w') as l: l.write("")

def read_info_only(myListJson, my_record_file):
    init_log(my_record_file)
    for f in myListJson: data = load(f)
    print ">>> content in", log

def update_catelogue(): #{{{
    list_json_files = [
        "datasets.json",
        "datasets_1.json",
        "datasets_10.json",
        "datasets_11.json",
        "datasets_2.json",
        "datasets_3.json",
        "datasets_4.json",
        "datasets_5.json",
        "datasets_7.json",
        "datasets_9.json",
    ]

    lata = "/afs/cern.ch/work/l/lata/public/ForPrafulla/Era2018_legacy_v1/"
    mine = "MetaData/data/tmp_Era2018_legacy_v1/"
    goal = "MetaData/data/Era2018_legacy_v1/" # need to check existence of the directory

    combine_json = True
    if combine_json:
        for f in list_json_files:
            output = goal + f
            print f, ":"
            d1 = load( mine + f )
            d2 = load( lata + f )
            data = merge(d1, d2)
            write(data, output)
            print ""

    check_output = False
    if check_output:
        for f in list_json_files:
            print f, ":"
            data = load( goal + f )
            print ""
 #}}}

if __name__ == "__main__":
    #update_catelogue()
    #read_info_only(glob.glob("/afs/cern.ch/work/y/ykao/ntuple_production_v7/CMSSW_10_6_8/src/flashgg/MetaData/data/Era2016_RR-17Jul2018_v[23]/*json"), "check_2016_v3.txt")
    #read_info_only(glob.glob("/afs/cern.ch/work/y/ykao/workspace_v2/CMSSW_10_6_8/src/flashgg/MetaData/data/Era2016_RR-17Jul2018_v[23]/*json"), "check_2016_v2.txt")
    read_info_only(glob.glob("MetaData/data/Era2016_RR-17Jul2018_v2/*json"), "check_reReco_2016.txt")
    read_info_only(glob.glob("MetaData/data/Era2017_RR-31Mar2018_v2/*json"), "check_reReco_2017.txt")
    read_info_only(glob.glob("MetaData/data/Era2018_RR-17Sep2018_v2/*json"), "check_reReco_2018.txt")
    #read_info_only(glob.glob("MetaData/data/Era2017_legacy_v1/*json"), "check_2017.txt")
    #read_info_only(glob.glob("MetaData/data/Era2018_legacy_v1/*json"), "check_2018.txt")

    #data = load("/afs/cern.ch/work/l/lata/public/ForPrafulla/Era2018_legacy_v1/datasets_9.json")
    print ">>> finished!"
