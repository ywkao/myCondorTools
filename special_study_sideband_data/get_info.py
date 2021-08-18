#!/usr/bin/env python
import os
import glob
import subprocess
import ROOT
ROOT.gROOT.SetBatch(True)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input" , help = "Input directory" , type=str)
parser.add_argument("--read" , help = "Read workspace", action = "store_true")
parser.add_argument("--convert" , help = "Convert info & sorting", action = "store_true")
parser.add_argument("--test" , help = "Test purpose", action = "store_true")
args = parser.parse_args()

cwd = os.getcwd()
txt_2016 = "%s/../plots/log/info_Data_Era2016_sideband.txt" % cwd
txt_2017 = "%s/../plots/log/info_Data_Era2017_sideband.txt" % cwd
txt_2018 = "%s/../plots/log/info_Data_Era2018_sideband.txt" % cwd

# more{{{

list_formated = "list_formated.txt"
list_formated_v2 = "list_formated_v2.txt"
list_no_found = "list_formated_v3.txt"

my_output_file = "dummy.txt" # result.txt
fout = open(my_output_file, 'w')
#}}}

counter = 0
counter_no_match = 0

#----------------------------------------------------------------------------------------------------

def read_ws_data():
    path = "/afs/cern.ch/work/y/ykao/workspace_v2/CMSSW_10_6_8/src/flashgg/Systematics/test/batch_01_workspace/output_data_17"
    path = "/eos/user/y/ykao/tPrimeExcessHgg/rootfiles/forPrafulla/workspace_M600_M700/output_data_17"
    path = "/afs/cern.ch/work/y/ykao/workspace_v1/CMSSW_10_6_8/src/flashgg/Systematics/test/output_data_16"
    path = args.input
    os.chdir(path)

    for root in glob.glob("*.root"):
        f = ROOT.TFile(root)
        w = f.Get("tagsDumper/cms_hgg_13TeV")
        dataFull = w.data("Data_13TeV_THQHadronicTag")
        #dataFull = w.data("Data_13TeV_THQLeptonicTag")
        entries = dataFull.sumEntries()
        
        print entries
        for i in range(int(entries)):
            dataFull.get(i).Print("CMS_hgg_mass")

    # Note: info are stored with  2>&1 > raw.txt

#----------------------------------------------------------------------------------------------------

def convert():
    subprocess.call("cp raw.txt tmp.txt", shell=True)
    with open("raw.txt", 'w') as fout:
        with open("tmp.txt", 'r') as fin:
            for line in fin.readlines():
                if 'RooReal' in line:
                    fout.write(line.strip() + '\n')
    #subprocess.call("vim raw.txt", shell=True)


    with open(list_formated, 'w') as f:
        with open("raw.txt", 'r') as fin:
            info = ""
            for line in fin.readlines():
                if 'CMS' in line:
                    info = ""
                    info += line.split("::")[1].strip() 
                if 'sigmaMoM_decorr' in line:
                    info += ", "
                    info += line.split("::")[1].strip() 
                    f.write(info + '\n')

    #print ">>> end of conversion. New file: list_formated.txt"

#----------------------------------------------------------------------------------------------------
# self-define sorters
#----------------------------------------------------------------------------------------------------
# more{{{
def sort_my_offline_format(txt):
    #[Info] Run:Lumi:Event = 274971:221:338418224, CMS_hgg_mass = 113.778328, sigmaMoM_decorr = 0.024490
    d_my_sideband = {}
    with open(txt, 'r') as f:
        for line in f.readlines():
            if not "Run:" in line:
                continue

            mass = line.strip().split(',')[1].split(' = ')[1]
            content = 'CMS' + line.strip().split(', CMS')[1] + line.strip().split(', CMS')[0]
            d_my_sideband[mass] = content

    stem = txt.split('.txt')[0]
    with open(stem + "_sorted.txt", 'w') as f:
        for key in sorted(d_my_sideband.keys()):
            f.write(d_my_sideband[key] + '\n')

def sort_my_workspace_format(txt):
    #[Info] run:lumi:event = 316766:224:274180403, diphoton_mass_: 102.5710719831, score_nrb_ = 0.768916, score_smh_ = 0.876383
    #[Info] run:lumi:event = 273158:1049:1486148462, CMS_hgg_mass: 100.3635218335, score_nrb_ = 0.913535, score_smh_ = 0.864169
    d_my_sideband = {}
    with open(txt, 'r') as f:
        for line in f.readlines():
            if not "run:" in line:
                continue

            print line
            mass = line.strip().split(',')[1].split(': ')[1]
            #content = 'CMS_hgg_mass = ' + line.strip().split(', diphoton_mass_: ')[1] + line.strip().split(', diphoton')[0]
            content = 'CMS' + line.strip().split(', CMS')[1] + line.strip().split(', CMS')[0]
            d_my_sideband[mass] = content

    with open(txt.split('.')[0] + "_sorted.txt", 'w') as f:
        for key in sorted(d_my_sideband.keys()):
            f.write(d_my_sideband[key] + '\n')

def sort_prafulla_workspace_format():
    #CMS_hgg_mass = 104.536, sigmaMoM_decorr = 0.00908527
    d_ws_sideband = {}
    with open("list_formated.txt", 'r') as f:
        for line in f.readlines():
            mass = line.strip().split(', ')[0].split(' = ')[1]
            if not (float(mass) > 115. and float(mass) < 135.):
                d_ws_sideband[mass] = line.strip()

    with open("list_formated_sorted.txt", 'w') as f:
        for key in sorted(d_ws_sideband.keys()):
            f.write(d_ws_sideband[key] + '\n')

#}}}

def my_sorter():
    #sort_my_offline_format("check_M1100_M1200_2018.txt")
    #subprocess.call("vim check_M1100_M1200_2018_sorted.txt", shell=True)

    #sort_my_workspace_format("another.txt")
    #sort_my_workspace_format("list_2017_events.txt")
    #sort_my_workspace_format("log_ntuples_18.txt")
    #sort_my_workspace_format("latest_check_2016.txt")
    #sort_my_workspace_format("latest_check_2017.txt")
    #sort_my_workspace_format("latest_check_2018.txt")

    sort_prafulla_workspace_format()

    counter = 0
    with open("list_formated_sorted.txt", 'r') as fin:
        for line in fin.readlines():
            if 'CMS' in line:
                counter += 1

    print ">>> # entries: ", counter
    #subprocess.call('echo ">>> # entries: `grep -c CMS list_formated_sorted.txt`"', shell=True)
    #subprocess.call("vim list_formated_sorted.txt", shell=True)

    exe = False
    if exe:
        sort_my_offline_format("log_looper_Data_Era2016_v3p7_20210713_0")
        sort_my_offline_format("log_looper_Data_Era2017_v3p7_20210713_1")
        sort_my_offline_format("log_looper_Data_Era2018_v3p7_20210713_2")

        sort_my_workspace_format("myworkspace_18.txt")

        sort_prafulla_workspace_format()

    # comparison result: to_be_investigate.txt

# rescue_no_found_entries() {{{
def rescue_no_found_entries():
    global fout

    with open(list_formated_v2, 'r') as f:
        for line in f.readlines():
            #[WARNING] no match for mass = 148.591, sigmaMoM_decorr = 0.0145326
            CMS_hgg_mass    = line.strip().split(', ')[0].split(' = ')[1]
            sigmaMoM_decorr = line.strip().split(', ')[1].split(' = ')[1]

            look_up_tables(CMS_hgg_mass[0:6], sigmaMoM_decorr)

    global counter_no_match
    print "counter_no_match: ", counter_no_match

    fout.close()
#}}}

#----------------------------------------------------------------------------------------------------
# more{{{
def read_a_table(txt, mass, sigmaMoM_decorr, bool_search_through_str = False):
    global fout, counter # count matched results
    era = "Era" + txt.split('Era')[1].split('_')[0]
    with open(txt, 'r') as f:
        for line in f.readlines():
            if bool_search_through_str:
                # search through string
                if str(mass) in line:
                    counter += 1
                    fout.write(line.strip() + ", " + era + '\n')
            else:
                # search through value
                #[Info] Run:Lumi:Event = 275068:170:342221127, CMS_hgg_mass = 102.776138, sigmaMoM_decorr = 0.011120, Era2016
                if 'CMS_hgg_mass' in line:
                    my_mass = float(line.strip().split(',')[1].split(' = ')[1])
                    ratio_mass = (my_mass - mass) / mass

                    my_sigma = float(line.strip().split(',')[2].split(' = ')[1])
                    ratio_sigma = (my_sigma - sigmaMoM_decorr) / sigmaMoM_decorr
                    #if abs(ratio_mass) < 1e-5 and abs(ratio_sigma) < 5e-1:
                    if abs(ratio_mass) < 1e-5 and abs(ratio_sigma) < 1e-1:
                        counter += 1
                        fout.write(line.strip() + ", " + era + '\n')
            

def look_up_tables(mass, sigmaMoM_decorr):
    global counter, counter_no_match

    counter = 0 # init for each entry
    read_a_table(txt_2016, float(mass), float(sigmaMoM_decorr))
    read_a_table(txt_2017, float(mass), float(sigmaMoM_decorr))
    read_a_table(txt_2018, float(mass), float(sigmaMoM_decorr))

    # check searching result
    if counter == 0 and not (float(mass) > 115. and float(mass) < 135.):
        counter_no_match += 1
        with open(list_no_found, 'a') as f:
            f.write("[WARNING] no match for mass = %s, sigmaMoM_decorr = %s\n" %(mass, sigmaMoM_decorr))

def batch_search():
    global fout

    counter_window = 0
    counter_sideband = 0
    with open("to_be_investigate.txt", 'r') as f:
        #CMS_hgg_mass = 104.536, sigmaMoM_decorr = 0.00908527
        for line in f.readlines():
            if 'CMS' in line and not '#' in line:
                CMS_hgg_mass    = line.strip().split(', ')[0].split(' = ')[1]
                sigmaMoM_decorr = line.strip().split(', ')[1].split(' = ')[1]

                look_up_tables(CMS_hgg_mass, sigmaMoM_decorr)

                if float(CMS_hgg_mass) > 115. and float(CMS_hgg_mass) < 135.:
                    counter_window += 1
                else:
                    counter_sideband += 1

    global counter_no_match
    print "counter_window: ", counter_window
    print "counter_sideband: ", counter_sideband
    print "counter_no_match: ", counter_no_match

    fout.close()


def compare():
    with open('result.txt', 'r') as f:
        for evt in f.readlines():
            if '#' in evt:
                continue
            # [Info] run:lumi:event = 317661:672:996396131, CMS_hgg_mass = 102.7698851824, score_nrb_ = 0.875308, score_smh_ = 0.868711, Era2018
            evtId = evt.split(',')[0].split(' = ')[1]

            #with open('latest_check_2017_sorted.txt', 'r') as fin:
            #with open('log_looper_Data_Era2017_20210718_1', 'r') as fin:
            #with open('log_looper_Data_Era2018_20210718_2', 'r') as fin:

            for log in glob.glob("../plots/log/*"):
                with open(log, 'r') as fin:
                    for line in fin.readlines():
                        if evtId in line:
                            print ">>> Yes! it is there, ", line.strip()

#}}}

if __name__ == "__main__":
    if args.read:
        read_ws_data()

    if args.convert:
        convert()
        my_sorter() # sort mass & filter out signal window

    if args.test:
        my_sorter() # sort mass & filter out signal window

    #compare()
    #batch_search()

    #rescue_no_found_entries()
