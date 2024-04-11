import os 
import argparse
def main(project_dir, array_id, account="davidhs1"):
    os.chdir(project_dir)
    dir_list = [dir for dir in os.listdir() if os.path.isdir(dir)]
    sorted_dir_list = sorted(dir_list)
    os.chdir(f"{sorted_dir_list[int(array_id) - 1]}/{sorted_dir_list[int(array_id) - 1]}_PC2")
    os.system(f"sbatch --account={account} GALD_noRelax.sh *.pdb")
    os.chdir(f"../{sorted_dir_list[int(array_id) - 1]}_PM7")
    os.system(f"sbatch --account={account} GALD_noRelax.sh *.pdb")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    parser.add_argument("array_id")
    parser.add_argument("--account", default="davidhs1")
    args = parser.parse_args()
    main(args.project_dir, args.array_id, args.account)