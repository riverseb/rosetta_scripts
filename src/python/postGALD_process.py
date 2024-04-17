#Authors: @riverseb
import argparse
from argparse import ArgumentError
import GALD_file_clean as file_clean
import calcRMSD_atomSubset as rmsd_calc
import rmsd_vs_score as rmsd_plot
import os
import warnings

def main(project, inputFile, repeats=5, native=None, rmsd=True, query_pdbs="pdbs/", 
         query_lig=None, ref_lig=None, clean=True, rmsd_path=None,
         score_path="scores/fullscore_sorted.sc", overwrite=False):
    """ 
    Cleans the GALigandDock output files and generates rmsd vs score plots

    :param project: name of project
    :param repeats: number of repeats
    :param native: path to native pdb
    :param rmsd: calculate rmsd? (Boolean)
    :param query_pdbs: path to query pdbs
    :param query_lig: query ligand
    :param ref_lig: reference ligand
    :param clean: clean files? (Boolean)
    :param rmsd_path: path to rmsd vs score plot
    :param score_path: path to score file
    """
    if clean:
        print("Cleaning files...")
        file_clean.main(project, inputFile, repeats)
    
    ref_name = native.split("/")[-1].split(".")[0]

    if not rmsd_path:
        rmsd_path = f"scores/rmsd_scores_{ref_name}.txt"
    
    if rmsd:
        if query_lig and ref_lig:
            print("Calculating rmsd...")
            if not os.path.exists(rmsd_path) or overwrite or os.stat(rmsd_path).st_size == 0:
                rmsd_calc.main(native, query_pdbs, ref_lig, query_lig)
            else:
                warnings.warn(message=f"RMSD file for {ref_name} already exisits. \
                              To overwrite, provide --overwrite arg.")

        else:
            raise ArgumentError(message="ERROR: Must provide query and reference residue name")   
    
    if not native:
        raise ArgumentError(message="ERROR: Must provide reference structure")
    print("Plotting rmsd vs score...", flush=True)        
    pnear, CI, best_model =rmsd_plot.main(rmsd_path, ref_name, score_path,
                                            outfile="PNear.txt")
    print(f"PNear: {pnear:.2f} (CI 95%:[{CI[0]:.3f} - {CI[1]:.3f}]), Best Model: {best_model}")
    
    results = {
    'pnear': pnear,
    'CI': CI,
    'best_rmsd': best_model['rmsd'],
    'total_score': best_model['total_score'],
    'best_model': best_model['description']
    }

    return results

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
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    main(**vars(args))
    