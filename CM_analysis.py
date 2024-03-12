import argparse
from collections import defaultdict
import os
from seq_logo import main as seq_logo_main
def organize_CM_files(cm_dir):
    fasta_dir = os.path.join(cm_dir, "fastas/")
    pdb_dir = os.path.join(cm_dir, "pdbs/")
    stats_dir = os.path.join(cm_dir, "stats/")
    if not os.path.exists(os.path.join(cm_dir, "fastas")):
        os.mkdir(fasta_dir)
    if not os.path.exists(os.path.join(cm_dir, "pdbs")):
        os.mkdir(pdb_dir)
    if not os.path.exists(os.path.join(cm_dir, "stats")):
        os.mkdir(stats_dir)
    for file in os.listdir(cm_dir):
        if file.endswith(".fasta"):
            os.rename(os.path.join(cm_dir, file), os.path.join(fasta_dir, file))
        elif file.endswith(".pdb"):
            os.rename(os.path.join(cm_dir, file), os.path.join(pdb_dir, file))
        elif file.endswith(".stats"):
            os.rename(os.path.join(cm_dir, file), os.path.join(stats_dir, file))

def unique_CM_seqs(cm_fasta_dir):
    seqDict = defaultdict(list)
    # loop through files in the directory
    for file in os.listdir(cm_fasta_dir):
        # if the file is a fasta file, open it and check sequences
        if file.endswith(".fasta"):
            # get the index for CM iteration
            index = file.split(".")[0][-5:]
            with open(os.path.join(cm_fasta_dir, file), 'r') as f:
                lines = f.readlines()
                # loop through the lines, even numbers are ids + scores, odd numbers are sequences
                for i in range(0, len(lines), 2):
                    # get the sequence
                    fastaSeq = lines[i+1].strip()
                     # get the id and score
                    id, score = lines[i].strip().split()
                    # add index to id
                    id_index = id + index
                    # check if sequence is in the dict or if the current ID has a lower score
                    if (fastaSeq in seqDict and float(score) < float(seqDict[fastaSeq][1])) or fastaSeq not in seqDict:
                        # update the dict
                        seqDict[fastaSeq] = [id_index, score]
    sortedDict = sorted(seqDict.items(), key=lambda x: float(x[1][1]))
    return sortedDict

def write_unique_CM_seqs(sortedDict, out_file):
    
    with open(out_file, 'w') as out:
        for key, value in sortedDict:
            out.write(f"{value[0]} {value[1]}\n{key}\n")

def write_top25_CM_seqs(sortedDict, out_file):
    with open(out_file, 'w') as out:
        cutoff = len(sortedDict)//4 
        for key, value in sortedDict[:cutoff]:
            out.write(f"{value[0]} {value[1]}\n{key}\n")

def main(cm_dir, out_file="unique_CM_seqs.fasta"):
    organize_CM_files(cm_dir)
    seqDict = unique_CM_seqs(os.path.join(cm_dir, "fastas"))
    write_unique_CM_seqs(seqDict, f"{cm_dir}{out_file}")
    write_top25_CM_seqs(seqDict, f"{cm_dir}top25_{out_file}")
    seq_logo_main(f"{cm_dir}top25_{out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cm_dir", type=str, help="Directory with coupledmoves results")
    parser.add_argument("--out_file", type=str, default="unique_CM_seqs.fasta", help="Output file name")
    args = parser.parse_args()
    main(args.cm_dir, args.out_file)
