from gnomAD_LD_Easy_Querying.hyperparams import global_directory_path,sherlock_partition_string

script_file_lines = [
    "#!/bin/bash",
    "#SBATCH -p " + sherlock_partition_string,
    "#SBATCH --mem=128G",
    "#SBATCH -n 1",
    "#SBATCH -N 1",
    "#SBATCH --time=36:00:00",
    "#SBATCH -e error_download.txt",
    "ml python/3.6.1",
    "pip3 install gsutil",
    "gsutil cp -r XXX /oak/stanford/groups/zihuai/gnomAD/LD_Scores/gnomAD_LD_Easy_Querying/gnomAD_downloaded_files/"
]
import os
import sys

assert len(sys.argv) > 1



updated_script = script_file_lines.copy()
updated_script[-1] = updated_script[-1].replace("XXX",sys.argv[1])
filename = global_directory_path + "batch_script_files/downloading_script" + sys.argv[1][-2:] + ".sh"
textfile = open(filename, "w")
for element in updated_script:
    textfile.write(element + "\n")
textfile.close()
os.system("sbatch " + filename)