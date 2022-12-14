import sys
import os
import random
import hail as hl
from hail.linalg import BlockMatrix
import pandas as pd
import sys
import struct
import numpy as np
import os
import math
from pathlib import Path
myDir = os.getcwd()
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from hyperparams import global_directory_path,sherlock_partition_string


"""
For a single chromosome, find the independent blocks defined 
by Beriza, use the variant indices gnomAD file to find hits 
within that independent block, and save the positions of said 
hits in a file for use downstream
*** NOTE: There are more populations defined by gnomAD, then the nearly independent blocks were calculated for. 
There are only "AFR", "EUR", "ASN" defined independent blocks. This is recognized as a source of error and we choose the 
closest option. So, depending on gnomAD population, we will pick one of those three. 
Further research might be warranted into how dissimilar blocks are across populations and quantifying how large this error is. 
My ~guess~ is that independent blocks will generally be conserved but i'm not sure
"""
# Initialize Hail Backend
hl.init()

# Default chromosome 
chr_ = 1

# Command line argument defines chromosome
if len(sys.argv) >= 2:
    chr_ = sys.argv[1]

# Default population
pop = "nfe"

if len(sys.argv) >= 3:
    pop = sys.argv[2]

# Depending on population, load different block matrix and variant indices hail, define different save location, etc..
bm = BlockMatrix.read(global_directory_path + "gnomAD_downloaded_files/gnomad.genomes.r2.1.1." + pop + ".common.adj.ld.bm")
ht_idx = hl.read_table(global_directory_path + "gnomAD_downloaded_files/gnomad.genomes.r2.1.1." + pop + ".common.adj.ld.variant_indices.ht")
save_dir = global_directory_path + "independent_partitions/" + pop + "/"

if pop == "afr":
    beriza_defined_population_name = "afr"
elif pop == "nfe" or pop == "asj" or pop == "amr" or pop == "fin" or pop == "est" or pop == "nwe" or pop == "seu":
    beriza_defined_population_name = "eur"
else:
     beriza_defined_population_name = "asn"

partitions_dict = dict()

# Load file which contains independent block information
beriza_chromsome_and_population_partition_file = global_directory_path + "generating_independent_partitions/ldetect-data/" + pop.upper() + "/fourier_ls-chr" + str(chr_) + ".bed"
beriza_chromsome_and_population_partition_file_df = pd.read_csv(beriza_chromsome_and_population_partition_file,sep='\t')
beriza_chromsome_and_population_partition_file_df.columns = ["chr","start","stop"]

# 2D list: ( (positions_in_block_1) , (positions_in_block_2), ...)
partitions = list()

# Each row in Beriza files correspond to one "independent block"
for ix,row in beriza_chromsome_and_population_partition_file_df.iterrows():

    # Get bp interval of block
    start, end = row["start"], row["stop"]
    
    # Define interval (importantly, with end+1)
    a = str(chr_) + ":" + str(start) + "-" + str(end+1)

    # Convert interval from type: <string> to type <hail?>
    interval = hl.parse_locus_interval(a)

    # Find idx in block matrix corresponding to that interval
    ht_idx_filtered = ht_idx.filter(interval.contains(ht_idx.locus))
    
    # Find which loci correspond to those indices
    locus = ht_idx_filtered.locus.collect()

    # Save the locations (no allele information for now) pertaining to locations within a particular patition
    locus = np.array(locus)
    locis = np.array([l.position for l in locus])
    partitions.append(list(locis))


partitions_dict[chr_] = partitions

# Make subdirectory if doesn't exist for saving
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

# Saving partition info into folder for use in next script
import pickle

with open(save_dir + "partitions_for_" + str(chr_) + ".pickle","wb") as f:
    pickle.dump(partitions_dict,f)

