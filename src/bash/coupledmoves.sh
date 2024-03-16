#!/bin/bash

#SBATCH --job-name=CM_design_CitL
#SBATCH --mail-user=riverseb@umich.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=/nfs/turbo/umms-maom/projects/IMDAase/rosetta/CMGP_CM4-58-2_PC2/logs/CMGP_CM4-58-2_PC2.log
#SBATCH --partition=standard
#SBATCH --mem-per-cpu=3g
#SBATCH --account=maom0
#SBATCH --cpus-per-task=1
#SBATCH --time=00-04:00:00

module restore
/sw/pkgs/med/Rosetta/3.13/main/source/bin/rosetta_scripts.default.linuxgccrelease -s $1 -parser:protocol /nfs/turbo/umms-maom/projects/IMDAase/rosetta/coupledmoves_GA.xml -packing:resfile /nfs/turbo/umms-maom/projects/IMDAase/rosetta/CitL_narrow.resfile -parser:script_vars res_file=/nfs/turbo/umms-maom/projects/IMDAase/rosetta/CitL_narrow.resfile @ ../flags.txt 
