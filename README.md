# Protein Embeddings

## Introduction
Recent advances of machine learning algorithms and accumulation of large datasets make possible a wide assortment of new predictive tasks in biological and medical settings. In particular, accurate prediction of protein-protein interactions (PPIs) is vital to our understanding of mechanistic pathways within the human body as well as drug design.

However, in order to be analyzed via computational means, proteins must first be embedded into numerical vectors. Recently, the Gene Ontology (GO), a database of biological terms arranged in a hierarchical graph structure, has been considered a potential source of extracting these vector representations of proteins. 

Here, we utilize two natural language processing (NLP) methods to embed proteins into dense vector representations. In the first method, dubbed Onto2Vec, the structure of the GO graph, with accompanying protein annotations, is described in a series of sentences. Word embeddings of each protein are generated using Word2Vec. In the second method, sentence embeddings of GO term definitions are inputted into a graph convolutional network (GCN) trained on entailment relationships of GO terms. Protein embeddings are calculated from GO term embeddings taken from the embedding layer. 

## Table of contents
<!--ts-->
   * [Dependencies](#dependencies)
   * [Running the code](#running)
      * [Running code on UCLA's Hoffman2 cluster](#hoffman)
   * [Dat Duong's GO term embeddings](#dat)
   * [Onto2Vec](#onto2vec)
      * [Changes to Onto2Vec pipeline](#changes)
   * [Options for evaluate_embeddings.py](#evaluate)
<!--te-->

<a name="dependencies"></a>
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

<a name="running"></a>
## Running the code
- Navigate to the ```scripts/``` directory.
- Change the ```server``` variable within each of the 6 scripts to point to this repository.
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

<a name="hoffman"></a>
### Running code on UCLA's Hoffman2 cluster
Running this code is extremely simple on UCLA's Hoffman2 cluster. Simply clone the repository into your scratch directory. Then, submit each script (in the order specified above) as a job using
```
qsub <script.sh>
```
The computing resources required per job are already built into each of the scripts. 

<a name="dat"></a>
## Dat Duong's GCN embeddings
One of the methods explored utilized Dat Duong's (Department of Computer Science, UCLA) sentence embedding GCN method. Due to the immensely high overhead (30 minutes per epoch) of generating the class embeddings via this method, the embeddings have been provided. You can download them from:

https://drive.google.com/open?id=1wjgatOZYlzMxtkOsA_neeN8_ZmnGBMCJ

You should download them into ```ProteinEmbedding/embeddings/yeast/```. This will allow the provided to scripts to run with these embeddings. 

Note that this is not required to generate and evaluate the remainder of the embeddings.

<a name="onto2vec"></a>
## Onto2Vec
Onto2Vec is a method developed in the following paper:

Onto2Vec: joint vector-based representation of biological entities and their ontology-based annotations by Fatima Zohra Smaili, Xin Gao, and Robert Hoehndorf. 2018. https://academic.oup.com/bioinformatics/article/34/13/i52/5045776

A modified version of their pipeline is included in the ```onto2vec/``` directory. Their original code can be found at: https://github.com/bio-ontology-research-group/onto2vec/

<a name="changes"></a>
### Changes to Onto2Vec pipeline
Several changes/bug fixes were made to the Onto2Vec pipeline. They are detailed here:
- In ```OntoProcess.groovy```, the following lines were added to the bottom of the file in order to flush the output to file. Otherwise, several hundred lines were lost.
  ```
  out.flush()
  out1.flush()
  out.close()
  out1.close()
  ```
- The original ```AddAncestors.pl``` was replaced with ```add_ancestors.py``` and ```add_parents.py```. The original script was incredibly slow and included a fatal bug.
  - ```add_ancestors.py``` propagates protein annotations up the entire GO tree.
  - ```add_parents.py``` propagates protein annotations up only a single layer.
  
- In ```runWord2Vec.py```, line 23 was changed from:
  ```
  file.write (str(GO_class) + ' '+ str(GOvectors[GO_class]) +'\n')
  ```
  to
  ```
  file.write (str(GO_class) + ' '+ ' '.join(str(element) for element in GOvectors[GO_class]) +'\n')
  ```
  This change results in nicer output file format. The new code prints the entire embedding on a single line, without extra ```,```, ```[```, and ```]``` characters.
- ```get_sum_mean_embeddings.py``` was added. This script generates protein embeddings by taking the sum and mean of GO class embeddings. This script is also used to generate protein embeddings from class embeddings generated via Dat Duong's GCN method.

<a name="evaluate"></a>
## Options for evaluate_embeddings.py
Each of the three tasks (binary PPI prediction, PPI type classification, and EC number classification), are evaluated using evaluate_embeddings.py. This script has several key options:
- Use ```-s``` to save the different classifiers. This will allow you to only have to perform training once. 
- Use ```-l``` to load the pretrained classifiers in.
- ```-p``` allows you to plot the ROC curve. You must specify a line name using ```-ln``` and optionally specify a line color using ```-lc```. 
- The ROC curve can be saved to a pickle file with ```-ps``` or exported to a .PNG using ```-pe```. 
- To plot the curves for different embedding types in the same plots, simply load the pickled ROC using ```-pl```.
By default, the provided script will train each classifier for each embedding type, then produce a plot with the ROCs of all embedding types on top of one another.




