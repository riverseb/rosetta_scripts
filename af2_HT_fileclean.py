import os 
from shutil import copy
import argparse
def copy_rename_best_model(model_dir, output_name, output_dir):
    if not os.path.exists(output_dir): os.mkdir(output_dir)
    index = model_dir.split("=")[-1]
    try:
        copy(f'{model_dir}/unrelaxed_model_1_pred_0.pdb', f'{output_dir}/{output_name}_{index}.pdb')
    except:
        print("Couldn't find unrelaxed_model_1_pred_0.pdb in " + model_dir)

    # for model in os.listdir(model_dir):
    #     index = model_dir.split("=")[-1]
    #     if model.startswith("relaxed") and model.endswith(".pdb"):
    #         copy(f'{model_dir}/{model}', f'{output_dir}/{output_name}_{index}.pdb')

def main(af2_HT_dir, output_name, output_dir):
   # os.chdir(af2_HT_dir)
    for model_dir in [model_dir for model_dir in os.listdir(af2_HT_dir) if os.path.isdir(f"{af2_HT_dir}{model_dir}")]:
        dir_path = af2_HT_dir + model_dir
        copy_rename_best_model(dir_path, output_name, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("af2_HT_dir", type=str, help="directory with AF2 output folders")
    parser.add_argument("output_name", type=str, help="output pdb name, exclude extension")
    parser.add_argument("--output_dir", type=str, default="best_models")
    args = parser.parse_args()
    main(**vars(args))