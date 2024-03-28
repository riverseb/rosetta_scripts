import os 
import argparse

def name_seq_pairs(uniq_seqs):
    # read uniq_seqs fasta file
    with open(uniq_seqs, "r") as f:
        lines = f.readlines()
    name_seq_pairs = []
    # loop through the top 25% uniq sequences
    for i in range(0, len(lines)//4):
        # first and even lines contain the sequence name
        if i == 0 or i % 2 == 0:
            line_split = lines[i].strip().split()
            name = line_split[0].lstrip(">Sequence")
        # all odd lines contain the sequence
        else:
            seq = lines[i].strip()
            # add name and sequence to list
            name_seq_pairs.append([name, seq])
    return name_seq_pairs
        

def full_seq_gen(native, resnum_list, name_seq_pairs):
    # read native sequence
    with open(native, "r") as f:
        lines = f.readlines()
    # store native sequence
    native_seq = lines[1].strip()
    # get native sequence name
    native_name = native.split("/")[-1].strip(".fasta")
    # loop over top 25% name_seq_pairs
    for name, seq in name_seq_pairs:
        # loop over number of design positions given by user
        for i in range(0, len(resnum_list)):
            # use native sequence as first input
            if i == 0:    
                CM_seq = native_seq[:int(resnum_list[i])] + seq[i] + \
                    native_seq[int(resnum_list[i]) + 1:]
            # add mutations iteratively
            else:
                CM_seq = CM_seq[:int(resnum_list[i])] + seq[i] + \
                    CM_seq[int(resnum_list[i]) + 1:]
        # write out each CM sequence as its own fasta file 
        with open(f"CM_fullfasta/{native_name}_CM_{name}.fasta", "w") as f:
            f.write(f">{native_name}_CM_{name}\n{CM_seq}\n")
def main(native, resnums, uniq_seqs):
    # make output directory if it doesn't exist
    if not os.path.exists("CM_fullfasta"): os.mkdir("CM_fullfasta")
    # create list of design positions from input 
    resnum_list = resnums.split(",")
    name_seqs = name_seq_pairs(uniq_seqs)
    full_seq_gen(native, resnum_list, name_seqs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-native", type=str, required=True, help="native sequence fasta file")
    parser.add_argument("-resnums", type=str, required=True, help="comma separated ordered list of design positions")
    parser.add_argument("-uniq_seqs", type=str, required=True, help="uniq seqs fasta file")
    args = parser.parse_args()
    main(**vars(args))