import sys

""" 
Generate LD matrices of every chromosome as batch script with population as command line argument
To make things go faster, we run two scripts per chromosome, one that starts at beginning and one that starts at end 
so that they meet in the middle (which checks to make sure there are no duplicates created)
"""

# Must define population
assert len(sys.argv) > 1
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
    "python3 populate_LD_matrices.py"
]
import os

# Starting from front

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

# Starting from back

# Don't need to include this, but will make it 2x faster
for i in range(1,23):
    updated_script = script_file_lines.copy()
    updated_script[-1] = updated_script[-1] + " " + str(i) + " " + str(pop) + " " + str(True)
    filename = "/oak/stanford/groups/zihuai/gnomAD/LD_Scores/nearly_independent_Beriza/temp_scripts/po" + str(i) + ".sh"
    updated_script[6] = updated_script[6].replace(".txt",str(i) + ".txt")
    textfile = open(filename, "w")
    for element in updated_script:
        textfile.write(element + "\n")
    textfile.close()
    os.system("sbatch " + filename)