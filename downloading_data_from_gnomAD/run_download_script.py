import os
import sys
from pathlib import Path
myDir = os.getcwd()
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from hyperparams import global_directory_path,sherlock_partition_string

script_file_lines = [
    "#!/bin/bash",
    "#SBATCH -p " + sherlock_partition_string,
    "#SBATCH --mem=128G",
    "#SBATCH -n 1",
    "#SBATCH -N 1",
    "#SBATCH --time=36:00:00",
    "#SBATCH -e " + global_directory_path + "batch_script_files/error_files/error_download.txt",
    "#SBATCH -o " + global_directory_path + "batch_script_files/output_files/output_download.txt",
    "ml python/3.6.1",
    "pip3 install gsutil",
    "gsutil cp -r XXX " + global_directory_path + "gnomAD_downloaded_files/"
]

assert len(sys.argv) > 1



updated_script = script_file_lines.copy()
updated_script[-1] = updated_script[-1].replace("XXX",sys.argv[1])
filename = global_directory_path + "batch_script_files/downloading_script" + sys.argv[1][-2:] + ".sh"
textfile = open(filename, "w")
for element in updated_script:
    textfile.write(element + "\n")
textfile.close()
os.system("sbatch " + filename)