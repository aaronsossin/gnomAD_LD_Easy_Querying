#WORKFLOW

To generate the LD files for a given population (let's say African (afr)) do the following

1. Download gnomAD files from https://gnomad.broadinstitute.org/downloads

    1.
    Copy the "LD matrix Hail Block Matrix" file (ends in .bm) google URL
    Paste URL into downloading_data_from_gnomAD/download_script.sh 
    
    in command line run:
    $sbatch download_script.sh 

    And then wait for file to be downloaded

    2. Repeat step 1 but, Copy the "Variant indices hail table" file (ends in .ht) google URL instead

2. Now we need to define the independent blocks for our population of choice. Moreover, we would like to know which variants inside these blocks are contained within the block matrix files. We thus create one file per chromosome, which contains a 2D list specifying the hits in each independent block (partition)

    1. From command line, run: $python3 .../gnomAD_LD_Easy_Querying/run_retrieve_independent_blocks.py nfe
       where 'nfe' is the population so could be 'afr', etc..
    
    2. Step 1 should result in 22 files inside "gnomAD_LD_Easy_Querying/independent_partitions/nfe/

3. Now, we are to generate the LD matrices that will be saved inside gnomAD_LD_Easy_Querying/LD_matrices/nfe where nfe is replaced by population

    1. $python3 .../gnomAD_LD_Easy_Querying/generating_LD_matrices/run_populate_LD_matrices.py nfe
    



