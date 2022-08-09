#!/bin/bash
#SBATCH -p qsu,zihuai
#SBATCH --mem=128G
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --time=75:00:00
#SBATCH -e error_please.txt

pip3 install gsutil

gsutil cp -r gs://gcp-public-data--gnomad/release/2.1.1/ld/gnomad.genomes.r2.1.1.nfe.common.adj.ld.bm /oak/stanford/groups/zihuai/gnomAD/LD_Scores/
