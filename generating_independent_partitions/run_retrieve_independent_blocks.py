import sys
from gnomAD_LD_Easy_Querying.hyperparams import global_directory_path


""" 
Here we parallelize by chromosome, and retrieve the blocks defined by Beriza and save the block matrix hits within each partition in files
"""

"""
Example command line to run this file:

python3 run_retrieve_independent_blocks.py nfe
"""

script_file_lines = [
    "#!/bin/bash",
    "#SBATCH -p qsu,zihuai",
    "#SBATCH --mem=128G",
    "#SBATCH -n 1",
    "#SBATCH -N 1",
    "#SBATCH --time=02:00:00",
    "#SBATCH -e error_ld.txt",
    "ml python/3.6.1",
    "ml chemistry",
    "ml gromacs",
    "ml java",
    "python3 retrieve_independent_blocks.py"
]
import os

# Must define a population for this script to work
assert len(sys.argv) > 1
pop = sys.argv[1]

for i in range(1,23):
    updated_script = script_file_lines.copy()
    updated_script[-1] = updated_script[-1] + " " + str(i) + " " + str(pop)
    filename = global_directory_path + "batch_script_files/" + str(i) + ".sh"
    textfile = open(filename, "w")
    for element in updated_script:
        textfile.write(element + "\n")
    textfile.close()
    os.system("sbatch " + filename)
