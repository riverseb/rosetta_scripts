import argparse
from argparse import ArgumentError
import os
import GALD_file_clean as file_clean
import calcRMSD_atomSubset as rmsd_calc
import rmsd_vs_score as rmsd_plot 

def main(project, inputFile, repeats=5, native=None, rmsd=True, query_pdbs="pdbs/", 
         query_lig=None, ref_lig=None, clean=True, rmsd_path=None,
         score_path="scores/fullscore_sorted.sc"):
    if clean:
        file_clean.main(project, inputFile, repeats)
    if rmsd and native:
        if query_lig and ref_lig:
            rmsd_calc.main(native, query_pdbs, ref_lig, query_lig)
        elif not query_lig and not ref_lig:
            ref_parsed_lig = native.strip(".pdb").split("_")[-1]
            query_parsed_lig = inputFile.strip(".pdb").split("_")[-1]
            rmsd_calc.main(native, query_pdbs, ref_parsed_lig, query_parsed_lig)
        elif query_lig and not ref_lig:
            ref_parsed_lig = native.strip(".pdb").split("_")[-1]
            rmsd_calc.main(native, query_pdbs, ref_lig, query_parsed_lig)
        elif not query_lig and ref_lig:
            query_parsed_lig = inputFile.strip(".pdb").split("_")[-1]
            rmsd_calc.main(native, query_pdbs, ref_parsed_lig, query_lig)
        ref_name = native.split("/")[-1].split(".")[0]
        if not rmsd_path:
            rmsd_path = f"scores/rmsd_scores_{ref_name}.txt"
        rmsd_plot.main(rmsd_path, ref_name, score_path)
    elif rmsd and not native:
        raise ArgumentError("Must provide native pdb file for rmsd calculation.")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=str, help="project name")
    parser.add_argument("inputFile", type=str, help="input file name")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--native", type=str, default=None)
    parser.add_argument("--no_rmsd", action="store_false", dest="rmsd")
    parser.add_argument("--query_pdbs", type=str, default="pdbs/")
    parser.add_argument("--query_lig", type=str, default=None)
    parser.add_argument("--ref_lig", type=str, default=None)
    parser.add_argument("--no_clean", action="store_false", dest="clean")
    parser.add_argument("--rmsd_path", type=str, default=None)
    parser.add_argument("--score_path", type=str, default="scores/fullscore_sorted.sc")
    args = parser.parse_args()
    main(**vars(args))
    