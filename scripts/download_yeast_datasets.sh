#!/bin/bash
#$ -cwd
# error = Merged with joblog
#$ -o joblog.download_yeast.$JOB_ID
#$ -j y
#$ -l h_rt=00:10:00,h_data=1G
# Email address to notify
#$ -M $email
# Notify when
#$ -m bea

# Script:
server=$SCRATCH/'ProteinEmbedding'
out_dir=$server/'datasets/raw/yeast'
mkdir -p $out_dir

# Chelsea and Muhao's protein link dataset
wget https://raw.githubusercontent.com/muhaochen/seq_ppi/master/yeast/preprocessed/protein.actions.tsv -O $out_dir/'protein.actions.tsv'

# Interaction types for protein links from STRING database
wget https://stringdb-static.org/download/protein.actions.v11.0/4932.protein.actions.v11.0.txt.gz -O $out_dir/'4932.protein.actions.v11.0.txt.gz'

# Scored links between proteins from STRING database
# Not needed. Use Chelsea and Muhao's protein link dataset instead
# wget https://stringdb-static.org/download/protein.links.v11.0/4932.protein.links.v11.0.txt.gz -O $out_dir/'4932.protein.links.v11.0.txt.gz'

# Gene annotations from UniProt-GOA database
wget ftp://ftp.ebi.ac.uk:21/pub/databases/GO/goa/YEAST/goa_yeast.gaf.gz -O $out_dir/'goa_yeast.gaf.gz'

# Enzyme commision numbers from Expasy database
wget ftp://ftp.expasy.org/databases/enzyme/enzyme.dat -O $out_dir/'enzyme.dat'

gunzip -f $out_dir/'4932.protein.actions.v11.0.txt.gz'
# gunzip -f $out_dir/'4932.protein.links.v11.0.txt.gz'
gunzip -f $out_dir/'goa_yeast.gaf.gz'