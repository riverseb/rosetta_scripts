#Authors: @riverseb
import sys
import logomaker
import argparse
import matplotlib.pyplot as plt

def create_matrix(seq_aln_file):
    """
    Creates a logomaker matrix from an alignment file
    :param seq_aln_file: alignment file
    :return: matrix
    """
    with open(seq_aln_file, "r") as input:
        seqs = [x.strip() for x in input.readlines() if not x.startswith(">")]
    seq_matrix = logomaker.alignment_to_matrix(seqs, to_type="probability")
    return seq_matrix

def create_export_logo(matrix):
    """
    Generates and saves sequence logo image
    :param matrix: logomaker matrix
    """
    logo = logomaker.Logo(df=matrix, color_scheme="chemistry", stack_order="small_on_top",
                          vpad=0.01)
    logo.fig.savefig('logo.png', dpi=300)

def main(seq_aln_file):
    seq_matrix = create_matrix(seq_aln_file)
    create_export_logo(seq_matrix)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    main(sys.argv[1])
