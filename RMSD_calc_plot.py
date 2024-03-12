import argparse
import calcRMSD_atomSubset as calcRMSD
import rmsd_vs_score as rmsd_plot

def main(ref_pdb, query_pdb_dir, ref_ligand, query_ligand):
    calcRMSD.main(ref_pdb, query_pdb_dir, ref_ligand, query_ligand)
    ref_name = ref_pdb.split("/")[-1].split(".")[0]
    rmsd_plot.main(f"scores/rmsd_scores_{ref_name}.txt", ref_name)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("ref_pdb", type=str, help="reference pdb file")
    parser.add_argument("query_pdb_dir", type=str, help="directory containing query pdb files")
    parser.add_argument("ref_ligand", type=str, help="reference ligand 3 letter code")
    parser.add_argument("query_ligand", type=str, help="query ligand 3 letter code")
    args = parser.parse_args()
    main(**vars(args))