import sys
from pathlib import Path
myDir = os.getcwd()
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from hyperparams import global_directory_path,sherlock_partition_string





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
    "#SBATCH -p " + sherlock_partition_string,
    "#SBATCH --mem=128G",
    "#SBATCH -n 1",
    "#SBATCH -N 1",
    "#SBATCH --time=06:00:00",
    "#SBATCH -e " + global_directory_path + "batch_script_files/error_files/error_LD.txt",
    "#SBATCH -o " + global_directory_path + "batch_script_files/output_files/output_LD.txt",
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
    filename = global_directory_path + "batch_script_files/" + str(i) + ".sh"
    updated_script[6] = updated_script[6].replace(".txt",str(i) + ".txt")
    updated_script[7] = updated_script[7].replace(".txt",str(i) + ".txt")
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
    filename = global_directory_path + "batch_script_files/" + str(i) + ".sh"
    updated_script[6] = updated_script[6].replace(".txt",str(i) + ".txt")
    updated_script[7] = updated_script[7].replace(".txt",str(i) + ".txt")
    textfile = open(filename, "w")
    for element in updated_script:
        textfile.write(element + "\n")
    textfile.close()
    os.system("sbatch " + filename)