#!/bin/bash

#SBATCH --job-name=CitL_relax
#SBATCH --mail-user=riverseb@umich.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=/nfs/turbo/umms-maom/projects/IMDAase/rosetta/relax_v4/logs/CitL_relax_v4.log
#SBATCH --partition=standard
#SBATCH --mem-per-cpu=4g
#SBATCH --cpus-per-task=1
#SBATCH --time=00-04:00:00
#SBATCH --account=maom0

module restore
/sw/pkgs/med/Rosetta/3.13/main/source/bin/relax.linuxgccrelease -s $1 -gen_potential -parser:protocol ../relax.xml -in:file:fullatom -out:file:silent $1_relaxed.out -nstruct 10 -in:file:extra_res_path /nfs/turbo/umms-maom/projects/IMDAase/rosetta/gen_params/ 