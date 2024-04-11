#!/bin/bash

#SBATCH --job-name=HT_GALD_start
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=riverseb@umich.edu
#SBATCH --partition=standard
#SBATCH --time=01:15:00
#SBATCH --account=davidhs1
#SBATCH --output=logs/HT_GALD_start_%a.log
#SBATCH --array=1-25%3
#SBATCH --cpus-per-task=1

module restore
python /nfs/turbo/umms-maom/projects/IMDAase/rosetta/scripts/src/python/HT_rosetta_start.py $1 $SLURM_ARRAY_TASK_ID
sleep 1h