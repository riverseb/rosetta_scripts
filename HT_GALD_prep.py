import os 
import pymol.cmd as cmd
from pymol import finish_launching
import argparse
from SLURM_utils import GALD_HT

def align_place_ligs(ref_pdb, query_pdb, ligs, output_dir="./"):
    cmd.load(ref_pdb, "ref")
    cmd.load(query_pdb, "query")
    cmd.align("ref", "query")
    lig_list = ligs.split(",")
    ligs_name_str = "_".join(lig_list)
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
    GALD_HT.job_name = job_name
    GALD_HT.logdir = "logs"
    GALD_HT.mail_type = "FAIL"
    GALD_HT.write_settings("GALD.sh")
    with open("GALD.sh", "a") as f, open(temp_script, "r") as temp:
        
        temp_lines = temp.readlines()
        for line in temp_lines:
            if not line.startswith("#"):
                f.write(line)


def main(ref_pdb, query_pdb_dir, ligs, project_dir):
    finish_launching(['pymol', '-qc'])
    if not os.path.exists(project_dir): os.mkdir(project_dir)
    os.chdir(project_dir)
    lig_list = ligs.split(",")
    ligs_name_str = "_".join(lig_list)
    for query_pdb in [pdbFile for pdbFile in os.listdir(f"{query_pdb_dir}") if pdbFile.endswith(".pdb")]:
        query_name = query_pdb.split("/")[-1].split(".")[0]
        # query_index = query_name.split("_")[-1]
        if not os.path.exists(f"{query_name}_{ligs_name_str}"): os.mkdir(f"{query_name}_{ligs_name_str}")
        os.chdir(f"{query_name}_{ligs_name_str}")
        write_shell_script(f"{query_name}_{ligs_name_str}", 
                           "/nfs/turbo/umms-maom/projects/IMDAase/rosetta/GALD.sh")
        if not os.path.exists("logs"): os.mkdir("logs")
        align_place_ligs(f"../../{ref_pdb}", f"{query_pdb_dir}{query_pdb}", ligs)
        os.chdir("..")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ref_pdb", type=str, help="reference pdb file")
    parser.add_argument("query_pdb_dir", type=str, help="directory containing query pdb files")
    parser.add_argument("ligs", type=str, help="ligands to place")
    parser.add_argument("project_dir", type=str)
    args = parser.parse_args()
    main(**vars(args))