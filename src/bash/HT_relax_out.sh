#!/bin/bash

#SBATCH --job-name=HT_relax_out
#SBATCH --mail-user=riverseb@umich.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=/nfs/turbo/umms-maom/projects/IMDAase/rosetta/relax_lmpnn_itr1_HT_ZWPneut/logs/relax_out_HT_%a.log
#SBATCH --partition=standard
#SBATCH --mem-per-cpu=2g
#SBATCH --array=1-100
#SBATCH --cpus-per-task=1
#SBATCH --time=00-00:30:00
#SBATCH --account=maom99

module load Rosetta Bioinformatics
dir_list=( $(find $1 -type d -exec basename {} \;) )
# sorts files in numerical order and strips extension
sorted_dir_list=($(printf "%s\n" "${dir_list[@]}" | sort -d))
if [ ! -d best_models ]; then
    mkdir best_models
fi
cd ${sorted_dir_list[ $SLURM_ARRAY_TASK_ID - 1 ]}
tag=$(python /nfs/turbo/umms-maom/projects/IMDAase/rosetta/scripts/src/python/lowest_tag.py *.out)
$ROSETTA3/bin/extract_pdbs.linuxgccrelease -in:file:silent *.out -in:file:extra_res_path ../../gen_params/ -tags $tag -gen_potential
cp $tag.pdb ../best_models/$tag.pdb