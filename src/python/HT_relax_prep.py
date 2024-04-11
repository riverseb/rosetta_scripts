from HT_GALD_prep import align_place_ligs
import os
from pymol import finish_launching
import argparse
def main(ref_pdb, query_pdb_dir, ligs, project_dir, old_ligs=None, write_scripts=False):
    finish_launching(['pymol', '-qc'])
    # make project dir if it doesn't exist
    if not os.path.exists(project_dir): os.mkdir(project_dir)
    os.chdir(project_dir)
    lig_list = ligs.split(",")
    ligs_name_str = "_".join(lig_list)
    # loop over query PDB files in the query_pdb_dir
    for query_pdb in [pdbFile for pdbFile in os.listdir(f"../{query_pdb_dir}") if pdbFile.endswith(".pdb")]:
        query_name = query_pdb.split("/")[-1].split(".")[0]
        # create starting structure for GA ligand dock
        align_place_ligs(f"../{ref_pdb}", f"../{query_pdb_dir}{query_pdb}", ligs, old_ligs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ref_pdb", type=str, help="reference pdb file")
    parser.add_argument("query_pdb_dir", type=str, help="directory containing query pdb files")
    parser.add_argument("ligs", type=str, help="ligands to place")
    parser.add_argument("--old_ligs", type=str, help="ligands to remove")
    parser.add_argument("project_dir", type=str)
    parser.add_argument("--write_scripts", action="store_true")
    args = parser.parse_args()
    main(**vars(args))