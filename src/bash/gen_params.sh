#!/bin/bash
#SBATCH --job-name=gen_params
#SBATCH --mail-user=riverseb@umich.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=/nfs/turbo/umms-maom/projects/IMDAase/rosetta/logs/gen_params.log
#SBATCH --account=maom0
#SBATCH --partition=standard
#SBATCH --mem-per-cpu=2g
#SBATCH --time=02:00:00

# Usage: ./gen_params.sh {ligand 3 letter code} {charge of ligand}"
# Must have mol2 ligand file in same directory that script is submitted from. Ensure that ligand file is named {3 letter code}.mol2

if [ "$#" -eq 0 ]; then

	echo
	echo "./gen_params.sh {ligand 3 letter code} {charge of ligand}"
	echo
	exit 1
fi
	module restore
	antechamber -i $1.mol2 -fi mol2 -o $1_charged.mol2 -fo mol2 -c bcc -nc $2
	python3 /sw/pkgs/med/Rosetta/3.13/main/source/scripts/python/public/generic_potential/mol2genparams.py -s $1_charged.mol2 --nm=$1  