#!/bin/bash
#$ -cwd
# error = Merged with joblog
#$ -o joblog.eval_types.$JOB_ID
#$ -j y
#$ -pe shared 4
#$ -l h_rt=24:00:00,h_data=16G
# Email address to notify
#$ -M $email
# Notify when
#$ -m bea

# Load the job environment:
. /u/local/Modules/default/init/modules.sh

module load python/3.6.1


# Script:
server=$SCRATCH
data_dir=$server/'datasets/processed/yeast'
emb_dir=$server/'embeddings/yeast'

src_dir=$server/'evaluate_types'
work_dir=$src_dir/'work'
out_dir=$src_dir/'output'
mkdir -p $out_dir
mkdir -p $work_dir
cd $work_dir

# Generate type embeddings in SVM Light format
if [ -f $work_dir/'types_embeddings_binary.dat' ]; then echo "Binary embeddings found"
else python3 $src_dir/'get_types_embeddings.py' $data_dir/'protein_action_types.lst' $emb_dir/'binary_embeddings.lst' $work_dir/'types_embeddings_binary.dat'
fi

if [ -f $work_dir/'types_embeddings_onto2vec_parents.dat' ]; then echo "Onto2Vec Parent embeddings found"
else python3 $src_dir/'get_types_embeddings.py' $data_dir/'protein_action_types.lst' $emb_dir/'onto2vec_embeddings_parents.lst' $work_dir/'types_embeddings_onto2vec_parents.dat'
fi

if [ -f $work_dir/'types_embeddings_onto2vec_ancestors.dat' ]; then echo "Onto2Vec Ancestor embeddings found"
else python3 $src_dir/'get_types_embeddings.py' $data_dir/'protein_action_types.lst' $emb_dir/'onto2vec_embeddings_ancestors.lst' $work_dir/'types_embeddings_onto2vec_ancestors.dat'
fi

if [ -f $work_dir/'types_embeddings_onto2vec_none.dat' ]; then echo "Onto2Vec No-Ancestor embeddings found"
else python3 $src_dir/'get_types_embeddings.py' $data_dir/'protein_action_types.lst' $emb_dir/'onto2vec_embeddings_none.lst' $work_dir/'types_embeddings_onto2vec_none.dat'
fi

if [ -f $work_dir/'types_embeddings_onto2vec_sum.dat' ]; then echo "Onto2Vec Sum embeddings found"
else python3 $src_dir/'get_types_embeddings.py' $data_dir/'protein_action_types.lst' $emb_dir/'onto2vec_embeddings_sum.lst' $work_dir/'types_embeddings_onto2vec_sum.dat'
fi

if [ -f $work_dir/'types_embeddings_onto2vec_mean.dat' ]; then echo "Onto2Vec Mean embeddings found"
else python3 $src_dir/'get_types_embeddings.py' $data_dir/'protein_action_types.lst' $emb_dir/'onto2vec_embeddings_mean.lst' $work_dir/'types_embeddings_onto2vec_mean.dat'
fi

if [ -f $work_dir/'types_embeddings_dat_sum.dat' ]; then echo "Dat's Sum embeddings found"
else python3 $src_dir/'get_types_embeddings.py' $data_dir/'protein_action_types.lst' $emb_dir/'dat_embeddings_sum.lst' $work_dir/'types_embeddings_dat_sum.dat'
fi

if [ -f $work_dir/'types_embeddings_dat_mean.dat' ]; then echo "Dat's Mean embeddings found"
else python3 $src_dir/'get_types_embeddings.py' $data_dir/'protein_action_types.lst' $emb_dir/'dat_embeddings_mean.lst' $work_dir/'types_embeddings_dat_mean.dat'
fi

# echo =============== Binary =====================
# OMP_NUM_THREADS=4 python3 -u $src_dir/evaluate_embeddings.py $work_dir/types_embeddings_binary.dat | tee $out_dir/output_binary.txt

# echo =============== Parents ====================
# OMP_NUM_THREADS=4 python3 -u $src_dir/evaluate_embeddings.py $work_dir/types_embeddings_onto2vec_parents.dat | tee $out_dir/output_parents.txt

# echo =============== Ancestors ==================
# OMP_NUM_THREADS=4 python3 -u $src_dir/evaluate_embeddings.py $work_dir/types_embeddings_onto2vec_ancestors.dat | tee $out_dir/output_ancestors.txt

# echo =============== None =======================
# OMP_NUM_THREADS=4 python3 -u $src_dir/evaluate_embeddings.py $work_dir/types_embeddings_onto2vec_none.dat | tee $out_dir/output_none.txt

# echo =============== Sum =======================
# OMP_NUM_THREADS=4 python3 -u $src_dir/evaluate_embeddings.py $work_dir/types_embeddings_onto2vec_sum.dat | tee $out_dir/output_sum.txt

# echo =============== Mean =======================
# OMP_NUM_THREADS=4 python3 -u $src_dir/evaluate_embeddings.py $work_dir/types_embeddings_onto2vec_mean.dat | tee $out_dir/output_mean.txt

echo =============== Dat Sum =======================
OMP_NUM_THREADS=4 python3 -u $src_dir/evaluate_embeddings.py $work_dir/types_embeddings_dat_sum.dat | tee $out_dir/output_dat_sum.txt

echo =============== Dat Mean =======================
OMP_NUM_THREADS=4 python3 -u $src_dir/evaluate_embeddings.py $work_dir/types_embeddings_dat_mean.dat | tee $out_dir/output_dat_mean.txt