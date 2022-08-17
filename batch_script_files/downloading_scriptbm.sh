#!/bin/bash
#SBATCH -p qsu,zihuai
#SBATCH --mem=128G
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --time=36:00:00
#SBATCH -e error_download.txt
ml python/3.6.1
pip3 install gsutil
gsutil cp -r gs://gcp-public-data--gnomad/release/2.1.1/ld/gnomad.genomes.r2.1.1.asj.common.adj.ld.bm /oak/stanford/groups/zihuai/gnomAD/LD_Scores/gnomAD_LD_Easy_Querying/gnomAD_downloaded_files/
