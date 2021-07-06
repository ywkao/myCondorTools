#!/bin/bash
set -e
target="/eos/user/y/ykao/tPrimeExcessHgg/rootfiles/plots"

function move()
{
    echo ">>> start to transfer $1"
    mv $1 $target
    ln -s $target/$1 $1
}

move "plots_20210617"
move "plots_20210618_consistency_check"
move "plots_20210619_consistency_check_after_mvahelper"
move "plots_20210619_myhists"
move "plots_20210619_myhists_v2"
move "plots_20210619_myhists_v3"
move "plots_20210621_forMaxime"
move "plots_20210622_v1"
move "plots_20210622_v2_tprimeCut"
move "plots_20210623_v1_morePatches"
move "plots_20210623_v2_morePatches_tprimeCut"
move "plots_20210623_v2_morePatches_tprimeCut_fakePhotonStudy"
move "plots_20210623_v3_morePatches_sidebandOnly"

echo ">>> finished!"
