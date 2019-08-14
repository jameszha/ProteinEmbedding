#!/bin/bash
#$ -cwd
# error = Merged with joblog
#$ -o joblog.process_yeast.$JOB_ID
#$ -j y
#$ -l h_rt=01:00:00,h_data=1G
# Email address to notify
#$ -M $email
# Notify when
#$ -m bea

# Load the job environment:
. /u/local/Modules/default/init/modules.sh
module load python/3.6.1

# Script:
server=$SCRATCH/'ProteinEmbedding'
src_dir=$server/'process_datasets'
data_dir=$server/'datasets/raw/yeast'
out_dir=$server/'datasets/processed/yeast'
emb_dir=$server/'embeddings/yeast'

mkdir -p $out_dir
mkdir -p $emb_dir


# Interleave links so that samples go positive, negative, positive, negative, ...
# Not really necessary. SKLearn's train_test_split() already handles shuffling (and optionally stratification)
python3 $src_dir/'interleave_links.py' $data_dir/'protein.actions.tsv' -o $out_dir/'protein_links.lst'

# Get binary embeddings as a baseline. 
# Also generates intermediate file proteins.lst that is used by get_single_ec_numbers.py
python3 $src_dir/'get_annotations.py' $data_dir/'goa_yeast.gaf' -a $out_dir/'annotations.lst' -p $out_dir/'proteins.lst'
python3 $src_dir/'get_binary_embeddings.py' $out_dir/'annotations.lst' -o $emb_dir/'binary_embeddings.lst'

# Extract EC numbers from enzyme.dat for the proteins in proteins.lst. Only take proteins that belong to a SINGLE
# top-level EC category. 
# Remove --single for multiclass classification.
python3 $src_dir/'get_ec_numbers.py' -e $data_dir/'enzyme.dat' -p $out_dir/'proteins.lst' -o $out_dir/'single_ec_numbers.lst' --single

# Extract interaction types
# Optionally take a random subset, as there are over 400,000 samples
python3 $src_dir/'convert_actions_string_to_uniprot.py' $data_dir/'4932.protein.actions.v11.0.txt' -m $src_dir/'yeast_string_to_uniprot.mapping' -o $out_dir/'all_protein_action_types.lst'
shuf -n 10000 $out_dir/'all_protein_action_types.lst' > $out_dir/'protein_action_types.lst'
