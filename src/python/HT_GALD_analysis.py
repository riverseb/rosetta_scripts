# Author: @riverseb
print("Importing packages...")
import os 
import postGALD_process as pgp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
from pymol import cmd, finish_launching
from pnear_vs_pnear import main as pnear_plt
import warnings

def pnear_hist(pnear_CIs):
    fig = plt.figure(figsize=(10,6))
    ax = sns.histplot(data=pnear_CIs, x='pnear', kde=True, stat="count")
    ax.set_xlim(0, 1)
    plt.savefig('pnear_hist.png', dpi=300)

def HT_process(project_dir, GALD_repeats=50, native=None, rmsd=True, query_pdbs="pdbs/", 
               ref_lig=None, target=None, target_lig=None, clean=True, 
               rmsd_path=None, score_path="scores/fullscore_sorted.sc",):
    print("Starting HT process...")

    os.chdir(project_dir)
    # Create empty dataframe
    pnears_CIs = pd.DataFrame(columns=['pnear', 'CI', 'best_rmsd', 'total_score', 'best_model'])
    pnear_vs_pnear = pd.DataFrame(columns=[f'PNear {ref_lig}', f'PNear {target_lig}', 'Protein'])
    dirList = [dir for dir in os.listdir() if os.path.isdir(dir) and dir != "logs"]
    sorted_dirList = sorted(dirList)

    # loop by the number of structures in the dock
    for dir in sorted_dirList:
        print(f"Starting: {dir}", flush=True)
        
        try:
            os.chdir(dir)
        except:
            # warnings.showwarning(f"WARNING: {dir} does not exist", filename="HT_process_errors.txt")
            continue

        os.chdir(f"{dir}_{ref_lig}")

        ref_results = pgp.main(project=f"{dir}_{ref_lig}", 
                                         inputFile=f"{dir}_{ref_lig}", 
                                         repeats=GALD_repeats, native=native, 
                                         rmsd=rmsd, query_pdbs=query_pdbs, 
                                         query_lig=ref_lig, ref_lig=ref_lig, 
                                         clean=clean, rmsd_path=rmsd_path, 
                                         score_path=score_path)
    
        print(f"Done postGALD processing: {dir}_{ref_lig}", flush=True)
        pnears_CIs = pnears_CIs.append(ref_results, ignore_index=True)
        pnear_native = ref_results["pnear"]
        
        os.chdir(f"../{dir}_{target_lig}")

        target_results = pgp.main(project=f"{dir}_{target_lig}", 
                                         inputFile=f"{dir}_{target_lig}", 
                                         repeats=GALD_repeats, native=target, rmsd=rmsd, 
                                         query_pdbs=query_pdbs, query_lig=target_lig, 
                                         ref_lig=target_lig, clean=clean, rmsd_path=rmsd_path, 
                                         score_path=score_path)
    
        print(f"Done postGALD processing: {dir}_{target_lig}", flush=True)
        pnears_CIs = pnears_CIs.append(target_results, ignore_index=True)
        pnear_target = target_results["pnear"]
        
        new_row = {
            f'PNear {ref_lig}': pnear_native, 
            f'PNear {target_lig}': pnear_target, 
            'Protein': dir
            }
        
        pnear_vs_pnear = pnear_vs_pnear.append(new_row, ignore_index=True)
        print(f"Done: {dir}")
        os.chdir("../..")
    
    pnears_CIs.to_csv('pnears_CIs.csv', index=False, sep='\t')
    pnear_vs_pnear.to_csv('pnear_vs_pnear.csv', index=False, sep='\t')
    
    pnear_plt("pnear_vs_pnear.csv", f'PNear {ref_lig}', f'PNear {target_lig}')
    pnear_hist(pnears_CIs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", type=str, help="Project directory")
    parser.add_argument("--GALD_repeats", type=int, default=50)
    parser.add_argument("--native", type=str, default=None)
    parser.add_argument("--target", type=str, default=None)
    parser.add_argument("--target_lig", type=str, default=None)
    parser.add_argument("--no_rmsd", action="store_false", dest="rmsd")
    parser.add_argument("--query_pdbs", type=str, default="pdbs/")
    parser.add_argument("--ref_lig", type=str, default=None)
    parser.add_argument("--no_clean", action="store_false", dest="clean")
    parser.add_argument("--rmsd_path", type=str, default=None)
    parser.add_argument("--score_path", type=str, default="scores/fullscore_sorted.sc")
    args = parser.parse_args()
    print("Reading command line arguments...")
    HT_process(**vars(args))