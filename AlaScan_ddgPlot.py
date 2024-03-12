# Authors: @riverseb
import os 
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# dict for swapping between 3 and 1 letter amino acid codes
aminoacids = {
    "GLY":"G",
    "ALA":"A",
    "VAL":"V",
    "LEU":"L",  
    "ILE":"I",
    "MET":"M",
    "PHE":"F",
    "PRO":"P",
    "SER":"S",
    "THR":"T",
    "CYS":"C",
    "ASN":"N",
    "GLN":"Q",
    "ASP":"D",
    "GLU":"E",
    "TYR":"Y",
    "HIS":"H",
    "LYS":"K",
    "ARG":"R",
    "TRP":"W",
    }
# parse Rosetta log file to extract ddgs
def extract_ddgs(rossetta_log_dir):
    for rossetta_log in [file for file in os.listdir(rossetta_log_dir) if file.endswith(".log")]:    
        with open(os.path.join(rossetta_log_dir, rossetta_log), 'r') as f:
            lines = f.readlines()
        ddgs = {}
        # parse for REPORT lin that contains ddg info
        for line in lines:
            if "REPORT:  Residue" in line:
                line_split = line.strip().split()
                # pull out tested mutation
                mutation = line_split[2]
                # swap 3 letter code to 1 letter
                res_1code = aminoacids[mutation[4:7]]
                # update mutation name
                mut_name = res_1code + mutation[1:4] + "A"
                ddg = line_split[-1]
                # add to dict if not present
                if ddgs.get(mut_name) == None:
                    ddgs[mut_name] = [float(ddg)]
                else:
                    ddgs[mut_name].append(float(ddg))
    avg_ddg_dict = avg_ddgs(ddgs)
    return avg_ddg_dict

# calculate average ddg over all iterations 
def avg_ddgs(ddgs):
    avg_ddgs = {}
    for mutation, ddg_list in ddgs.items():
        avg_ddgs[mutation] = [sum(ddg_list) / len(ddg_list)]
        std_err = np.std(ddg_list) / np.sqrt(len(ddg_list))
        avg_ddgs[mutation].append(std_err)
    return avg_ddgs

# write data file w/ mutations at their associated ddg and std err
def output_ddgs(ddgs, outfile):
    with open(outfile, 'w') as f:
        f.write("Mutation\tAvg_DDG\tStd_Err\n")
        for mutation, ddg_std_err in ddgs.items():
            f.write(f"{mutation}\t{ddg_std_err[0]}\t{ddg_std_err[1]}\n")

def create_dataframe_from_file(file_path):
    df = pd.read_csv(file_path, sep='\t', header=0)
    return df

# plot ddg as bar graph for each mutation using matplotlib
def create_bar_graph(df):
    plt.figure(figsize=(6,4))
    plt.bar(df['Mutation'], df['Avg_DDG'], yerr=df['Std_Err'], capsize=5)
    plt.xlabel('Mutations', fontsize=20)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.ylabel('$\Delta\Delta$G (REU)', fontsize=20)
    plt.title('$\Delta\Delta$G of Alanine Scan', fontsize=20)
    plt.axhline(y=0, color='black', linestyle='--')
    plt.xticks(rotation=90)
    plt.savefig('ddg_plot.png', dpi=300, bbox_inches='tight')

def main(rossetta_log, outfile):
    ddgs = extract_ddgs(rossetta_log)
    output_ddgs(ddgs, outfile)
    df = create_dataframe_from_file(outfile)
    create_bar_graph(df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description= '''This script is designed to extract ddgs from a rosetta log file'''
    )

    parser.add_argument('rossetta_log', help='Path to rosetta log file')
    parser.add_argument('--outfile', default="avg_ddgs.txt", help='Path to output file')
    args = parser.parse_args()

    main(**vars(args))