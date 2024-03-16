#!/bin/bash

#SBATCH --job-name=relax_PhqE
#SBATCH --mail-user=riverseb@umich.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=/nfs/turbo/umms-maom/projects/IMDAase/rosetta/relax_PhqE/logs/relax_PhqE.log
#SBATCH --partition=standard
#SBATCH --mem-per-cpu=4g
#SBATCH --cpus-per-task=1
#SBATCH --time=00-04:00:00
#SBATCH --account=maom0

module restore
/sw/pkgs/med/Rosetta/3.13/main/source/bin/relax.linuxgccrelease -s $1.pdb -relax:script /sw/pkgs/med/Rosetta/3.13/main/database/sampling/relax_scripts/legacy.beta_nov16.txt -in:file:fullatom -out:file:silent $1_relaxed.out -nstruct 10 -in:file:extra_res_path /nfs/turbo/umms-maom/projects/IMDAase/rosetta/gen_params/ -gen_potential