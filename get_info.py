#!/usr/bin/env python
import glob

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
    get_dir("195148")
    get_dir("195149")
    get_dir("195150")
    get_dir("195151")
    get_dir("195152")
    get_dir("195153")
    get_dir("195154")
    get_dir("195155")
    get_dir("195156")
    get_dir("195157")
    get_dir("195158")
    get_dir("195159")
    get_dir("195160")
    get_dir("195161")
    get_dir("195162")
    get_dir("195163")
    get_dir("195164")

if __name__ == "__main__":
    #check_run_scripts()
    check_job_id()
