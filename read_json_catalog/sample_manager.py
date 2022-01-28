#/usr/bin/env python

template_ul = '''#!/bin/bash
time ./scripts/run_{SAMPLE}_{YEAR}.sh &
''' #time ./script/run_{SAMPLE}_{YEAR}.sh 2>&1 | tee log_{SAMPLE}_{YEAR}.txt &

template_rr = '''#!/bin/bash
time ./scripts/run_rereco_{SAMPLE}_{YEAR}.sh &
'''

template_run_all_rereco = '''cwd=`pwd`
outdir="${{cwd}}/../output_{SAMPLE}_{YEAR}"
mkdir -p ${{outdir}}
fggRunJobs.py --load $CMSSW_BASE/src/flashgg/Systematics/test/samples/ReReco/RR_runII_{SAMPLE}_{YEAR}.json \\
        -d dir_{SAMPLE}_{YEAR} \\
              -n 50 \\
              -q tomorrow \\
              --no-use-tarball --no-copy-proxy \\
              --stage-to ${{outdir}} \\
              -x cmsRun ../workspaceStd_ntuple.py maxEvents=-1 \\
                                                  doSystematics=false \\
                                                  dumpTrees=true \\
                                                  dumpWorkspace=false
#copyInputMicroAOD=1
'''

template_run_all_ul = '''cwd=`pwd`
outdir="${{cwd}}/../output_{SAMPLE}_{YEAR}"
mkdir -p ${{outdir}}
fggRunJobs.py --load $CMSSW_BASE/src/flashgg/Systematics/test/samples/UltraLegacy/UL_runII_{SAMPLE}_{YEAR}.json \\
        -d dir_{SAMPLE}_{YEAR} \\
              -n 50 \\
              -q tomorrow \\
              --no-use-tarball --no-copy-proxy \\
              --stage-to ${{outdir}} \\
              -x cmsRun ../workspaceStd_ntuple.py maxEvents=-1 \\
                                                  doSystematics=false \\
                                                  dumpTrees=true \\
                                                  dumpWorkspace=false
#copyInputMicroAOD=1
'''

template_run_ttjets = '''cwd=`pwd`
outdir="${{cwd}}/../output_{SAMPLE}_{YEAR}"
mkdir -p ${{outdir}}
fggRunJobs.py --load $CMSSW_BASE/src/flashgg/Systematics/test/samples/UltraLegacy/UL_runII_{SAMPLE}_{YEAR}.json \\
        -d dir_{SAMPLE}_{YEAR} \\
              -n 800 \\
              -q testmatch \\
              --no-use-tarball --no-copy-proxy \\
              --stage-to ${{outdir}} \\
              -x cmsRun ../workspaceStd_ntuple.py maxEvents=-1 \\
                                                  doSystematics=false \\
                                                  dumpTrees=true \\
                                                  dumpWorkspace=false
#copyInputMicroAOD=1
'''

# cmdLine {{{
dict_cmdLine_2016 = {
    "RR16_data"  : "campaign=Era2016_RR-17Jul2018_v2 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2016_RR-17Jul2018_v1.json useAAA=True lumiMask=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt",
    "RR16_MC"  : "campaign=Era2016_RR-17Jul2018_v2 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2016_RR-17Jul2018_v1.json puTarget=6.557e-06,2.331e-05,6.347e-05,8.636e-05,0.0001235,0.0001654,0.0001932,0.0003625,0.0009901,0.002212,0.004983,0.0101,0.01683,0.0244,0.03264,0.0413,0.04865,0.05362,0.05642,0.0578,0.05863,0.05902,0.05837,0.05647,0.05367,0.0503,0.04647,0.04234,0.03807,0.03378,0.02953,0.02537,0.02139,0.0177,0.01437,0.01146,0.008964,0.006874,0.00515,0.003754,0.002652,0.001808,0.001186,0.0007463,0.0004497,0.0002591,0.0001426,7.497e-05,3.763e-05,1.806e-05,8.323e-06,3.713e-06,1.638e-06,7.458e-07,3.784e-07,2.312e-07,1.721e-07,1.463e-07,1.325e-07,1.227e-07,1.142e-07,1.06e-07,9.787e-08,8.98e-08,8.184e-08,7.409e-08,6.661e-08,5.949e-08,5.276e-08,4.648e-08,4.066e-08,3.533e-08,3.049e-08,2.614e-08,2.225e-08",
    "RR16_MC_v3"  : "campaign=Era2016_RR-17Jul2018_v3 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2016_RR-17Jul2018_v1.json puTarget=6.557e-06,2.331e-05,6.347e-05,8.636e-05,0.0001235,0.0001654,0.0001932,0.0003625,0.0009901,0.002212,0.004983,0.0101,0.01683,0.0244,0.03264,0.0413,0.04865,0.05362,0.05642,0.0578,0.05863,0.05902,0.05837,0.05647,0.05367,0.0503,0.04647,0.04234,0.03807,0.03378,0.02953,0.02537,0.02139,0.0177,0.01437,0.01146,0.008964,0.006874,0.00515,0.003754,0.002652,0.001808,0.001186,0.0007463,0.0004497,0.0002591,0.0001426,7.497e-05,3.763e-05,1.806e-05,8.323e-06,3.713e-06,1.638e-06,7.458e-07,3.784e-07,2.312e-07,1.721e-07,1.463e-07,1.325e-07,1.227e-07,1.142e-07,1.06e-07,9.787e-08,8.98e-08,8.184e-08,7.409e-08,6.661e-08,5.949e-08,5.276e-08,4.648e-08,4.066e-08,3.533e-08,3.049e-08,2.614e-08,2.225e-08",
}

dict_cmdLine_2017 = {
    "UL17_data" : "campaign=Era2017_legacy_v1 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2017_legacy_v1.json useAAA=True lumiMask=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
    "UL17_MC" : "campaign=Era2017_legacy_v1 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2017_legacy_v1.json useAAA=True puTarget=6.238e-06,2.614e-05,4.849e-05,9.107e-05,9.776e-05,0.0001416,0.0001553,0.0001637,0.0002213,0.0005245,0.001052,0.001992,0.00317,0.004549,0.006438,0.009079,0.01267,0.01687,0.02103,0.02487,0.02824,0.03097,0.03307,0.03469,0.03608,0.03739,0.03851,0.0392,0.03932,0.03881,0.03775,0.03623,0.03435,0.03215,0.02974,0.0273,0.02494,0.02277,0.02082,0.01917,0.01791,0.01711,0.01682,0.01702,0.01759,0.01836,0.01906,0.01941,0.01917,0.01821,0.01654,0.01433,0.01184,0.009335,0.007048,0.005114,0.003583,0.002435,0.001613,0.001047,0.0006682,0.0004212,0.0002632,0.0001635,0.0001014,6.299e-05,3.93e-05,2.471e-05,1.568e-05,1.006e-05,6.53e-06,4.28e-06,2.83e-06,1.883e-06,1.259e-06,8.436e-07,5.655e-07,3.787e-07,2.53e-07,1.684e-07,1.116e-07,7.359e-08,4.825e-08,3.143e-08,2.033e-08,1.306e-08,8.322e-09,5.261e-09,3.297e-09,2.049e-09,1.262e-09,7.697e-10,4.652e-10,2.785e-10,1.651e-10,9.691e-11,5.632e-11,3.24e-11,1.845e-11 targetLumi=1e+3 processType='mc'",

    "RR17_data"  : "campaign=Era2017_RR-31Mar2018_v2 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2017_RR-31Mar2018_v1.json useAAA=True lumiMask=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt",
    "RR17_MC"  : "campaign=Era2017_RR-31Mar2018_v2 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2017_RR-31Mar2018_v1.json puTarget=6.245e-06,2.63e-05,4.92e-05,9.084e-05,9.854e-05,0.0001426,0.0001557,0.0001656,0.0002269,0.0005395,0.001076,0.002034,0.003219,0.004616,0.006528,0.009201,0.01283,0.01707,0.02125,0.0251,0.02847,0.03118,0.03325,0.03486,0.03626,0.03758,0.0387,0.03937,0.03946,0.03892,0.03782,0.03627,0.03435,0.03211,0.02967,0.02719,0.02482,0.02264,0.0207,0.01907,0.01784,0.01709,0.01685,0.0171,0.01771,0.01849,0.01916,0.01945,0.01911,0.01804,0.01627,0.01399,0.01147,0.008976,0.006728,0.004848,0.003375,0.002281,0.001504,0.0009715,0.0006178,0.0003882,0.0002419,0.0001501,9.294e-05,5.768e-05,3.598e-05,2.263e-05,1.437e-05,9.233e-06,5.996e-06,3.933e-06,2.601e-06,1.731e-06,1.157e-06,7.743e-07,5.184e-07,3.466e-07,2.311e-07,1.535e-07,1.015e-07,6.676e-08,4.365e-08,2.836e-08,1.829e-08,1.171e-08,7.437e-09,4.685e-09,2.926e-09,1.812e-09,1.111e-09,6.754e-10,4.066e-10,2.424e-10,1.431e-10,8.363e-11,4.839e-11,2.771e-11,1.571e-11,8.814e-12",
    "RR17_MC_v3"  : "campaign=Era2017_RR-31Mar2018_v3 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2017_RR-31Mar2018_v1.json puTarget=6.245e-06,2.63e-05,4.92e-05,9.084e-05,9.854e-05,0.0001426,0.0001557,0.0001656,0.0002269,0.0005395,0.001076,0.002034,0.003219,0.004616,0.006528,0.009201,0.01283,0.01707,0.02125,0.0251,0.02847,0.03118,0.03325,0.03486,0.03626,0.03758,0.0387,0.03937,0.03946,0.03892,0.03782,0.03627,0.03435,0.03211,0.02967,0.02719,0.02482,0.02264,0.0207,0.01907,0.01784,0.01709,0.01685,0.0171,0.01771,0.01849,0.01916,0.01945,0.01911,0.01804,0.01627,0.01399,0.01147,0.008976,0.006728,0.004848,0.003375,0.002281,0.001504,0.0009715,0.0006178,0.0003882,0.0002419,0.0001501,9.294e-05,5.768e-05,3.598e-05,2.263e-05,1.437e-05,9.233e-06,5.996e-06,3.933e-06,2.601e-06,1.731e-06,1.157e-06,7.743e-07,5.184e-07,3.466e-07,2.311e-07,1.535e-07,1.015e-07,6.676e-08,4.365e-08,2.836e-08,1.829e-08,1.171e-08,7.437e-09,4.685e-09,2.926e-09,1.812e-09,1.111e-09,6.754e-10,4.066e-10,2.424e-10,1.431e-10,8.363e-11,4.839e-11,2.771e-11,1.571e-11,8.814e-12",

    
}

dict_cmdLine_2018 = {
    "UL18_data"  : "campaign=Era2018_legacy_v1 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2018_legacy_v1.json useAAA=True lumiMask=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
    "UL18_MC" : "campaign=Era2018_legacy_v1 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2018_legacy_v1.json useAAA=True puTarget=4.548e-06,1.601e-05,5.089e-05,0.0001143,0.0002035,0.0003172,0.0004688,0.0006826,0.0009665,0.001345,0.001884,0.002648,0.003691,0.00505,0.006756,0.00884,0.01132,0.01416,0.01729,0.02053,0.02367,0.02651,0.02888,0.03076,0.03222,0.03338,0.03438,0.0353,0.03619,0.03705,0.03787,0.03859,0.03918,0.03956,0.03969,0.0395,0.03893,0.03792,0.03643,0.03445,0.03201,0.02919,0.02608,0.02281,0.01953,0.01636,0.0134,0.01075,0.008451,0.006517,0.004938,0.003683,0.00271,0.001971,0.00142,0.001015,0.0007202,0.000508,0.0003561,0.000248,0.0001714,0.0001175,7.979e-05,5.36e-05,3.56e-05,2.337e-05,1.515e-05,9.699e-06,6.136e-06,3.836e-06,2.371e-06,1.45e-06,8.777e-07,5.259e-07,3.121e-07,1.834e-07,1.067e-07,6.145e-08,3.501e-08,1.973e-08,1.099e-08,6.041e-09,3.278e-09,1.755e-09,9.256e-10,4.811e-10,2.462e-10,1.24e-10,6.147e-11,2.996e-11,1.436e-11,6.767e-12,3.134e-12,1.426e-12,6.376e-13,2.801e-13,1.209e-13,5.13e-14,2.142e-14 targetLumi=1e+3 processType='mc'",

    "RR18_data"  : "campaign=Era2018_RR-17Sep2018_v2 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2018_RR-17Sep2018_v1.json useAAA=True lumiMask=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt",
    "RR18_MC"  : "campaign=Era2018_RR-17Sep2018_v2 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2018_RR-17Sep2018_v1.json puTarget=1.105e-07,3.485e-06,2e-05,5.011e-05,8.593e-05,0.0001214,0.0001645,0.0002381,0.0003153,0.0004159,0.0006128,0.0009682,0.00154,0.002407,0.003656,0.005369,0.007596,0.01032,0.01345,0.0168,0.02011,0.02316,0.02579,0.02799,0.02987,0.03155,0.03314,0.03465,0.03608,0.03738,0.03851,0.03944,0.04016,0.04064,0.04085,0.04078,0.04035,0.03953,0.03828,0.03657,0.03442,0.03187,0.02899,0.0259,0.0227,0.01951,0.01645,0.01361,0.01106,0.008825,0.006927,0.005355,0.004082,0.003073,0.002289,0.001688,0.001234,0.0008952,0.0006447,0.0004608,0.0003269,0.00023,0.0001603,0.0001107,7.561e-05,5.108e-05,3.412e-05,2.253e-05,1.47e-05,9.484e-06,6.051e-06,3.819e-06,2.386e-06,1.475e-06,9.035e-07,5.48e-07,3.292e-07,1.958e-07,1.153e-07,6.722e-08,3.876e-08,2.21e-08,1.245e-08,6.927e-09,3.805e-09,2.062e-09,1.102e-09,5.807e-10,3.015e-10,1.542e-10,7.765e-11,3.85e-11,1.879e-11,9.023e-12,4.263e-12,1.981e-12,9.058e-13,4.072e-13,1.8e-13,7.823e-14",
    "RR18_MC_v3"  : "campaign=Era2018_RR-17Sep2018_v3 metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2018_RR-17Sep2018_v1.json puTarget=1.105e-07,3.485e-06,2e-05,5.011e-05,8.593e-05,0.0001214,0.0001645,0.0002381,0.0003153,0.0004159,0.0006128,0.0009682,0.00154,0.002407,0.003656,0.005369,0.007596,0.01032,0.01345,0.0168,0.02011,0.02316,0.02579,0.02799,0.02987,0.03155,0.03314,0.03465,0.03608,0.03738,0.03851,0.03944,0.04016,0.04064,0.04085,0.04078,0.04035,0.03953,0.03828,0.03657,0.03442,0.03187,0.02899,0.0259,0.0227,0.01951,0.01645,0.01361,0.01106,0.008825,0.006927,0.005355,0.004082,0.003073,0.002289,0.001688,0.001234,0.0008952,0.0006447,0.0004608,0.0003269,0.00023,0.0001603,0.0001107,7.561e-05,5.108e-05,3.412e-05,2.253e-05,1.47e-05,9.484e-06,6.051e-06,3.819e-06,2.386e-06,1.475e-06,9.035e-07,5.48e-07,3.292e-07,1.958e-07,1.153e-07,6.722e-08,3.876e-08,2.21e-08,1.245e-08,6.927e-09,3.805e-09,2.062e-09,1.102e-09,5.807e-10,3.015e-10,1.542e-10,7.765e-11,3.85e-11,1.879e-11,9.023e-12,4.263e-12,1.981e-12,9.058e-13,4.072e-13,1.8e-13,7.823e-14",
}

dict_cmdLine_ul = {
    2016 : {
        "data" : dict_cmdLine_2016["RR16_data"],
        "sig"  : dict_cmdLine_2016["RR16_MC_v3"],
        "smh"  : dict_cmdLine_2016["RR16_MC"],
        "nrb"  : dict_cmdLine_2016["RR16_MC"],
    },

    2017 : {
        "data"   : dict_cmdLine_2017["UL17_data"],
        "sig"    : dict_cmdLine_2017["UL17_MC"],
        "smh"    : dict_cmdLine_2017["UL17_MC"],
        "nrb"    : dict_cmdLine_2017["UL17_MC"],
        "ttjets" : dict_cmdLine_2017["UL17_MC"],
    },

    2018 : {
        "data"   : dict_cmdLine_2018["UL18_data"],
        "sig"    : dict_cmdLine_2018["UL18_MC"],
        "smh"    : dict_cmdLine_2018["UL18_MC"],
        "nrb"    : dict_cmdLine_2018["UL18_MC"],
        "ttjets" : dict_cmdLine_2018["UL18_MC"],
    },
}

dict_cmdLine_rr = {
    2016 : {
        "data" : dict_cmdLine_2016["RR16_data"],
        "sig"  : dict_cmdLine_2016["RR16_MC_v3"],
        "smh"  : dict_cmdLine_2016["RR16_MC"],
        "nrb"  : dict_cmdLine_2016["RR16_MC"],
    },

    2017 : {
        "data"   : dict_cmdLine_2017["RR17_data"],
        "sig"    : dict_cmdLine_2017["RR17_MC_v3"],
        "smh"    : dict_cmdLine_2017["RR17_MC"],
        "nrb"    : dict_cmdLine_2017["RR17_MC"],
    },

    2018 : {
        "data"   : dict_cmdLine_2018["RR18_data"],
        "sig"    : dict_cmdLine_2018["RR18_MC_v3"],
        "smh"    : dict_cmdLine_2018["RR18_MC"],
        "nrb"    : dict_cmdLine_2018["RR18_MC"],
    },
}

#}}}

ul_samples_2017_full = { #{{{
    "data" : {
        "Data" : [
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017F-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017B-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017D-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017E-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017C-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
        ]
    },

    "sig" : {
        "TprimeM600_125"  : ["/TprimeBToTH_Hgg_M-600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM625_125"  : ["/TprimeBToTH_Hgg_M-625_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM650_125"  : ["/TprimeBToTH_Hgg_M-650_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM675_125"  : ["/TprimeBToTH_Hgg_M-675_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM700_125"  : ["/TprimeBToTH_Hgg_M-700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM800_125"  : ["/TprimeBToTH_Hgg_M-800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM900_125"  : ["/TprimeBToTH_Hgg_M-900_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM1000_125" : ["/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM1100_125" : ["/TprimeBToTH_Hgg_M-1100_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM1200_125" : ["/TprimeBToTH_Hgg_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        #"TprimeM1300_125" : ["/TprimeBToTH_Hgg_M-1300_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        #"TprimeM1400_125" : ["/TprimeBToTH_Hgg_M-1400_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        #"TprimeM1500_125" : ["/TprimeBToTH_Hgg_M-1500_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        #"TprimeM1600_125" : ["/TprimeBToTH_Hgg_M-1600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        #"TprimeM1700_125" : ["/TprimeBToTH_Hgg_M-1700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        #"TprimeM1800_125" : ["/TprimeBToTH_Hgg_M-1800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
    },

    "smh" : {
        "tth_125" : ["/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-40c8f5e3297812fbf727853bb545f6df/USER"],
        "thq_125" : ["/THQ_ctcvcp_HToGG_M125_TuneCP5_13TeV-madgraph-pythia8/alesauva-UL2017_3-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-00000000000000000000000000000000/USER"],
        "thw_125" : ["/THW_ctcvcp_HToGG_M125_TuneCP5_13TeV-madgraph-pythia8/alesauva-UL2017_3-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-9bdaeb58fc35885a7495aa2986b66870/USER"],
        "vh_125"  : ["/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/alesauva-UL2017_3-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-9bdaeb58fc35885a7495aa2986b66870/USER"],
        "ggh_125" : ["/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-f92679b6f67e90fd93c35b41b89480a0/USER"],
        "vbf_125" : ["/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8709e8b8d2daa2ed8fac18f6d4560942/USER"],
    },

    "nrb" : {
        "NRB" : [
            "/DiPhotonJetsBox2BJets_MGG-80toInf_13TeV-sherpa/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v3-b4ca3fbc0a606daa82bec910d90e7c99/USER",
            "/DiPhotonJetsBox_M40_80-sherpa/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v3-b4ca3fbc0a606daa82bec910d90e7c99/USER",
            "/DiPhotonJetsBox1BJet_MGG-80toInf_13TeV-sherpa/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v3-b4ca3fbc0a606daa82bec910d90e7c99/USER",
            "/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v3-b4ca3fbc0a606daa82bec910d90e7c99/USER",
            "/DiPhotonJets_MGG-80toInf_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",

            "/GJets_DoubleEMEnriched_PtG-20MGG-40To80_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJets_DoubleEMEnriched_PtG-40MGG-80_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJets_DoubleEMEnriched_PtG-20MGG-80_TuneCP5_13TeV-madgraphMLM-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-4cores5k_106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            
            "/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            
            "/TGJets_TuneCP5_13TeV-amcatnlo-madspin-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/TTGG_0Jets_TuneCP5_13TeV-amcatnlo-madspin-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            
            "/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            
            "/ZZ_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/WW_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/WZ_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/ZZ_TuneCP5_13TeV-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/WW_TuneCP5_13TeV-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/WZ_TuneCP5_13TeV-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
        ]
    },
} #}}}
ReReco_samples_2016 = { #{{{
    "data" : {
        "Data" : [
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016B-17Jul2018_ver2-v1-86023db6be00ee64cd62a3172358fb9f/USER",
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016C-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER",
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016D-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER",
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016E-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER",
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016F-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER",
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016G-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER",
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016H-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER",
        ]
    },

    "sig" : {
        "TprimeM600_125"  : ["/TprimeBToTH_Hgg_M-600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER"],
        "TprimeM625_125"  : ["/TprimeBToTH_Hgg_M-625_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER"],
        "TprimeM650_125"  : ["/TprimeBToTH_Hgg_M-650_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER"],
        "TprimeM675_125"  : ["/TprimeBToTH_Hgg_M-675_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER"],
        "TprimeM700_125"  : ["/TprimeBToTH_Hgg_M-700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER"],
        "TprimeM800_125"  : ["/TprimeBToTH_Hgg_M-800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER"],
        "TprimeM900_125"  : ["/TprimeBToTH_Hgg_M-900_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER"],
        "TprimeM1000_125" : ["/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER"],
        "TprimeM1100_125" : ["/TprimeBToTH_Hgg_M-1100_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER"],
        "TprimeM1200_125" : ["/TprimeBToTH_Hgg_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER"],
    },

    "smh" : {
        "tth_125" : ["/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8_v2/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-4b15415e8d56c44d7f20bde93a158c60/USER"],
        "thq_125" : ["/THQ_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCUETP8M1_v2/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-b8a5b6287120fce79bb02069cbed82a0/USER"],
        "vh_125"  : ["/VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-b8a5b6287120fce79bb02069cbed82a0/USER"],
        "ggh_125" : ["/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2-6512204af72ea57fbfefdf0db0649ffe/USER"],
        "vbf_125" : ["/VBFHToGG_M125_13TeV_amcatnlo_pythia8_v2/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-42666aea495bdc3a36d796ff9c4bc819/USER"],
    },

    "nrb" : {
        "NRB" : [
            #"/DiPhotonJetsBox_M40_80-Sherpa/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-735d6f5d6752834cf1de64ba6920599a/USER",
            "/DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",

            "/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/TTGG_0Jets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-735d6f5d6752834cf1de64ba6920599a/USER",
            "/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",

            "/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-c7e9dfda701ffa83862108b4f8303392/USER",
            "/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",

            "/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext3-v1-735d6f5d6752834cf1de64ba6920599a/USER",
            "/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1-735d6f5d6752834cf1de64ba6920599a/USER",
            "/WW_TuneCUETP8M1_13TeV-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/WZ_TuneCUETP8M1_13TeV-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/ZZ_TuneCUETP8M1_13TeV-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",
        ]
    },
} #}}}
ul_samples_2017 = { #{{{
    "data" : {
        "Data" : [
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017F-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017B-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017D-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017E-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017C-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
        ]
    },

    "sig" : {
        "TprimeM600_125"  : ["/TprimeBToTH_Hgg_M-600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM625_125"  : ["/TprimeBToTH_Hgg_M-625_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM650_125"  : ["/TprimeBToTH_Hgg_M-650_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM675_125"  : ["/TprimeBToTH_Hgg_M-675_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM700_125"  : ["/TprimeBToTH_Hgg_M-700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM800_125"  : ["/TprimeBToTH_Hgg_M-800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM900_125"  : ["/TprimeBToTH_Hgg_M-900_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM1000_125" : ["/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM1100_125" : ["/TprimeBToTH_Hgg_M-1100_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        "TprimeM1200_125" : ["/TprimeBToTH_Hgg_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        #"TprimeM1300_125" : ["/TprimeBToTH_Hgg_M-1300_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        #"TprimeM1400_125" : ["/TprimeBToTH_Hgg_M-1400_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        #"TprimeM1500_125" : ["/TprimeBToTH_Hgg_M-1500_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        #"TprimeM1600_125" : ["/TprimeBToTH_Hgg_M-1600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        #"TprimeM1700_125" : ["/TprimeBToTH_Hgg_M-1700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
        #"TprimeM1800_125" : ["/TprimeBToTH_Hgg_M-1800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER"],
    },

    "smh" : {
        "tth_125" : ["/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-40c8f5e3297812fbf727853bb545f6df/USER"],
        "thq_125" : ["/THQ_ctcvcp_HToGG_M125_TuneCP5_13TeV-madgraph-pythia8/alesauva-UL2017_3-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-00000000000000000000000000000000/USER"],
        "thw_125" : ["/THW_ctcvcp_HToGG_M125_TuneCP5_13TeV-madgraph-pythia8/alesauva-UL2017_3-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-9bdaeb58fc35885a7495aa2986b66870/USER"],
        "vh_125"  : ["/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/alesauva-UL2017_3-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-9bdaeb58fc35885a7495aa2986b66870/USER"],
        "ggh_125" : ["/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-f92679b6f67e90fd93c35b41b89480a0/USER"],
        "vbf_125" : ["/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8709e8b8d2daa2ed8fac18f6d4560942/USER"],
    },

    "nrb" : {
        "NRB" : [
            #"/DiPhotonJetsBox2BJets_MGG-80toInf_13TeV-sherpa/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v3-b4ca3fbc0a606daa82bec910d90e7c99/USER",
            #"/DiPhotonJetsBox_M40_80-sherpa/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v3-b4ca3fbc0a606daa82bec910d90e7c99/USER",
            #"/DiPhotonJetsBox1BJet_MGG-80toInf_13TeV-sherpa/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v3-b4ca3fbc0a606daa82bec910d90e7c99/USER",
            #"/DiPhotonJets_MGG-80toInf_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v3-b4ca3fbc0a606daa82bec910d90e7c99/USER",

            #"/GJets_DoubleEMEnriched_PtG-20MGG-40To80_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/GJets_DoubleEMEnriched_PtG-40MGG-80_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/GJets_DoubleEMEnriched_PtG-20MGG-80_TuneCP5_13TeV-madgraphMLM-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            #"/GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-4cores5k_106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            
            #"/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            
            #"/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/TGJets_TuneCP5_13TeV-amcatnlo-madspin-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/TTGG_0Jets_TuneCP5_13TeV-amcatnlo-madspin-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            
            #"/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/ZZ_TuneCP5_13TeV-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/WW_TuneCP5_13TeV-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/WZ_TuneCP5_13TeV-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/ZZ_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/WW_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/WZ_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
        ]
    },
} #}}}
ul_samples_2018 = { #{{{
    "data" : {
        "Data" : [
            "/EGamma/alesauva-UL2018_0-10_6_4-v0-Run2018A-12Nov2019_UL2018-v2-981b04a73c9458401b9ffd78fdd24189/USER",
            "/EGamma/alesauva-UL2018_0-10_6_4-v0-Run2018B-12Nov2019_UL2018-v2-981b04a73c9458401b9ffd78fdd24189/USER",
            "/EGamma/alesauva-UL2018_0-10_6_4-v0-Run2018C-12Nov2019_UL2018-v2-981b04a73c9458401b9ffd78fdd24189/USER",
            "/EGamma/alesauva-UL2018_0-10_6_4-v0-Run2018D-12Nov2019_UL2018-v4-981b04a73c9458401b9ffd78fdd24189/USER",
        ]
    },

    "sig" : {
        "TprimeM600_125" : ["/TprimeBToTH_Hgg_M-600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        "TprimeM625_125" : ["/TprimeBToTH_Hgg_M-625_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        "TprimeM650_125" : ["/TprimeBToTH_Hgg_M-650_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        "TprimeM675_125" : ["/TprimeBToTH_Hgg_M-675_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        "TprimeM700_125" : ["/TprimeBToTH_Hgg_M-700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        "TprimeM800_125" : ["/TprimeBToTH_Hgg_M-800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        "TprimeM900_125" : ["/TprimeBToTH_Hgg_M-900_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        "TprimeM1000_125" : ["/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        "TprimeM1100_125" : ["/TprimeBToTH_Hgg_M-1100_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        "TprimeM1200_125" : ["/TprimeBToTH_Hgg_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        #"TprimeM1300_125" : ["/TprimeBToTH_Hgg_M-1300_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        #"TprimeM1400_125" : ["/TprimeBToTH_Hgg_M-1400_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        #"TprimeM1500_125" : ["/TprimeBToTH_Hgg_M-1500_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        #"TprimeM1600_125" : ["/TprimeBToTH_Hgg_M-1600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        #"TprimeM1700_125" : ["/TprimeBToTH_Hgg_M-1700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        #"TprimeM1800_125" : ["/TprimeBToTH_Hgg_M-1800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER"],
    },

    "smh" : {
        "tth_125" : ["/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1-3fde8d2608442ffb74ed8d18d363b700/USER"],
        "thq_125" : ["/THQ_ctcvcp_HToGG_M125_TuneCP5_13TeV-madgraph-pythia8/lata-Era2018_legacy_v1_UL19-v1-v0-RunIISummer19UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-dae14ff740345aa37ec48c23e14f3dd3/USER"],
        "ggh_125" : ["/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8_storeWeights/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1-3f96409841a3cc85b911eb441562baae/USER"],
        "vbf_125" : ["/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8_storeWeights/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-cd53024353ab74068d5c62af34cd5d53/USER"],
        "vh_125"  : ["/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1-4e4629d24fb44591ff8ab61ece79898c/USER"],
    },

    "nrb" : {
        "NRB" : [
            "/DiPhotonJets_MGG-80toInf_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            
            "/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-09a907750fba2d34e04c07dbff1d88d6/USER",
            
            "/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-1189eb090a948a87991b3c60b3d75f1c/USER",
            "/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1-1189eb090a948a87991b3c60b3d75f1c/USER",
            "/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-1189eb090a948a87991b3c60b3d75f1c/USER",
            
            #"/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/TTGG_0Jets_TuneCP5_13TeV-amcatnlo-madspin-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer19UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/TGJets_TuneCP5_13TeV-amcatnlo-madspin-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer19UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            
            "/WZ_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/WW_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
        ]
    },
} #}}}

ReReco_samples_2016_myNtuple = { #{{{
    "data" : {
        "Data" : [
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016B-17Jul2018_ver2-v1-86023db6be00ee64cd62a3172358fb9f/USER",
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016C-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER",
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016D-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER",
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016E-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER",
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016F-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER",
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016G-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER",
            "/DoubleEG/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-Run2016H-17Jul2018-v1-86023db6be00ee64cd62a3172358fb9f/USER",
        ]
    },

    "sig" : {
        "tHq" : [
            "/TprimeBToTH_Hgg_M-600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER",
            "/TprimeBToTH_Hgg_M-625_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER",
            "/TprimeBToTH_Hgg_M-650_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER",
            "/TprimeBToTH_Hgg_M-675_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER",
            "/TprimeBToTH_Hgg_M-700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER",
            "/TprimeBToTH_Hgg_M-800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER",
            "/TprimeBToTH_Hgg_M-900_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER",
            "/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER",
            "/TprimeBToTH_Hgg_M-1100_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER",
            "/TprimeBToTH_Hgg_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2016_RR-17Jul2018-v2_p12-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-558f94a366de3fc00ec9d9ea7e93aa72/USER",
        ]
    },

    "smh" : {
        "SMH" : [
            "/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8_v2/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-4b15415e8d56c44d7f20bde93a158c60/USER",
            "/THQ_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCUETP8M1_v2/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-b8a5b6287120fce79bb02069cbed82a0/USER",
            "/VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-b8a5b6287120fce79bb02069cbed82a0/USER",
            "/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2-6512204af72ea57fbfefdf0db0649ffe/USER",
            "/VBFHToGG_M125_13TeV_amcatnlo_pythia8_v2/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-42666aea495bdc3a36d796ff9c4bc819/USER",
        ]
    },

    "nrb" : {
        "NRB" : [
            #"/DiPhotonJetsBox_M40_80-Sherpa/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-735d6f5d6752834cf1de64ba6920599a/USER",
            "/DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",

            "/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/TTGG_0Jets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-735d6f5d6752834cf1de64ba6920599a/USER",
            "/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",

            "/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-c7e9dfda701ffa83862108b4f8303392/USER",
            "/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",

            "/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1-735d6f5d6752834cf1de64ba6920599a/USER",
            "/WW_TuneCUETP8M1_13TeV-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/WZ_TuneCUETP8M1_13TeV-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            "/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1-735d6f5d6752834cf1de64ba6920599a/USER",
            "/ZZ_TuneCUETP8M1_13TeV-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-735d6f5d6752834cf1de64ba6920599a/USER",

            # the following dataset are not found in datalogue
            #"/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext3-v1-735d6f5d6752834cf1de64ba6920599a/USER",
            #"/WW_TuneCUETP8M1_13TeV-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",
            #"/WZ_TuneCUETP8M1_13TeV-pythia8/spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2-735d6f5d6752834cf1de64ba6920599a/USER",
        ]
    },
} #}}}
ReReco_samples_2017_myNtuple = { #{{{
    "data" : {
        "Data" : [
            "/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017B-31Mar2018-v1-d9c0c6cde5cc4a64343ae06f842e5085/USER",
            "/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017C-31Mar2018-v1-d9c0c6cde5cc4a64343ae06f842e5085/USER",
            "/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017D-31Mar2018-v1-d9c0c6cde5cc4a64343ae06f842e5085/USER",
            "/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017E-31Mar2018-v1-d9c0c6cde5cc4a64343ae06f842e5085/USER",
            "/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017F-31Mar2018-v1-6275f8d5048d2e0a580d591e02fde0b8/USER",
            "/DoubleEG/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-Run2017F-31Mar2018-v1-d9c0c6cde5cc4a64343ae06f842e5085/USER",
        ]
    },

    "sig" : {
        "tHq" : [
            "/TprimeBToTH_Hgg_M-600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-6f64939368112792100a27fcb8918a00/USER",
            "/TprimeBToTH_Hgg_M-625_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-6f64939368112792100a27fcb8918a00/USER",
            "/TprimeBToTH_Hgg_M-650_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-6f64939368112792100a27fcb8918a00/USER",
            "/TprimeBToTH_Hgg_M-675_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-6f64939368112792100a27fcb8918a00/USER",
            "/TprimeBToTH_Hgg_M-700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-6f64939368112792100a27fcb8918a00/USER",
            "/TprimeBToTH_Hgg_M-800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-6f64939368112792100a27fcb8918a00/USER",
            "/TprimeBToTH_Hgg_M-900_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-6f64939368112792100a27fcb8918a00/USER",
            "/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-6f64939368112792100a27fcb8918a00/USER",
            "/TprimeBToTH_Hgg_M-1100_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-6f64939368112792100a27fcb8918a00/USER",
            "/TprimeBToTH_Hgg_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_RR-31Mar2018_v2-v2_p11-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-6f64939368112792100a27fcb8918a00/USER",
        ]
    },

    "smh" : {
        "SMH" : [
            "/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-8898d473234391c75fcfaef6f4012781/USER",
            "/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-881967903231519e7d04858a35c22266/USER",
            "/VBFHToGG_M125_13TeV_amcatnlo_pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-fb12d0f0ef6bfdb97703485ba72bfbd7/USER",
            "/VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-bc7e32150d646e869747d832d07c9d2a/USER",
            #"/bbHToGG_M-125_4FS_yb2_13TeV_amcatnlo/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-3da075b92990944976687db6a045f405/USER",
            "/THQ_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCP5/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-bc7e32150d646e869747d832d07c9d2a/USER",
        ]
    },

    "nrb" : {
        "NRB" : [
            "/DiPhotonJetsBox_M40_80-Sherpa/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-3cb6894c0d48cb783c8c8d2d15e29103/USER",
            "/DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-4acbc742bb1007da3b7cc5c39b831d51/USER",
            "/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-4acbc742bb1007da3b7cc5c39b831d51/USER",
            "/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-4acbc742bb1007da3b7cc5c39b831d51/USER",
            "/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-4d2010f8ba2360fb4de1038d4a1ef29e/USER",

            "/GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-4d2010f8ba2360fb4de1038d4a1ef29e/USER",

            "/TGJets_TuneCP5_13TeV_amcatnlo_madspin_pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/TTGG_0Jets_TuneCP5_13TeV_amcatnlo_madspin_pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/WW_TuneCP5_13TeV-pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/WZ_TuneCP5_13TeV-pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
            "/ZZ_TuneCP5_13TeV-pythia8/spigazzi-Era2017_RR-31Mar2018_v2-legacyRun2FullV1-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2-4d2010f8ba2360fb4de1038d4a1ef29e/USER",
        ]
    },
} #}}}
ReReco_samples_2018_myNtuple = { #{{{
    "data" : {
        "Data" : [
            "/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018A-17Sep2018-v2-dc8e5fb301bfbf2559680ca888829f0c/USER",
            "/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018A-17Sep2018-v2-e35808f23b4776d10c777cb2c9d2f07a/USER",
            "/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018B-17Sep2018-v1-dc8e5fb301bfbf2559680ca888829f0c/USER",
            "/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018B-17Sep2018-v1-e35808f23b4776d10c777cb2c9d2f07a/USER",
            "/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018C-17Sep2018-v1-e35808f23b4776d10c777cb2c9d2f07a/USER",
            "/EGamma/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-Run2018D-22Jan2019-v2-dc8e5fb301bfbf2559680ca888829f0c/USER",
        ]
    },

    "sig" : {
        "tHq" : [
            "/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_RR-17Sep2018_v2-v2_p12-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-c8742baf38d1e270734b273d38e0b81b/USER",
            "/TprimeBToTH_Hgg_M-1100_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_RR-17Sep2018_v2-v2_p12-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-c8742baf38d1e270734b273d38e0b81b/USER",
            "/TprimeBToTH_Hgg_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_RR-17Sep2018_v2-v2_p12-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-c8742baf38d1e270734b273d38e0b81b/USER",
            "/TprimeBToTH_Hgg_M-600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_RR-17Sep2018_v2-v2_p12-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-c8742baf38d1e270734b273d38e0b81b/USER",
            "/TprimeBToTH_Hgg_M-625_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_RR-17Sep2018_v2-v2_p12-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-c8742baf38d1e270734b273d38e0b81b/USER",
            "/TprimeBToTH_Hgg_M-650_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_RR-17Sep2018_v2-v2_p12-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-c8742baf38d1e270734b273d38e0b81b/USER",
            "/TprimeBToTH_Hgg_M-675_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_RR-17Sep2018_v2-v2_p12-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-c8742baf38d1e270734b273d38e0b81b/USER",
            "/TprimeBToTH_Hgg_M-700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_RR-17Sep2018_v2-v2_p12-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-c8742baf38d1e270734b273d38e0b81b/USER",
            "/TprimeBToTH_Hgg_M-800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_RR-17Sep2018_v2-v2_p12-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-c8742baf38d1e270734b273d38e0b81b/USER",
            "/TprimeBToTH_Hgg_M-900_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_RR-17Sep2018_v2-v2_p12-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-c8742baf38d1e270734b273d38e0b81b/USER",
        ]
    },

    "smh" : {
        "SMH" : [
            "/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-22826b4b3f0f74a98f5d2803cae2df21/USER",
            "/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-a56b881212d7e1373ea9751571b84b54/USER",
            "/VBFHToGG_M125_13TeV_amcatnlo_pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-9e48e061eb25395806bdefdfcc4171ae/USER",
            "/VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-1304caed375f091a256618f37b82b587/USER",
            #"/bbHToGG_M-125_4FS_yb2_TuneCP5-13TeV-amcatnlo-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-db144f48e9d4babdfe9806c850922302/USER",
            "/THQ_ctcvcp_HToGG_M125_TuneCP5_13TeV-madgraph-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-db144f48e9d4babdfe9806c850922302/USER",
        ]
    },

    "nrb" : {
        "NRB" : [
            "/DiPhotonJetsBox_M40_80-Sherpa/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/DiPhotonJets_MGG-80toInf_TuneCP5_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-2fd15c7990311bd7455b91cc32d06425/USER",
            "/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-2fd15c7990311bd7455b91cc32d06425/USER",
            "/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2-fd1bbca0499161eb81400b47608e6cd0/USER",
            "/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2-fd1bbca0499161eb81400b47608e6cd0/USER",
            "/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-fd1bbca0499161eb81400b47608e6cd0/USER",

            "/GJets_HT-40To100_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV-madgraphMLM-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/GJets_HT-100To200_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV-madgraphMLM-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/GJets_HT-200To400_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV-madgraphMLM-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/GJets_HT-600ToInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV-madgraphMLM-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-08dcbeed5736d288ed971f3c5cf5bfe1/USER",

            "/TGJets_TuneCP5_13TeV_amcatnlo_madspin_pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/TTGG_0Jets_TuneCP5_13TeV_amcatnlo_madspin_pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v1-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/WW_TuneCP5_13TeV-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/WZ_TuneCP5_13TeV-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v3-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
            "/ZZ_TuneCP5_13TeV-pythia8/spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2-08dcbeed5736d288ed971f3c5cf5bfe1/USER",
        ]
    },
} #}}}
ul_samples_2017_myNtuple = { #{{{
    "data" : {
        "Data" : [
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017F-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017B-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017D-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017E-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
            "/DoubleEG/alesauva-UL_test-10_6_4-v0-Run2017C-09Aug2019_UL2017-v1-53faf905fdb551f89c40f719673e864f/USER",
        ]
    },

    "sig" : {
        "tHq" : [
            "/TprimeBToTH_Hgg_M-600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER",
            "/TprimeBToTH_Hgg_M-625_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER",
            "/TprimeBToTH_Hgg_M-650_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER",
            "/TprimeBToTH_Hgg_M-675_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER",
            "/TprimeBToTH_Hgg_M-700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER",
            "/TprimeBToTH_Hgg_M-800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER",
            "/TprimeBToTH_Hgg_M-900_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER",
            "/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER",
            "/TprimeBToTH_Hgg_M-1100_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER",
            "/TprimeBToTH_Hgg_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2017_legacy_v1-v1_p1-v0-RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2-59721402629b4b4fae2a29dd9bb0dfe1/USER",
        ]
    },

    "smh" : {
        "SMH" : [
            "/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-40c8f5e3297812fbf727853bb545f6df/USER",
            "/THQ_ctcvcp_HToGG_M125_TuneCP5_13TeV-madgraph-pythia8/alesauva-UL2017_3-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-00000000000000000000000000000000/USER",
            "/THW_ctcvcp_HToGG_M125_TuneCP5_13TeV-madgraph-pythia8/alesauva-UL2017_3-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-9bdaeb58fc35885a7495aa2986b66870/USER",
            "/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/alesauva-UL2017_3-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-9bdaeb58fc35885a7495aa2986b66870/USER",
            "/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-f92679b6f67e90fd93c35b41b89480a0/USER",
            "/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8709e8b8d2daa2ed8fac18f6d4560942/USER",
        ]
    },

    "nrb" : {
        "NRB" : [
            #"/DiPhotonJetsBox2BJets_MGG-80toInf_13TeV-sherpa/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v3-b4ca3fbc0a606daa82bec910d90e7c99/USER",
            #"/DiPhotonJetsBox_M40_80-sherpa/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v3-b4ca3fbc0a606daa82bec910d90e7c99/USER",
            #"/DiPhotonJetsBox1BJet_MGG-80toInf_13TeV-sherpa/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v3-b4ca3fbc0a606daa82bec910d90e7c99/USER",
            #"/DiPhotonJets_MGG-80toInf_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v3-b4ca3fbc0a606daa82bec910d90e7c99/USER",

            #"/GJets_DoubleEMEnriched_PtG-20MGG-40To80_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/GJets_DoubleEMEnriched_PtG-40MGG-80_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/GJets_DoubleEMEnriched_PtG-20MGG-80_TuneCP5_13TeV-madgraphMLM-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            #"/GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-4cores5k_106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            
            #"/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            "/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            
            #"/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/TGJets_TuneCP5_13TeV-amcatnlo-madspin-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/TTGG_0Jets_TuneCP5_13TeV-amcatnlo-madspin-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
            
            #"/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/alesauva-UL2017-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/alesauva-UL2017_5-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v1-8980ba169e8b72d53459e52844728ed8/USER",
            #"/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/ZZ_TuneCP5_13TeV-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/WW_TuneCP5_13TeV-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            #"/WZ_TuneCP5_13TeV-pythia8/alesauva-UL2017_2-10_6_4-v0-RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2-8980ba169e8b72d53459e52844728ed8/USER",
            "/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/ZZ_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/WW_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
            "/WZ_TuneCP5_13TeV-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1-01f31eaceb254ddd929b0978a7323b12/USER",
        ]
    },

    "ttjets" : {
        "NRB" : [
            "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2017_legacy_v1-v1_p2-v0-RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2-01f31eaceb254ddd929b0978a7323b12/USER",
        ]
    },
} #}}}
ul_samples_2018_myNtuple = { #{{{
    "data" : {
        "Data" : [
            "/EGamma/alesauva-UL2018_0-10_6_4-v0-Run2018A-12Nov2019_UL2018-v2-981b04a73c9458401b9ffd78fdd24189/USER",
            "/EGamma/alesauva-UL2018_0-10_6_4-v0-Run2018B-12Nov2019_UL2018-v2-981b04a73c9458401b9ffd78fdd24189/USER",
            "/EGamma/alesauva-UL2018_0-10_6_4-v0-Run2018C-12Nov2019_UL2018-v2-981b04a73c9458401b9ffd78fdd24189/USER",
            "/EGamma/alesauva-UL2018_0-10_6_4-v0-Run2018D-12Nov2019_UL2018-v4-981b04a73c9458401b9ffd78fdd24189/USER",
        ]
    },

    "sig" : {
        "tHq" : [
            "/TprimeBToTH_Hgg_M-600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER",
            "/TprimeBToTH_Hgg_M-625_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER",
            "/TprimeBToTH_Hgg_M-650_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER",
            "/TprimeBToTH_Hgg_M-675_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER",
            "/TprimeBToTH_Hgg_M-700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER",
            "/TprimeBToTH_Hgg_M-800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER",
            "/TprimeBToTH_Hgg_M-900_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER",
            "/TprimeBToTH_Hgg_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER",
            "/TprimeBToTH_Hgg_M-1100_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER",
            "/TprimeBToTH_Hgg_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/lata-Era2018_legacy_v1-v1_p1-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-dae14ff740345aa37ec48c23e14f3dd3/USER",
        ]
    },

    "smh" : {
        "SMH" : [
            "/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1-3fde8d2608442ffb74ed8d18d363b700/USER",
            "/THQ_ctcvcp_HToGG_M125_TuneCP5_13TeV-madgraph-pythia8/lata-Era2018_legacy_v1_UL19-v1-v0-RunIISummer19UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-dae14ff740345aa37ec48c23e14f3dd3/USER",
            "/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8_storeWeights/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1-3f96409841a3cc85b911eb441562baae/USER",
            "/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8_storeWeights/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-cd53024353ab74068d5c62af34cd5d53/USER",
            "/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1-4e4629d24fb44591ff8ab61ece79898c/USER",
        ]
    },

    "nrb" : {
        "NRB" : [
            "/DiPhotonJets_MGG-80toInf_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            
            "/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-09a907750fba2d34e04c07dbff1d88d6/USER",
            
            "/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-1189eb090a948a87991b3c60b3d75f1c/USER",
            "/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1-1189eb090a948a87991b3c60b3d75f1c/USER",
            "/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/alesauva-UL2018_0-10_6_4-v0-RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2-1189eb090a948a87991b3c60b3d75f1c/USER",
            
            #"/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/TTGG_0Jets_TuneCP5_13TeV-amcatnlo-madspin-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer19UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/TGJets_TuneCP5_13TeV-amcatnlo-madspin-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer19UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            
            "/WZ_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/WW_TuneCP5_13TeV-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
            "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
        ]
    },

    "ttjets" : {
        "NRB" : [
            "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/lata-Era2018_legacy_v1-v1_p2-v0-RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1-09a907750fba2d34e04c07dbff1d88d6/USER",
        ]
    },
} #}}}

ul_samples = {
    2016 : ReReco_samples_2016_myNtuple,
    2017 : ul_samples_2017_myNtuple,
    2018 : ul_samples_2018_myNtuple,
    #2016 : ReReco_samples_2016,
    #2017 : ul_samples_2017,
    #2018 : ul_samples_2018,
}

rr_samples = {
    2016 : ReReco_samples_2016_myNtuple,
    2017 : ReReco_samples_2017_myNtuple,
    2018 : ReReco_samples_2018_myNtuple,
}

