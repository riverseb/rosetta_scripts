## Authors: @riverseb
import os
import pandas as pd
import rdkit.Chem as rd
import rdkit.Chem.rdMolAlign as rdMolAlign
from rdkit.Chem import AllChem
from pymol import cmd, finish_launching

# align query pdb to reference over the whole reference pdb using pymol
def align_pdbs(ref_pdb, query_pdb):
    cmd.load(ref_pdb, "ref")
    cmd.load(query_pdb, "query")
    cmd.align("ref", "query")
    cmd.save("aligned_ref.pdb", "ref")    
    cmd.delete("query")
    cmd.delete("ref")
    aligned_ref_pdb = "aligned_ref.pdb"
    return aligned_ref_pdb
def extract_and_save_query_ligand(query_pdb, query_ligand, index):
    """Load and extract ligands from pdb files using PyMOL.

    :param query_pdb: query pdb file
    :param query_ligand: query ligand
    """
    # load the query pdb
    cmd.load(query_pdb, "query")

    # select and extract the query ligand
    cmd.select("query_ligand", f"query and resn {query_ligand}")
    # cmd.extract("query_ligand_ext", "query_ligand")
    if not os.path.exists("docked_ligands/"): os.mkdir("docked_ligands/")
    cmd.save(f"docked_ligands/{query_ligand}_{index}.mol2", "query_ligand")
    cmd.delete("query")
    cmd.delete("query_ligand")

def extract_and_save_ref_ligand(aligned_ref_pdb, ref_ligand):
    """Load and extract ligands from pdb files using PyMOL.

    :param ref_pdb: reference pdb file
    :param ref_ligand: reference ligand
    """
    # load the reference pdb
    cmd.load(aligned_ref_pdb, "ref")

    # select and extract the reference ligand
    cmd.select("ref_ligand", f"ref and resn {ref_ligand}")
    cmd.extract("ref_ligand", "ref_ligand")
    # save the reference ligand as an sdf file
    cmd.save(f"aligned_{ref_ligand}.mol2", "ref_ligand")
    cmd.delete("ref")
    cmd.delete("ref_ligand")

def calc_rmsd_atomSubset(aligned_ref_ligand, query_ligand):
    """Calculate RMSD between two ligands using PyMOL and RDkit. Performs substructure
    matching between the reference ligand and the query ligand.

    :param ref_ligand: aligned reference ligand pdb file
    :param query_ligand: query ligand pdb file
    """
    # load the reference ligand
    ref_mol = rd.rdmolfiles.MolFromMol2File(aligned_ref_ligand)
    query_mol = rd.rdmolfiles.MolFromMol2File(query_ligand)
    ref_match = ref_mol.GetSubstructMatch(query_mol)
    query_match = query_mol.GetSubstructMatch(ref_mol)
    rmsd = AllChem.CalcRMS(ref_mol, query_mol, map=[list(zip(query_match , ref_match))]) 
    return rmsd

def main(ref_pdb, query_pdb_dir, ref_ligand, query_ligand):
    finish_launching(['pymol', '-qc'])
    # create list of query pdbs
    query_pdbs = [pdbFile for pdbFile in os.listdir(query_pdb_dir) if pdbFile.endswith(".pdb")]
    # align and save reference pdb
    aligned_ref_pdb = align_pdbs(ref_pdb, f"{query_pdb_dir}{query_pdbs[0]}")
    # extract and save reference ligand
    extract_and_save_ref_ligand(aligned_ref_pdb, ref_ligand)
    
    if not os.path.exists("scores/"): os.mkdir("scores/")
    ref_name = ref_pdb.split("/")[-1].split(".")[0]
    # create rmsd vs score table for each query ligand
    with open(f"scores/rmsd_scores_{ref_name}.txt", "w") as out:
        out.write("rmsd\tquery_ligand\tdescription\n")
        rmsd_table = []
        # loop over query pdbs
        for query in query_pdbs:
            query_pdb = query_pdb_dir + query
            index_list = query.split(".")[0].split("_")[-2:]
            index = "_".join(index_list)
            # extract and save query ligand
            extract_and_save_query_ligand(query_pdb, query_ligand, index)
            # calculate rmsd
            rmsd = calc_rmsd_atomSubset(f"aligned_{ref_ligand}.mol2", f"docked_ligands/{query_ligand}_{index}.mol2")
            # add to rmsd table
            rmsd_table.append([rmsd, query_ligand, query])
        # sort by rmsd
        sorted_rmsd_table = sorted(rmsd_table, key=lambda x: float(x[0]))
        # write out rmsd vs score table
        for entry in sorted_rmsd_table:
            out.write(f"{entry[0]}\t{entry[1]}\t{entry[2]}\n")
    cmd.quit()
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("ref_pdb", type=str, help="reference pdb file")
    parser.add_argument("query_pdb_dir", type=str, help="directory containing query pdb files")
    parser.add_argument("ref_ligand", type=str, help="reference ligand 3 letter code")
    parser.add_argument("query_ligand", type=str, help="query ligand 3 letter code")
    args = parser.parse_args()
    main(**vars(args))
