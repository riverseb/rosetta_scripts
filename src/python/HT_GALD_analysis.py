# Author: @riverseb
print("Importing packages...")
import os 
import postGALD_process as pgp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
from pymol import cmd, finish_launching

def HT_process(input_name, GALD_repeats=100, n_structs=100, 
               native=None, rmsd=True, query_pdbs="pdbs/", query_lig=None, 
               ref_lig=None, clean=True, rmsd_path=None, score_path="scores/fullscore_sorted.sc"):
    print("Starting HT process...")
    i = 0
    # Create empty dataframe
    pnears_CIs = pd.DataFrame(columns=['pnear', 'CI', 'best_rmsd', 'total_score', 'best_model'])
    # loop by the number of structures in the dock
    for i in range(1, n_structs + 1):
        split_input_name = input_name.split("_")
        inputFile = "_".join(split_input_name[0:2]) + f"_{i}_" + "_".join(split_input_name[2:])
        print(f"Starting: {inputFile}", flush=True)
        os.chdir(inputFile)
        pnear, CI, best_model =pgp.main(project=inputFile, inputFile=inputFile, 
                                        repeats=GALD_repeats, native=native, 
                                        rmsd=rmsd, query_pdbs=query_pdbs, 
                                        query_lig=query_lig, ref_lig=ref_lig, 
                                        clean=clean, rmsd_path=rmsd_path, 
                                        score_path=score_path)
        results = {
            'pnear': pnear,
            'CI': CI,
            'best_rmsd': best_model['rmsd'],
            'total_score': best_model['total_score'],
            'best_model': best_model['description']
        }
        print(f"Done postGALD processing: {inputFile}")
        pnears_CIs = pnears_CIs.append(results, ignore_index=True)
        print(f"Done: {inputFile}")
        os.chdir("..")
        i += 1
    pnears_CIs.to_csv('pnears_CIs.csv', index=False, sep='\t')
    return pnears_CIs
def pnear_hist(pnear_CIs):
    fig = plt.figure(figsize=(10,6))
    ax = sns.histplot(data=pnear_CIs, x='pnear', kde=True, stat="count")
    ax.set_xlim(0, 1)
    plt.savefig('pnear_hist.png', dpi=300)

def main(input_name, n_structs=100, GALD_repeats=100, native=None, 
         rmsd=True, query_pdbs="pdbs/", query_lig=None, ref_lig=None, clean=True, 
         rmsd_path=None, score_path="scores/fullscore_sorted.sc"):
    pnears_CIs = HT_process(input_name, GALD_repeats=GALD_repeats, 
                            n_structs=n_structs, native=native, rmsd=rmsd, 
                            query_pdbs=query_pdbs, query_lig=query_lig, 
                            ref_lig=ref_lig, clean=clean, rmsd_path=rmsd_path, 
                            score_path=score_path)
    pnear_hist(pnears_CIs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_name", type=str, help="input name")
    parser.add_argument("--n_structs", type=int, default=100)
    parser.add_argument("--GALD_repeats", type=int, default=100)
    parser.add_argument("--native", type=str, default=None)
    parser.add_argument("--no_rmsd", action="store_false", dest="rmsd")
    parser.add_argument("--query_pdbs", type=str, default="pdbs/")
    parser.add_argument("--query_lig", type=str, default=None)
    parser.add_argument("--ref_lig", type=str, default=None)
    parser.add_argument("--no_clean", action="store_false", dest="clean")
    parser.add_argument("--rmsd_path", type=str, default=None)
    parser.add_argument("--score_path", type=str, default="scores/fullscore_sorted.sc")
    args = parser.parse_args()
    print("Reading command line arguments...")
    main(**vars(args))