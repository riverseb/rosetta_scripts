# Authors: @riverseb
import os 
from shutil import copy
import argparse
# parse through AlphaFold2 output folders and copy first model to specified dir
def copy_rename_best_model(model_dir, output_name, output_dir):
    if not os.path.exists(output_dir): os.mkdir(output_dir)
    model_dir_namesplit = model_dir.split("_")
    index = model_dir_namesplit[4] + "_" + model_dir_namesplit[5]
    pdb_list = [pdbFile for pdbFile in os.listdir(model_dir) if pdbFile.endswith(".pdb")]
    relax_found = False
    for pdb in pdb_list:
        if pdb.startswith("relaxed_model"):
            copy(f'{model_dir}/{pdb}', f'{output_dir}/{output_name}_{index}.pdb')
            relax_found = True
            break
    if not relax_found:        
        try:
            copy(f'{model_dir}/unrelaxed_model_1_pred_0.pdb', f'{output_dir}/{output_name}_{index}.pdb')
            print("No relaxed model found in " + model_dir + ", using unrelaxed model")
        except:
            print("Couldn't find output models in " + model_dir)


def main(af2_HT_dir, output_name, output_dir):
   # os.chdir(af2_HT_dir)
    for model_dir in [model_dir for model_dir in os.listdir(af2_HT_dir) if os.path.isdir(f"{af2_HT_dir}{model_dir}") and (model_dir != "logs" and model_dir != "best_models")]:
        dir_path = af2_HT_dir + model_dir
        copy_rename_best_model(dir_path, output_name, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("af2_HT_dir", type=str, help="directory with AF2 output folders")
    parser.add_argument("output_name", type=str, help="output pdb name, exclude extension")
    parser.add_argument("--output_dir", type=str, default="best_models")
    args = parser.parse_args()
    main(**vars(args))