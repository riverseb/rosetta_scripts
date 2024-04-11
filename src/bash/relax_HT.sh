#!/bin/bash

#SBATCH --job-name=ZWPneut_relax_HT_CitL_CM4
#SBATCH --mail-user=riverseb@umich.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=/nfs/turbo/umms-maom/projects/IMDAase/rosetta/relax_HT_CitL_CM4_ZWPneut/logs/relax_HT_CitL_CM4_ZWPneut_%a.log
#SBATCH --partition=standard
#SBATCH --mem-per-cpu=4g
#SBATCH --array=1-100
#SBATCH --cpus-per-task=1
#SBATCH --time=00-02:00:00
#SBATCH --account=davidhs1

module restore
file_list=( $(find $1 -type f -exec basename {} \;) )
# sorts files in numerical order and strips extension
sorted_file_list=($(printf "%s\n" "${file_list[@]%.*}" | sort -d))

if [ ! -d "${sorted_file_list[ $SLURM_ARRAY_TASK_ID - 1 ]}" ]; then
    mkdir "${sorted_file_list[ $SLURM_ARRAY_TASK_ID - 1 ]}"
fi
cd "${sorted_file_list[ $SLURM_ARRAY_TASK_ID - 1]}"
/sw/pkgs/med/Rosetta/3.13/main/source/bin/relax.linuxgccrelease -s ../"$1"/"${sorted_file_list[ $SLURM_ARRAY_TASK_ID - 1 ]}".pdb -relax:script "$ROSETTA3_DB"/sampling/relax_scripts/legacy.beta_nov16.txt -out:file:silent "${sorted_file_list[ $SLURM_ARRAY_TASK_ID - 1 ]}"_relaxed.out -nstruct 10 -in:file:extra_res_path /nfs/turbo/umms-maom/projects/IMDAase/rosetta/gen_params/ -gen_potential