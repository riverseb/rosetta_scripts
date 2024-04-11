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

def HT_process(project_dir, GALD_repeats=50, n_structs=100, 
               native=None, rmsd=True, query_pdbs="pdbs/", query_lig=None, 
               ref_lig=None, target=None, target_lig=None, clean=True, rmsd_path=None, score_path="scores/fullscore_sorted.sc"):
    print("Starting HT process...")
    i = 0
    query_lig_list = query_lig.split(",")
    # Create empty dataframe
    pnears_CIs = pd.DataFrame(columns=['pnear', 'CI', 'best_rmsd', 'total_score', 'best_model'])
    pnear_vs_pnear = pd.DataFrame(columns=[f'PNear {query_lig_list[0]}', f'PNear {query_lig_list[1]}', 'Protein'])
    dirList = [dir for dir in os.listdir() if os.path.isdir(dir) and dir != "logs"]
    sorted_dirList = sorted(dirList)

    # loop by the number of structures in the dock
    for i in range(0, n_structs):
        # split_input_name = input_name.split("_")
        # inputFile = "_".join(split_input_name[0:2]) + f"_{i}_" + "_".join(split_input_name[2:])
        inputFile = sorted_dirList[i]
        print(f"Starting: {inputFile}", flush=True)
        try:
            os.chdir(inputFile)
        except:
            print(f"WARNING: {inputFile} does not exist")
            continue
        
        os.chdir(f"{inputFile}_{query_lig_list[0]}")
        pnear, CI, best_model = pgp.main(project=f"{inputFile}_{query_lig_list[0]}", inputFile=f"{inputFile}_{query_lig_list[0]}", 
                                    repeats=GALD_repeats, native=native, 
                                    rmsd=rmsd, query_pdbs=query_pdbs, 
                                    query_lig=query_lig_list[0], ref_lig=ref_lig, 
                                    clean=clean, rmsd_path=rmsd_path, 
                                    score_path=score_path)
        results = {
        'pnear': pnear,
        'CI': CI,
        'best_rmsd': best_model['rmsd'],
        'total_score': best_model['total_score'],
        'best_model': best_model['description']
        }
        print(f"Done postGALD processing: {inputFile}_{query_lig_list[0]}", flush=True)
        pnears_CIs = pnears_CIs.append(results, ignore_index=True)
        pnear_native = pnear
        
        os.chdir(f"../{inputFile}_{query_lig_list[1]}")
        pnear, CI, best_model = pgp.main(project=f"{inputFile}_{query_lig_list[1]}", 
                                         inputFile=f"{inputFile}_{query_lig_list[1]}", repeats=GALD_repeats, 
                                         native=target, rmsd=rmsd, query_pdbs=query_pdbs, 
                                         query_lig=query_lig_list[1], ref_lig=target_lig, 
                                         clean=clean, rmsd_path=rmsd_path, 
                                         score_path=score_path)
        results = {
        'pnear': pnear,
        'CI': CI,
        'best_rmsd': best_model['rmsd'],
        'total_score': best_model['total_score'],
        'best_model': best_model['description']
        }
        print(f"Done postGALD processing: {inputFile}_{query_lig_list[1]}", flush=True)
        pnears_CIs = pnears_CIs.append(results, ignore_index=True)
        pnear_target = pnear
        new_row = {f'PNear {query_lig_list[0]}': pnear_native, f'PNear {query_lig_list[1]}': pnear_target, 'Protein': inputFile}
        pnear_vs_pnear = pnear_vs_pnear.append(new_row, ignore_index=True)
        print(f"Done: {inputFile}")
        i += 1
        os.chdir("../..")
    pnears_CIs.to_csv('pnears_CIs.csv', index=False, sep='\t')
    return pnears_CIs, pnear_vs_pnear
def pnear_hist(pnear_CIs):
    fig = plt.figure(figsize=(10,6))
    ax = sns.histplot(data=pnear_CIs, x='pnear', kde=True, stat="count")
    ax.set_xlim(0, 1)
    plt.savefig('pnear_hist.png', dpi=300)

def main(project_dir, n_structs=100, GALD_repeats=50, native=None, 
         rmsd=True, query_pdbs="pdbs/", query_lig=None, ref_lig=None, target=None, 
         target_lig=None, clean=True, rmsd_path=None, score_path="scores/fullscore_sorted.sc"):
    pnears_CIs, pnear_vs_pnear = HT_process(project_dir, GALD_repeats=GALD_repeats, 
                            n_structs=n_structs, native=native, rmsd=rmsd, 
                            query_pdbs=query_pdbs, query_lig=query_lig, 
                            ref_lig=ref_lig, target_lig=target_lig, target=target, 
                            clean=clean, rmsd_path=rmsd_path, score_path=score_path)
    query_lig_list = args.query_lig.split(",")
    pnear_plt(pnear_vs_pnear, f'PNear {query_lig_list[0]}', f'PNear {query_lig_list[1]}')
    pnear_hist(pnears_CIs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", type=str, help="Project directory")
    parser.add_argument("--n_structs", type=int, default=100)
    parser.add_argument("--GALD_repeats", type=int, default=50)
    parser.add_argument("--native", type=str, default=None)
    parser.add_argument("--target", type=str, default=None)
    parser.add_argument("--target_lig", type=str, default=None)
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