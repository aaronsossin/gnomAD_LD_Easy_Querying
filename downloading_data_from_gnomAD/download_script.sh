#!/bin/bash
#SBATCH -p qsu,zihuai
#SBATCH --mem=128G
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --time=75:00:00
#SBATCH -e error_downloading_script.txt

pip3 install gsutil

gsutil cp -r gs://gcp-public-data--gnomad/release/2.1.1/ld/gnomad.genomes.r2.1.1.nfe.common.adj.ld.variant_indices.ht /oak/stanford/groups/zihuai/gnomAD/LD_Scores/gnomAD_LD_Easy_Querying/gnomAD_downloaded_files/
