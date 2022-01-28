#!/usr/bin/env python
import subprocess
import json
import sample_manager as sm

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-e", help = "enable to create scripts", action = "store_true")
args = parser.parse_args()

data_xsec = {}
#----------------------------------------------------------------------------------------------------
# control panel
#----------------------------------------------------------------------------------------------------
dir_script = "Systematics/test/runWS/scripts"
#dir_script = "/afs/cern.ch/work/y/ykao/public/VLQ_UL_samples/script/"

samples = ["ttjets"] # standalone submission
samples = ["nrb"] # standalone submission
samples = ["data", "sig", "smh", "nrb"]

# ultraLegecy ttJets
dir_json = "Systematics/test/samples/UltraLegacy"
template_exe = sm.template_ul
template_run = sm.template_run_ttjets
dict_cmdLine = sm.dict_cmdLine_ul
dict_samples = sm.ul_samples
tag_script = ""
tag_json = "UL"

# ultraLegecy
dir_json = "Systematics/test/samples/UltraLegacy"
template_exe = sm.template_ul
template_run = sm.template_run_all_ul
dict_cmdLine = sm.dict_cmdLine_ul
dict_samples = sm.ul_samples
tag_script = ""
tag_json = "UL"

# ReReco
dir_json = "Systematics/test/samples/ReReco"
template_exe = sm.template_rr
template_run = sm.template_run_all_rereco
dict_cmdLine = sm.dict_cmdLine_rr
dict_samples = sm.rr_samples
tag_script = "_rereco"
tag_json = "RR"

# create scripts {{{
def create(fout, template, sample, year, json=""):
    output = template.format(SAMPLE=sample, YEAR=year)
    with open(fout, 'w') as f: f.write(output)

def create_scripts(year):
    for sample in samples:
        create('%s/exe%s_%s_%d.sh' % (dir_script, tag_script, sample, year), template_exe, sample, year)
        create('%s/run%s_%s_%d.sh' % (dir_script, tag_script, sample, year), template_run, sample, year)
#}}}
# create jsons {{{
def make_json(fout, samples, cmdLine):
    d = {}
    d["processes"] = samples
    d["cmdLine"] = cmdLine
    #print d
    with open(fout, 'w') as f:
        json.dump(d, f, sort_keys=True, indent=4)
        f.write('\n')

def create_jsons(year):
    for sample in samples:
        make_json("%s/%s_runII_%s_%d.json" % (dir_json, tag_json, sample, year), dict_samples[year][sample], dict_cmdLine[year][sample])
#}}}
# function for double check{{{
def load_xsec_json():
    global data_xsec
    with open("MetaData/data/cross_sections.json", 'r') as f: data_xsec = json.load(f)
    for key in data_xsec.keys():
        continue
        print key

def print_sample(samples):
    global data_xsec
    database = data_xsec.keys()
    for key, list_processes in samples.items():
        for process in list_processes:
            stem = process.split('/')[1]
            if not stem in database:
                print "[Error]", stem, " does not exist!"

def check_xsec(year):
    print ">>> check xsec for UL sample", year
    for sample in samples:
        if sample == "data": continue
        print_sample( dict_samples[year][sample] )
#}}}
if __name__ == "__main__":
    if args.e:
        subprocess.call("mkdir -p %s" % dir_script, shell=True)
        subprocess.call("mkdir -p %s" % dir_json, shell=True)

        create_scripts(2018)
        create_scripts(2017)
        create_scripts(2016)

        create_jsons(2018)
        create_jsons(2017)
        create_jsons(2016)

        print ">>>", dir_script
        subprocess.call("chmod +x %s/*" % dir_script, shell=True)
        subprocess.call("ls -lhrt %s" % dir_script, shell=True)

        print ">>>", dir_json
        subprocess.call("ls -lhrt %s" % dir_json, shell=True)

    else:
        load_xsec_json()
        check_xsec(2016)
        check_xsec(2017)
        check_xsec(2018)

    print ">>> finished!"
