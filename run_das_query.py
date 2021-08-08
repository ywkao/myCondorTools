#!/usr/bin/env python
import subprocess
import json
import argparse #{{{
parser = argparse.ArgumentParser()
parser.add_argument("-d", help = "Look for data events and dowload microAODs"  , action="store_true")
parser.add_argument("-q", help = "General das query"  , action="store_true")
parser.add_argument("-c", help = "Convert to flashgg format"  , action="store_true")
args = parser.parse_args()
#}}}

log = "mycheck_gjets.json"
myfile = "datasets_998.json"
output = myfile
datasets = [ #{{{
    "/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER"
] #}}}

def make_datasets(era): #{{{
    global datasets
    list_microAOD = []
    with open("list_microAOD.txt", 'r') as fin:
        for line in fin.readlines():
            if '#' in line or not 'USER' in line or not era in line:
                continue
            list_microAOD.append( line.strip() )
    datasets = list_microAOD

# 2016: 100To200
# 2017: 200To400
# 2018: 400To600
#}}}
def read(): #{{{
    f = open("example_gjets.json", 'r')
    data = json.load(f)
    for sample in data:
        if not sample == "/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER":
            continue

        tot = 0
        for ele in data[sample]["files"]:
            tot += ele["nevents"]
            is_the_same = ele["nevents"] == ele["totEvents"] and ele["totEvents"] == int(ele["weights"])
            if not is_the_same:
                print ">>> not the same: ", ele["nevents"], ele["totEvents"], ele["weights"]
        print ">>> check: tot = ", tot
    f.close()
#}}}
def search(dataset): #{{{
    subprocess.call('dasgoclient --query="file dataset=%s instance=prod/phys03" -json 2>&1 > %s' % (dataset, log), shell=True)
    #subprocess.call('vim %s' % log, shell=True)
    #subprocess.call('dasgoclient --query="summary dataset=%s instance=prod/phys03"' % (dataset), shell=True)
#}}}
def write(fout, name, nevents, is_the_last_one = False): #{{{
    fout.write( '            {\n')
    fout.write( '                \"bad\": false, \n')
    fout.write( '                \"events\": %d, \n' % nevents)
    fout.write( '                \"name\": \"%s\", \n' % name)
    fout.write( '                \"nevents\": %d, \n' % nevents)
    fout.write( '                \"totEvents\": %d, \n' % nevents)
    fout.write( '                \"weights\": %.1f\n' % nevents)

    if is_the_last_one:
        fout.write( '            }\n')
    else:
        fout.write( '            }, \n')
#}}}
def convert(dataset, is_the_last_one = False): #{{{
    fout = open(output, 'a')
    f = open(log, 'r')
    data = json.load(f)

    # opening 
    fout.write( '    \"%s\": {\n' % dataset)
    fout.write( '        \"dset_type\": \"mc\", \n')
    fout.write( '        \"files\": [\n')

    # files
    tot = 0
    counter = 0
    for rootfile in data:
        counter += 1
        for ele in rootfile["file"]:
            name = ele["name"]
            nevents = ele["nevents"]
            tot += ele["nevents"]

            if counter == len(data):
                write(fout, name, nevents, True)
            else:
                write(fout, name, nevents)

    print ">>> # of root files = ", len(data)
    print ">>> check: tot events = ", tot

    # ending
    fout.write( '        ], \n')
    fout.write( '        \"parent_n_units\": %d, \n' % tot)
    fout.write( '        \"vetted\": true\n')

    if is_the_last_one:
        fout.write( '    } \n')
        fout.write( '}')
    else:
        fout.write( '    }, \n\n')

    f.close()
    fout.close()
#}}}
def create_json_files(): #{{{
    global log, output
    eras = ["Era2016", "UL2017", "Era2018"] # gjet has UL
    eras = ["Era2016", "Era2017", "Era2018"]
    d = { "Era2016" : "Era2016_RR-17Jul2018_v3", "Era2017" : "Era2017_RR-31Mar2018_v3", "Era2018" : "Era2018_RR-17Sep2018_v3", "UL2017" : "Era2017_RR-31Mar2018_v3"}
    
    for era in eras:
        # init output file
        path = "/afs/cern.ch/work/y/ykao/ntuple_production_v7/CMSSW_10_6_8/src/flashgg/MetaData/data"
        directory = path + "/" + d[era]
        subprocess.call("mkdir -p %s" % directory, shell=True)
        output = directory + "/" + myfile

        # create json file
        make_datasets(era)
        if len(datasets) > 0: 
            print ">>> write to ", output
            with open(output, 'w') as f:
                f.write("{\n")
    
            idx = 0
            for dataset in datasets:
                print dataset
                log = "mycheck_%d.json" % idx
                search(dataset)
                if idx+1 == len(datasets):
                    convert(dataset, True)
                else:
                    convert(dataset)
                idx += 1
    
            # check
            subprocess.call("vim %s" % output, shell=True)
#}}}

if __name__ == "__main__":
    if args.d:
        read()

    if args.c:
        create_json_files()

    if args.q:
        #search(datasets[0])
        subprocess.call('dasgoclient --query="dataset=/QCD*DoubleEM*/*/USER instance=prod/phys03"', shell=True)
        #subprocess.call('dasgoclient --query="dataset=/GJets_HT*madgraphMLM*/spigazzi*/USER instance=prod/phys03"', shell=True)
        #subprocess.call('dasgoclient --query="dataset=/GJets_HT*madgraphMLM*/alesauva*/USER instance=prod/phys03"', shell=True)
        #subprocess.call('dasgoclient --query="file dataset=/GJets_HT*madgraphMLM*/spigazzi*Era2016*/USER instance=prod/phys03"', shell=True)
        #subprocess.call('dasgoclient --query="dataset=/GJets_HT*/*Era201*/USER instance=prod/phys03"', shell=True)

    print ">>> finished!"
