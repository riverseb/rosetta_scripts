#!/bin/bash

#SBATCH --job-name=GALD_HT_CitL_PC2
#SBATCH --mail-user=riverseb@umich.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=/nfs/turbo/umms-maom/projects/IMDAase/rosetta/GALD_HT_CitL_PC2/logs/GALD_HT_CitL_PC2_%a.log
#SBATCH --partition=standard
#SBATCH --array=1-100
#SBATCH --account=maom99
#SBATCH --mem-per-cpu=5g
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00

module restore

if [ "$#" -eq 0 ]; then
    echo
    echo "./GALD.sh input.pdb"
    echo
    exit 1
fi
    if [ ! -d "$SLURM_JOB_NAME"_"$SLURM_ARRAY_TASK_ID" ]; then
    mkdir "$SLURM_JOB_NAME"_"$SLURM_ARRAY_TASK_ID"	
    fi

    cd "$SLURM_JOB_NAME"_"$SLURM_ARRAY_TASK_ID"
    /sw/pkgs/med/Rosetta/3.13/main/source/bin/rosetta_scripts.default.linuxgccrelease -s ../$1 @ /nfs/turbo/umms-maom/projects/IMDAase/rosetta/GAligand.options      
