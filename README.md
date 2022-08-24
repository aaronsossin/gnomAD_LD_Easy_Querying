# WORKFLOW

To generate the LD files for a given population (let's say African (afr)) do the following

Note, define population as the shortened form as seen in gnomAD website.
African = afr, Non-finnish european = nfe, Estonian = est, etc...

1. Install the hail package which is leveraged to query and operate on the gnomAD blockmatrices downstream. 

```bash
pip3 install hail
```

2. 

Navigate to hyperparams.py to update some hyper-parameters that the rest of scripts will use. Where this repository is git cloned, 

   1. Update the global_directory_path variable such that the path is 
    
```bash
.../gnomAD_LD_Easy_Querying/
```

   2. Update the "sherlock_partition_string" to account for which partitions you will be using (specific to your lab). For example, I use "qsu,zihuai". One could also use "zihuai" etc. 


3. Download gnomAD files from https://gnomad.broadinstitute.org/downloads

    1. For your population of choice, copy the "LD matrix Hail Block Matrix" file (ends in .bm) google URL. 

    2. navigate terminal to /downloading_data_from_gnomAD/

    3. Download file by running the following from command line:
        $python3 run_download_script.py <pasted_url_from_step1>
    
    4. File will be downloaded in /gnomAD_downloaded_files/ repo

    5. Repeat step 1 but, Copy the "Variant indices hail table" file (ends in .ht) google URL instead. You do not need to wait for the above script to finish - they can be running in parallel

4. First, wait for step 2 to finish. Now we need to define the independent blocks for our population of choice using the paper found here: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4731402/
Moreover, we want to know which independent blocks each hit in our LD matrices belongs to. We thus create one file per chromosome, which contains a 2D list specifying the hits in each independent block (partition)

    1. Navigate terminal to /generating_independent_partitions/ and run $python3 run_retrieve_independent_blocks.py nfe
       where 'nfe' is the population so could be 'afr', etc..
    
    2. Step 1 should result in 22 files inside "gnomAD_LD_Easy_Querying/independent_partitions/nfe/

5. Now, we are ready to generate the LD matrices that will be saved inside gnomAD_LD_Easy_Querying/LD_matrices/nfe where nfe can be your population of choice consistent with the above

    1. Navigate terminal to generating_LD_matrices/ and run:
    $python3 run_populate_LD_matrices.py nfe, again where 'nfe' is changed to the population of choice

## License

Distributed under the ASossin License

<p align="right">(<a href="#readme-top">back to top</a>)</p>





