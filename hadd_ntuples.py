#!/usr/bin/env python2
import os
import subprocess
import glob
import parallel_utils

path = os.getcwd()

more_messages = True
more_messages = False

execution = False
execution = True

#----------------------------------------------------------------------------------------------------#
# v3p5: after including masses in ntuples during consistency check
#----------------------------------------------------------------------------------------------------#
global_version = "v3.5"
target_directory = "/eos/user/y/ykao/tPrimeExcessHgg/rootfiles/ntuples_%s/" % global_version

destinations = {
    '2016' : 'ntuples_v3p5p1_2016',
    '2017' : 'ntuples_v3p5p1_2017',
    '2018' : 'ntuples_v3p5p1_2018',
}

dirs = [
    "ntuples_data_2016",
    "ntuples_data_2017",
    "ntuples_data_2018",
    "ntuples_gamma_2016",
    "ntuples_gamma_2017",
    "ntuples_gamma_2018",
    "ntuples_qcdGjet_2016",
    "ntuples_qcdGjet_2017",
    "ntuples_qcdGjet_2018",
    "ntuples_signal_2016",
    "ntuples_signal_2017",
    "ntuples_signal_2018",
    "ntuples_smh_2016",
    "ntuples_smh_2017",
    "ntuples_smh_2018",
    "ntuples_ttX_2016",
    "ntuples_ttX_2017",
    "ntuples_ttX_2018",
]

#----------------------------------------------------------------------------------------------------#
# low level auxiliary functions
#----------------------------------------------------------------------------------------------------#
def make_command(samples, output):
    good_histos = []
    for hist in samples:
      size = os.stat(hist).st_size * (1./(1024))
      if size >= 16.:
        good_histos.append(hist)
        print("good hist: %s, size (kb): %d" % (hist, os.stat(hist).st_size * (1./(1024))))
      else:
        print("bad  hist: %s, size (kb): %d" % (hist, os.stat(hist).st_size * (1./(1024))))
    
    target = ""
    for hist in good_histos:
      target += "%s " % hist

    command = '/usr/bin/ionice -c2 -n7 hadd -f -k -j 4 %s %s' % (output, target)
    return command

def produce_commands(samples, output_dir):
    commands = []
    copy = samples
    counter = 1 
    while len(copy) > 10:
        output = output_dir + "/" + "merged_ntuple_" + str(counter) + ".root"
        command = make_command(copy[:10], output)
        commands.append(command)
        copy = copy[10:]
        counter += 1

    output = output_dir + "/" + "merged_ntuple_" + str(counter) + ".root"
    command = make_command(copy, output)
    commands.append(command)
    return commands

#----------------------------------------------------------------------------------------------------#
# high level functions for mergin ntuples
#----------------------------------------------------------------------------------------------------#
def merge_ntuples_1st():
    print "\n>>> start 1st run of merging\n"

    global path
    commands = []
    for directory in dirs:
        year = directory.split("_")[-1]
        destination = "merged_ntuples/" + destinations[year]
        os.chdir( directory )
        ntuples = glob.glob("*.root")
        #ntuples = glob.glob("*TTJets*.root") # merge specific sample
    
        print "[Info] " + directory + " >>> " + destination
    
        # look for ntuples with individual size greater than 16 KB (non-empty)
        # hint: output_TprimeBToTH_Hgg_M-1100_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8_lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72_USER_14.root
        samples = []
        for ntuple in ntuples:
            size = os.stat(ntuple).st_size * (1./1024.)
            sample_name = ntuple.split("_USER_")[0]
            if size > 16:
                samples.append(sample_name)
            if not execution and more_messages:
                print '%4d KB %s' % ( int(size), ntuple )
    
        # merge root files according to unique sample name
        # hint: output_TprimeBToTH_Hgg_M-1100_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8_lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-TRAILING
        os.chdir(path)
        samples_uniq = list(set(samples))
        for sample in samples_uniq:
            stem = sample.split("-Run")[0]
            era = sample.split("-Run")[1].split("-")[0]
            sample_name = destination + "/" + stem + "-Run" + era
            output_dir = sample_name.replace("output", "merged_ntuple")
    
            if not execution:
                print output_dir
            else:
                subprocess.call("mkdir -p %s" % output_dir, shell=True)
                related_ntuples = glob.glob( directory + "/%s*" % sample )
                tokens = produce_commands(related_ntuples, output_dir)
                for command in tokens:
                    commands.append(command)
    
    if execution:
        parallel_utils.submit_jobs(commands, 10)

#----------------------------------------------------------------------------------------------------#
# 2nd stage of hadd
#----------------------------------------------------------------------------------------------------#

years = ["2016", "2017", "2018"]
    
mysamples = {
        "_bbHToGG"               : "bbH",
        "_VHToGG"                : "VHToGG",
        "_GluGluHToGG"           : "GluGluHToGG",
        "_VBFHToGG"              : "VBF",
        "_THQ"                   : "THQ",
        "_ttHJet"                : "ttHJet",
        "_DiPhotonJets"          : "DiPhotonJets",
        "_DoubleEG"              : "Data",
        "_EGamma"                : "Data",
        "_GJet_Pt"               : "GJet_Pt",
        "_QCD_Pt"                : "QCD",
        "_ST_tW"                 : "ST_tW",
        "_TTGG"                  : "TTGG",
        "_TGJets"                : "TGJets",
        "_TTGJet"                : "TTGJets",
        "_TTJets"                : "TTJets",
        "_WG"                    : "WG",
        "_WW"                    : "WW",
        "_WZ"                    : "WZ",
        "_ZG"                    : "ZG",
        "_ZZ"                    : "ZZ",
        "_ZNuNuGJets"            : "ZNuNuGJets",
        "TprimeBToTH_Hgg_M-600"  : "TprimeBToTH_M-600",
        "TprimeBToTH_Hgg_M-625"  : "TprimeBToTH_M-625",
        "TprimeBToTH_Hgg_M-650"  : "TprimeBToTH_M-650",
        "TprimeBToTH_Hgg_M-675"  : "TprimeBToTH_M-675",
        "TprimeBToTH_Hgg_M-700"  : "TprimeBToTH_M-700",
        "TprimeBToTH_Hgg_M-800"  : "TprimeBToTH_M-800",
        "TprimeBToTH_Hgg_M-900"  : "TprimeBToTH_M-900",
        "TprimeBToTH_Hgg_M-1000" : "TprimeBToTH_M-1000",
        "TprimeBToTH_Hgg_M-1100" : "TprimeBToTH_M-1100",
        "TprimeBToTH_Hgg_M-1200" : "TprimeBToTH_M-1200",
}

def convert_list_to_str(base, mylist):
    output = ""
    counter = 0
    for element in mylist:
        if counter == 0:
            output = base + element
        else:
            output = output + " " + base + element
        counter += 1
    return output

#----------------------------------------------------------------------------------------------------#

def merge_ntuples_2nd():
    print "\n>>> start 2nd run of merging\n"

    global path
    global target_directory
    version_stamp = global_version.split('.')[0] + 'p' + global_version.split('.')[1]
    command_list = []

    for year in years:
        source_directory = "merged_ntuples/" + destinations[year]

        os.chdir( path )
        os.chdir( source_directory )
        sub_directories = glob.glob("merged*")
        #sub_directories = glob.glob("merged*TTJets*2017*")
        counter = 0
        for sub in sub_directories:
            os.chdir( sub )
            rootfiles_raw = glob.glob("*root")
            base = path +  "/" + source_directory + "/" + sub + "/"

            #----------------------------------------------------------------------------------------------------
            # Remove empty root files
            #----------------------------------------------------------------------------------------------------
            rootfiles = []
            for ntuple in rootfiles_raw:
                size = os.stat(ntuple).st_size * (1./1024.)
                if size > 2:
                    rootfiles.append(ntuple)
            #----------------------------------------------------------------------------------------------------
            # Bypass samples that have been 2nd merged
            #----------------------------------------------------------------------------------------------------
            hasBeenMerged = ("TprimeBToTH_Hgg" in sub) or ("ttHJetToGG" in sub) or ("TT" in sub) or ("TG" in sub) or ("DiPhoton" in sub)
            hasBeenMerged = ("DoubleEG" in sub) or ("EGamma" in sub)
            hasBeenMerged = False
            if hasBeenMerged:
                os.chdir("../")
                continue
            #----------------------------------------------------------------------------------------------------
            # Embark on the 2nd merge of produced ntuples
            #----------------------------------------------------------------------------------------------------
            else:
                print ">>>>> ", sub
                # example 1: merged_ntuple_QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8_spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD
                # example 2: merged_ntuple_TprimeBToTH_Hgg_M-625_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8_lata-Era2018_RR-17Sep2018_v2-v2_p12-v0-RunIIAutumn18MiniAOD
                has_permission = False
                for key in mysamples.keys():
                    if key in sub:
                        stamp = mysamples[key]
                        if stamp != "Data":
                            my_rootfile_name = stamp + "_Era" + year + "_%s_%d.root" % (version_stamp, counter)
                        else:
                            # example: merged_ntuple_DoubleEG_spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017C
                            data_year_stamp = sub.split('-')[5].split('un')[1]
                            my_rootfile_name = stamp + "_Era" + data_year_stamp + "_%s.root" % version_stamp

                        has_permission = True
                        print my_rootfile_name

                if has_permission:
                    target = target_directory + my_rootfile_name
                    command = "hadd %s %s" % (target, convert_list_to_str(base, rootfiles))
                    command_list.append(command)

                    if not execution:
                        print command
                else:
                    print "[ERROR] missing key for the sample: ", sub

                os.chdir("../")

            counter += 1
    
    if execution:
        subprocess.call("mkdir -p %s" % target_directory, shell=True)
        #parallel_utils.submit_jobs(command_list, 10)

        for command in command_list:
            print ">>>>> start to run: ", command
            parallel_utils.run(command)

#----------------------------------------------------------------------------------------------------#

def merge_ntuples_3rd():
    global target_directory
    os.chdir( target_directory )
    rootfiles = glob.glob("*root")

    command_list = []
    collection = {"Data" : {}, "DiPhotonJets" : {}, "GJet_Pt" : {}, "QCD" : {}}
    #Data_Era2016B_v3p5.root
    #DiPhotonJets_Era2016_v3p5_0.root
    #GJet_Pt_Era2018_v3p5_9.root
    #QCD_Era2016_v3p5_13.root

    for rootfile in rootfiles:
        need_to_merge = False
        for key in collection.keys():
            if key in rootfile:
                need_to_merge = True

                # extract year info
                year = ''
                if key == "Data":
                    tag = rootfile.split('Era')[1].split('_')[0]
                    if '2016' in tag:
                        year = '2016'
                    elif '2017' in tag:
                        year = '2017'
                    elif '2018' in tag:
                        year = '2018'
                    else:
                        print "[Error] something is not right for the rootfile: ", rootfile
                        break
                else:
                    year = rootfile.split('Era')[1].split('_')[0]

                # store the rootfile in collection
                if year in collection[key]:
                    collection[key][year].append(rootfile)
                else:
                    collection[key][year] = []
                    collection[key][year].append(rootfile)

        if not need_to_merge:
            new_name = ""
            reduced_elements = rootfile.split('_')[:-1]
            for ele in reduced_elements:
                if new_name == "":
                    new_name = ele
                else:
                    new_name = new_name + "_" + ele
            new_name += ".root"

            command = "mv %s %s" % (rootfile, new_name)
            command_list.append(command)

    for sample in collection.keys():
        for year in collection[sample].keys():
            target = sample + "_Era" + year + ".root" 

            rootfiles_src = ""
            for root in collection[sample][year]:
                rootfiles_src += "%s " % root

            command = "hadd %s %s" % (target, rootfiles_src)
            command_list.append(command)

    if not execution:
        for command in command_list:
            print command

    if execution:
        parallel_utils.submit_jobs(command_list, 10)


if __name__ == "__main__":
    #merge_ntuples_1st()
    #merge_ntuples_2nd()
    merge_ntuples_3rd()

    print "\n>>> Good, this is the end! ;)"
