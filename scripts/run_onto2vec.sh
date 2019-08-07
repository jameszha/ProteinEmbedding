#!/bin/bash
#$ -cwd
# error = Merged with joblog
#$ -o joblog.run_onto2vec.$JOB_ID
#$ -j y
#$ -pe shared 4
#$ -l h_rt=1:00:00,h_data=16G
# Email address to notify
#$ -M $email
# Notify when
#$ -m bea

# Load the job environment:
. /u/local/Modules/default/init/modules.sh

module load python/3.6.1
module load java
module load perl

# Script:
server=$SCRATCH
src_dir=$server/'onto2vec'
data_dir=$server/'datasets/raw/yeast'
work_dir=$src_dir/'work'
out_dir=$server/'embeddings/yeast'

mkdir -p $work_dir
mkdir -p $out_dir

cd $work_dir

# Download and process go.own into axioms
if [ -f $work_dir/'classes.lst' ] && [ -f $work_dir/'axioms.lst' ]; then echo "axioms.lst and classes.lst found"
else 
    curl -s get.sdkman.io | bash
    source "$HOME/.sdkman/bin/sdkman-init.sh"
    sdk install groovy
    groovy $src_dir/'OntoProcess.groovy'
fi

# Load all annotations from gaf file.
rm annotationAxiom.lst
perl $src_dir/getAnnotations.pl $data_dir/'goa_yeast.gaf'

# Here, we feed all the protein annotations through getClasses.pl.
# This will generate a list of all proteins that have GO annotations
rm AllClasses.lst
cp annotationAxiom.lst AllAxioms.lst
perl $src_dir/getClasses.pl

# Propagate annotations up the GO tree
python3 $src_dir/add_parents.py
python3 $src_dir/add_ancestors.py

# Generate word2vec embeddings for annotations with parents
cat axioms.lst annotationAxiom_parents.lst > AllAxioms.lst
python3 $src_dir/'runWord2Vec.py'
cp VecResults.lst $out_dir/'onto2vec_embeddings_parents.lst'

# Generate word2vec embeddings for annotations with ancestors
cat axioms.lst annotationAxiom_ancestors.lst > AllAxioms.lst
python3 $src_dir/'runWord2Vec.py'
cp VecResults.lst $out_dir/'onto2vec_embeddings_ancestors.lst'

# Generate word2vec embeddings for annotations with no propagation
cat axioms.lst annotationAxiom.lst > AllAxioms.lst
python3 $src_dir/'runWord2Vec.py'
cp VecResults.lst $out_dir/'onto2vec_embeddings_none.lst'



# Generate GO term embeddings, without protein information
rm AllClasses.lst
cp axioms.lst AllAxioms.lst
perl $src_dir/getClasses.pl
python3 $src_dir/'runWord2Vec.py'
cp VecResults.lst $out_dir/'onto2vec_class_embeddings.lst'

# Generate Sum and Mean embeddings based on classes to which proteins are annotated
python3 $src_dir/'get_sum_mean_embeddings.py' $out_dir/'onto2vec_class_embeddings.lst' 'annotationAxiom.lst' $out_dir/'onto2vec_embeddings_sum.lst' $out_dir/'onto2vec_embeddings_mean.lst'
python3 $src_dir/'get_sum_mean_embeddings.py' $out_dir/'dat_class_embeddings_avepool_cosine.lst' 'annotationAxiom.lst' $out_dir/'dat_embeddings_sum.lst' $out_dir/'dat_embeddings_mean.lst'
