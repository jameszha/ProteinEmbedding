# Protein Embeddings

## Introduction
Recent advances of machine learning algorithms and accumulation of large datasets make possible a wide assortment of new predictive tasks in biological and medical settings. In particular, accurate prediction of protein-protein interactions (PPIs) is vital to our understanding of mechanistic pathways within the human body as well as drug design.

However, in order to be analyzed via computational means, proteins must first be embedded into numerical vectors. Recently, the Gene Ontology (GO), a database of biological terms arranged in a hierarchical graph structure, has been considered a potential source of extracting these vector representations of proteins. 

Here, we utilize two natural language processing (NLP) methods to embed proteins into dense vector representations. In the first method, dubbed Onto2Vec4, the structure of the GO graph, with accompanying protein annotations, is described in a series of sentences. Word embeddings of each protein are generated using Word2Vec. In the second method2, sentence embeddings of GO term definitions are inputted into a graph convolutional network (GCN) trained on entailment relationships of GO terms. Protein embeddings are calculated from GO term embeddings taken from the embedding layer. 

## Dependencies
```
Groovy
Perl
Python
```
Python Libraries:
```
gensim
matplotlib
scikit-learn
scipy
numpy
```
## Running the code
- Navigate to the ```scripts/``` directory.
- Change the ```server``` variable within each of the 5 scripts to point to this repository.
- Download the yeast dataset using
```
$ ./download_yeast_datasets.sh
```
- Process the raw data using
```
$ ./process_yeast_datasets.sh
```
- Run Onto2Vec on the yeast data using
```
$ ./run_onto2vec.sh
```
- Evaluate the embeddings in three different tasks using
```
$ ./run_eval_ppi.sh
$ ./run_eval_types.sh
$ ./run_eval_ec.sh
```

## Running code on UCLA's Hoffman2 cluster
Running this code is extremely simple on UCLA's Hoffman2 cluster. Simply clone the repository into your scratch directory. Then, submit each script as a job using
```
qsub <script.sh>
```





