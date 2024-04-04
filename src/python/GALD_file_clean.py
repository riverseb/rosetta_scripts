## Authors: @riverseb
import os 
import argparse 
import fileinput

def rename_projFiles(project, inputFile, n = 5):
    ### Usage: This function is designed to rename the output files of GALigandDock and consolidate them

    # make scores and pdbs folders
    if not os.path.exists("scores/"):
        os.mkdir("scores/")
    if not os.path.exists("pdbs/"):
        os.mkdir("pdbs/")
    # loop over folders based on number of repeats
    for i in range(0, n):
        index = i + 1
        # generate folder name based on project and index
        folder_name = project + "_" + index.__str__()
        # create new path and filename for score file
        scorefile = '../scores/score_' + index.__str__() + ".sc"
        # change directory into specific repeat folder
        try:
            os.chdir(folder_name)
        except:
            continue
        # check if score file is present or if the score file has been renamed but not moved
        if os.path.exists("score.sc"):
            os.rename("score.sc", scorefile)
        elif os.path.exists(f"score_{index.__str__()}.sc"):
            os.rename(f"score_{index.__str__()}.sc", scorefile)
            os.rename(f"score_{index.__str__()}.sc.bak", f"../scores/score_{index.__str__()}.sc.bak")
        else:
            print("No score file detected in folder " + folder_name)
        # loop over pdb files and rename them based on index
        for x in range(1,21):
            # create new pdb file name based on index and pdb number
            pdbFile = inputFile + "_" + index.__str__() + "_" + x.__str__() + ".pdb"
            # generate the original pdb file names
            if x < 10:
                origFile = inputFile + "_0001_" + "000" + x.__str__()
            else:
                origFile = inputFile + "_0001_" + "00" + x.__str__() 
            # replace the original pdb file names with the new ones in the score file
            if os.path.exists(scorefile):
                with fileinput.FileInput(scorefile, inplace=True, backup='.bak') as file:
                    # loop over lines in the score file
                    for line in file:
                        # replace the original pdb file names with the new ones
                        print(line.replace(origFile, pdbFile), end="")
            # create original pdb file path and new pdb file path and name
            infilename = origFile + ".pdb"
            pdbFilePath =  "../pdbs/" + pdbFile
            # check if the original pdb file is present or if the pdb file has been renamed but not moved
            if os.path.exists(infilename):
                os.rename(infilename, pdbFilePath)
            elif os.path.exists(pdbFile):
                os.rename(pdbFile, pdbFilePath)
        # back out to project folder
        os.chdir('..')
        # delete empty repeat folder
        if not os.listdir(folder_name):
            os.rmdir(folder_name)
        # check if crash log exists and move it to its own folder
        elif "ROSETTA_CRASH.log" in os.listdir(folder_name):
            if not os.path.exists("crash_logs/"):
                os.mkdir("crash_logs/")
            os.rename(f"{folder_name}/ROSETTA_CRASH.log", f"crash_logs/ROSETTA_CRASH_{index.__str__()}.log")
            # delete folder if empty
            if not os.listdir(folder_name):
                os.rmdir(folder_name)
            # print warning if folder is not empty
            else:
                print("WARNING: Failed to clean folder " + folder_name)
    
def combine_scores(scores):
    ### Usage: This function is designed to combine the scores from all repeats    
    if os.path.exists(scores):
        # creates list for all score data
        full_data =[]
        # creates a list of files from specified directory of just score files
        scoreFiles = [file for file in os.listdir(scores) if file.endswith(".sc") and file != "fullscore_sorted.sc"] 
        # changes directory to specified directory
        os.chdir(scores)
        # loop through files
        for file in scoreFiles:
            with open(file, 'r') as input:
                # creates a list of lines from specified file
                lines = [line.strip().split() for line in input.readlines()]
                # splits lines into header and data and throws out first line
                __, header, *data = lines
                # add data to full_data list
                full_data.extend(data)
        # sort data by score
        sorted_data = sorted(full_data, key=lambda x: float(x[1]))
        # write sorted data to file
        with open("fullscore_sorted.sc", 'w', encoding='utf-8') as outfile:
            outfile.seek(0)
            # write header formatted to 20 char columns and remove SCORE: column
            outfile.write("".join("{:<20}".format(x) for x in header if x != "SCORE:") + "\n")
            # write sorted data formatted to 20 char columns and remove SCORE: column
            for row in sorted_data:
                outfile.write("".join("{:<20}".format(s) for s in row if s != "SCORE:") + "\n")
            outfile.truncate()
        os.chdir("..")        
    else:
        raise TypeError("Input is not a directory")

def main(project, inputFile, repeats, scores="scores/"):
    rename_projFiles(project, inputFile, n=repeats)
    combine_scores(scores)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description= '''This script is designed to combine score files and rename
    outputs from replicates of GALigandDock'''
    )

    parser.add_argument('project', help='''Project name''')
    parser.add_argument('inputFile', help='Input structure file name without the extension')
    parser.add_argument('--repeats', type=int, help='Number of repeats of GALigandDock run', default=5)
    parser.add_argument('--scores', default="scores/", help='Path to score files')

    args = parser.parse_args()

    main(**vars(args))