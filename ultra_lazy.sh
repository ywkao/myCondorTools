#!/bin/bash

function check()
{
    dir='examine'
    dir='tmp_ntuples_data_2018'
    #dir='ntuples_data_2018'
    #vimdiff $dir/$1 $dir/$2


    #sed -i 's/tomorrow/workday/g' $dir/${1}.sub
    #sed -i 's/ntuples/tmp_ntuples/g' $dir/${1}.sub
    #sed -i 's/ntuples/tmp_ntuples/g' $dir/${1}.sh
    #vim $dir/${1}.sub
    #vim $dir/${1}.sh

    #grep 'workday' $dir/${1}.sub
    #grep 'tmp_ntuples' $dir/${1}.sub
    #grep 'tmp_ntuples' $dir/${1}.sh

    grep 'queue' $dir/${1}.sub
    grep 'declare' $dir/${1}.sh
}
#check mylist_data_2016_20210706.txt
#check runJobs1
#check runJobs2
#check runJobs3
#check runJobs4
#check runJobs5

function move()
{
    mkdir -p $2
    #mv $1/*root $2
    mv $1/*err $2
    mv $1/*out $2
    mv $1/*log $2
}
#move ntuples_data_2016 errFiles_data_2016_v3
#move ntuples_data_2017 errFiles_data_2017_v3
#move ntuples_data_2018 errFiles_data_2018_v3

function backup()
{
    dir="examine"
    #mv $dir/$1 $dir/$2
    mv $1 $2
}
#backup check_list.txt check_list_0709.txt
#backup mylist.txt mylist_0709.txt
#backup latest_resubmit_list.txt latest_resubmit_list_0709.txt

#backup examine/check_list_data_2018_20210710.txt examine/check_list_data_2018_20210710_v1.txt
#backup examine/latest_resubmit_list_data_2018_20210710.txt examine/latest_resubmit_list_data_2018_20210710_v1.txt
#backup examine/mylist_data_2018_20210710.txt examine/mylist_data_2018_20210710_v1.txt
#backup examine/uniq_list_data_2018_20210710.txt examine/uniq_list_data_2018_20210710_v1.txt
