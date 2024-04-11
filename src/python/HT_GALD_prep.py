# Authors: @riverseb
import os 
import pymol.cmd as cmd
from pymol import finish_launching
import argparse
from SLURM_utils import GALD_HT
### Usage: This script is designed to set up GA ligand dock runs in high-throughput
### from empty models and generate shell scripts for SLURM submission.
def align_place_ligs(ref_pdb, query_pdb, ligs, old_ligs=None, output_dir="./"):
    """
    Aligns the reference and query PDB files, creates a new PDB file with 
    aligned ligands, and saves it in the specified output directory.

    Parameters:
    ref_pdb (str): Path to the reference PDB file.
    query_pdb (str): Path to the query PDB file.
    ligs (str): Comma-separated string of ligand names.
    output_dir (str): Output directory for the new PDB file. Defaults to "./".

    Returns:
    None
    """

    cmd.load(ref_pdb, "ref")
    cmd.load(query_pdb, "query")
    cmd.align("ref", "query")
    lig_list = ligs.split(",")
    ligs_name_str = "_".join(lig_list)
    if old_ligs is not None:
        old_lig_list = old_ligs.split(",")
        for old_lig in old_lig_list:
            cmd.extract(f"{old_lig}", f"query and resn {old_lig}")
            cmd.delete(f"{old_lig}")
    for lig in lig_list:
        cmd.select(f"{lig}", f"ref and resn {lig}")
        cmd.create("query", f"query or {lig}")
        cmd.delete(f"{lig}")
    query_name = query_pdb.split("/")[-1].split(".")[0]
    if not os.path.exists(output_dir): os.mkdir(output_dir)
    cmd.save(f"{output_dir}{query_name}_{ligs_name_str}.pdb", "query")
    cmd.delete("ref")
    cmd.delete("query")
def write_shell_script(job_name, temp_script):
    """
    Writes a shell script for SLURM submission.

    Parameters:
    job_name (str): Name of the SLURM job.
    temp_script (str): Path to the template script with code to execute.

    Returns:
    None
    """
    # set up the SLURM settings with SLURM_settings object
    GALD_HT.job_name = job_name
    GALD_HT.logdir = "logs"
    GALD_HT.mail_type = "FAIL"
    # write the SLURM settings
    GALD_HT.write_settings("GALD_noRelax.sh")
    # append executable code from template script
    with open("GALD_noRelax.sh", "a") as f, open(temp_script, "r") as temp:
        
        temp_lines = temp.readlines()
        for line in temp_lines:
            if not line.startswith("#"):
                f.write(line)


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
        # make dir for query if it doesn't exist
        if not os.path.exists(f"{query_name}"): os.mkdir(f"{query_name}")
        os.chdir(f"{query_name}")
        if not os.path.exists(f"{query_name}_{ligs_name_str}"): os.mkdir(f"{query_name}_{ligs_name_str}")
        os.chdir(f"{query_name}_{ligs_name_str}")
        # generate shell script for query
        if write_scripts:
            write_shell_script(f"{query_name}_{ligs_name_str}", 
                            "/nfs/turbo/umms-maom/projects/IMDAase/rosetta/scripts/src/bash/GALD_noRelax.sh")
        if not os.path.exists("logs"): os.mkdir("logs")
        # create starting structure for GA ligand dock
        align_place_ligs(f"../../../{ref_pdb}", f"../../../{query_pdb_dir}{query_pdb}", ligs, old_ligs)
        os.chdir("../..")
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