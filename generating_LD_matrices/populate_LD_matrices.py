import sys
import os
import random
import hail as hl
from hail.linalg import BlockMatrix
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import sys
import struct
import numpy as np
import glob as glob
import pickle

from pathlib import Path
myDir = os.getcwd()
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from hyperparams import global_directory_path,sherlock_partition_string



"""

For a single chromosome, generate the LD matrix files corresponding to pre-defined independent partitions

"""

# Must define chromosome and population
assert len(sys.argv) > 2

# Hyperparam - kept low to avoid memory issues
interval_size = 1500

# Chromosome
chr_ = sys.argv[1]

# Population
pop = sys.argv[2]

"""
To increase parallelization, i found it nice to run two scripts per chromosome where each starts from one end of the chromosome and meets in the middle
This only works since before processing a block, it checks to make sure if the file has already been generated!
"""
start_from_back = False
if len(sys.argv) > 3:
    start_from_back = sys.argv[3]

# Initialize hail
hl.init(min_block_size=128)

bm = BlockMatrix.read(global_directory_path + "gnomAD_downloaded_files/gnomad.genomes.r2.1.1." + pop + ".common.adj.ld.bm")
ht_idx = hl.read_table(global_directory_path + "gnomAD_downloaded_files/gnomad.genomes.r2.1.1." + pop + ".common.adj.ld.variant_indices.ht")
save_dir = global_directory_path + "LD_matrices/" + pop + "/"

# Create sub-directory for saving files if it doesn't exist
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

# Pre-partitioned file loading
partitions = pickle.load(open(global_directory_path + "independent_partitions/" + pop + "/partitions_for_" + str(chr_) + ".pickle","rb"))[str(chr_)]

# Here, we populate our independent block with data from sub-matrix queries
# So, we have two non-overlapping intervals (a,b) & (x,y) where we calculate the LD 
def calculate_sub_matrix_and_populate(chr_, pos_start, pos_end, pos_start_y, pos_end_y):

    # Global variables we keep track of after every function call
    global ht_idx
    global bm
    global complete_matrix
    global info_dict

    # Firsts interval is queried for indices and af/ref/alt
    a = str(chr_) + ":" + str(positions[pos_start]) + "-" + str(positions[pos_end]+1)
    interval = hl.parse_locus_interval(a)
    ht_idx_filtered = ht_idx.filter(interval.contains(ht_idx.locus))

    locus = ht_idx_filtered.locus.collect()
    locis = [l.position for l in locus]
    idx = ht_idx_filtered.idx.collect()
    alleles = ht_idx_filtered.alleles.collect()

    af_structs = ht_idx_filtered.pop_freq.collect()

    #second interval is queried for indices and af/ref/alt
    a = str(chr_) + ":" + str(positions[pos_start_y]) + "-" + str(positions[pos_end_y]+1)
    interval = hl.parse_locus_interval(a)
    ht_idx_filtered_y = ht_idx.filter(interval.contains(ht_idx.locus))

    locus_y = ht_idx_filtered_y.locus.collect()
    locis_y = [l.position for l in locus_y]
    idx_y = ht_idx_filtered_y.idx.collect()
    alleles_y = ht_idx_filtered_y.alleles.collect()
    
    af_structs_y = ht_idx_filtered_y.pop_freq.collect()


    # Combining info taken from the above queries
    refs = list()
    alts = list()
    refs_y = list()
    alts_y = list()
    for ix,a in enumerate(alleles):
        refs.append(alleles[ix][0])
        alts.append(alleles[ix][1])
    for ix, a in enumerate(alleles_y):
        refs_y.append(alleles_y[ix][0])
        alts_y.append(alleles_y[ix][1] )
    
    afs = [float(str(x).split("AF=")[1].split(",")[0]) for x in af_structs]
    afs_y = [float(str(x).split("AF=")[1].split(",")[0]) for x in af_structs_y]

    # GET LD AND SAVE
    bm_filtered = bm.filter(idx, idx_y)
    data = bm_filtered.to_numpy()

    # Save info like ref/alt/af - confusing how this works but it does!
    for ixx,ix in enumerate(range(pos_start,pos_end+1)):
        if not info_dict[ix]:
            info_dict[ix] = [int(locis[ixx]),refs[ixx],alts[ixx],afs[ixx]]
    for ixx,ix in enumerate(range(pos_start_y,pos_end_y+1)):
        if not info_dict[ix]:
            info_dict[ix] = [int(locis_y[ixx]),refs_y[ixx],alts_y[ixx],afs_y[ixx]]

    # Global variable gets updated
    complete_matrix[pos_start:pos_end+1,pos_start_y:pos_end_y+1] = data

# Reverse partition list if we are starting from back
if start_from_back:
    partitions = partitions[::-1]

# For each partition in this chromosome
for ix,i in enumerate(partitions):
    global info_dict # Info_dict represents the other information for each LD score like ref, alt, AF
    global complete_matrix # Complete matrix represents the final LD matrix we are saving at the end
    global positions # Positions represents all the hits within this independent block

    # For each new partition (independent_block), get the positions (with duplicates representing alleles)
    positions = partitions[ix]
    
    # Start and end position
    pos_start = positions[0]
    pos_end = positions[-1]

    # Name of resulting csv file for this independent block
    save_file = save_dir + str(chr_) + "_" + str(pos_start) + "_" + str(pos_end) + ".csv"
    
    # Make sure this file hasn't already been made - and if so skip (relevent for when we start from back and front of chromosome)
    if os.path.exists(save_file):
        print("skipping ",ix)
        continue

    print("Positions in partition: ",len(positions))
    
    # Start by defining the LD matrix as just zeros
    complete_matrix = np.zeros((len(positions),len(positions)))

    # Dictionary for ref + alt + AF
    info_dict = dict()
    for ix in range(len(positions)):
        info_dict[ix] = list()

    # Calculate remainder and then divide indices of partition into groups for querying
    remainder = len(positions) % interval_size
    print("remainder, ", remainder)
    

        
    if len(positions) < interval_size:
        split_indices = [np.array(range(len(positions)))]
    else:
        split_indices = list(np.array_split(range(len(positions))[:-remainder], int(len(range(len(positions))[:-remainder])/interval_size)))
        if remainder != 0:
            split_indices.append(np.array(range(len(positions))[-remainder:]))
        
    # Remove duplicating problem that meant weird sizes would happen. 
    for ix in range(len(split_indices) - 1):
        while positions[split_indices[ix][-1]] == positions[split_indices[ix+1][0]]:
            l = split_indices[ix][-1]
            split_indices[ix] = split_indices[ix][:-1]
            split_indices[ix+1] = np.insert(split_indices[ix+1],0,l)



    pairs_of_splits_indices = [(a.tolist(),b.tolist()) for idx, a in enumerate(split_indices) for b in split_indices[idx + 0:]]
    
    # Diagonal pairs (identity)
    print("#Pairs: ",len(pairs_of_splits_indices))

    # Calculates LD for each pair of intervals
    for pair_from_split in pairs_of_splits_indices:
        p0 = pair_from_split[0]
        p1 = pair_from_split[1]

        calculate_sub_matrix_and_populate(chr_,p0[0],p0[-1],p1[0],p1[-1])
    
    # Nice check to do to make sure diagonal is all 1s
    print("Average diagonal score: ",np.mean([complete_matrix[i,i] for i in range(complete_matrix.shape[0])]))

    # Once calculated - combine saved information into dataframe
    info_df = pd.DataFrame()
    info_df["chr"] = [chr_] * len(positions)
    info_df["pos"] = positions
    for i in range(len(positions)):
        info_df.loc[i,"ref"] = info_dict[i][1]
        info_df.loc[i,"alt"] = info_dict[i][2]
        info_df.loc[i,"AF"] = info_dict[i][3]

    # Dataframe with LD data
    data_df = pd.DataFrame(data=complete_matrix)

    # Concatenating info and LD
    final_df = pd.concat([info_df, data_df], axis=1)

    # Removing duplicate rows from df
    duplicate_entries = final_df.duplicated(subset=["pos","ref","alt"],keep='first')
    duplicate_indices = [x for ix,x in enumerate(final_df.index) if duplicate_entries[ix]]
    final_df = final_df.drop(duplicate_indices)

    # Drop duplicate columns corresponding
    column_duplicate_indices = [x + 5 for x in duplicate_indices]
    columns_to_drop = final_df.columns[column_duplicate_indices]
    final_df = final_df.drop(columns=columns_to_drop)

    # Reset index
    final_df.reset_index(inplace=True,drop=True)

    # Rename columns to include ref and alt
    unique_column_keys = [str(final_df.loc[x,"pos"]) + "_" + str(final_df.loc[x,"ref"]) + "_" + str(final_df.loc[x,"alt"]) for x in range(final_df.shape[0])]
    final_df.columns = ["chr","pos","ref","alt","AF"] + unique_column_keys

    # Display
    print(final_df)
    final_df.to_csv(save_file,sep='\t')

    # Erase global variables before next query
    del info_dict 
    del positions 
    del complete_matrix

print("DONE!")