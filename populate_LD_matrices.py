import sys

""" 
Generate LD matrices of every chromosome as batch script with population as command ine argument
"""
pop = sys.argv[1]

script_file_lines = [
    "#!/bin/bash",
    "#SBATCH -p qsu,zihuai",
    "#SBATCH --mem=128G",
    "#SBATCH -n 1",
    "#SBATCH -N 1",
    "#SBATCH --time=06:00:00",
    "#SBATCH -e error_ld.txt",
    "ml python/3.6.1",
    "ml chemistry",
    "ml gromacs",
    "ml java",
    "python3 populate_LD_matrices_Beriza_complete.py"
]
import os
for i in range(1,23):
    updated_script = script_file_lines.copy()
    updated_script[-1] = updated_script[-1] + " " + str(i) + " " + str(pop)
    filename = "/oak/stanford/groups/zihuai/gnomAD/LD_Scores/nearly_independent_Beriza/temp_scripts/po" + str(i) + ".sh"
    updated_script[6] = updated_script[6].replace(".txt",str(i) + ".txt")
    textfile = open(filename, "w")
    for element in updated_script:
        textfile.write(element + "\n")
    textfile.close()
    os.system("sbatch " + filename)
