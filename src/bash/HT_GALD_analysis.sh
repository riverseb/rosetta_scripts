#!/bin/bash

#SBATCH --job-name=HT_GALD_analysis
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=riverseb@umich.edu
#SBATCH --partition=standard
#SBATCH --time=00-02:01:15
#SBATCH --account=davidhs1
#SBATCH --output=logs/HT_GALD_analysis_1.log
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=16g
#bash --rcfile ~/.bashrc
module restore
source /sw/pkgs/arc/python3.10-anaconda/2023.03/etc/profile.d/conda.sh
conda activate default
/home/riverseb/.conda/envs/default/bin/python -u /nfs/turbo/umms-maom/projects/IMDAase/rosetta/scripts/src/python/HT_GALD_analysis.py ./\
 --native /nfs/turbo/umms-maom/projects/IMDAase/rosetta/ref_structures/lmpnnHM1_PM7_GALD.pdb\
 --target /nfs/turbo/umms-maom/projects/IMDAase/rosetta/ref_structures/lmpnnHM1_PC2_GALD.pdb\
 --query_lig PM7,PC2 --ref_lig PM7 --n_structs 25 --target_lig PC2