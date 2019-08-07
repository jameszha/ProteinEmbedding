import argparse
import time
from tqdm import tqdm

def get_binary_embeddings(annotations_file_name, output_file_name):

    classes = set()
    proteins = {}
    vectors = {}

    with open(annotations_file_name, 'r') as f:
        print("Loading all classes . . . ")
        for line in tqdm(f):
            line_data = line.split()
            go_class = line_data[2]
            classes.add(go_class)

            protein = line_data[0]
            if protein in proteins: 
                proteins[protein].append(go_class)
            else:
                proteins[protein] = [go_class]

        print("Proteins found: " + str(len(proteins)))
        print("Classes found: " + str(len(classes)))

        classes = list(classes) # fix order of classes to allow for indexing

        vector_length = len(classes)
        
        print("Generating binary embeddings . . . ")
        for protein in tqdm(proteins):
            vectors[protein] = [0] * vector_length
            for go_class in proteins[protein]:
                index = classes.index(go_class)
                if (index >= vector_length): print(str(index) + ' ' + str(vector_length))
                vectors[protein][index] = 1

    print("Writing vectors out to file . . .")
    with open(output_file_name, 'w') as f:
        for vector in tqdm(vectors):
            f.write(vector + ' ' + ' '.join(str(element) for element in vectors[vector]) + '\n')

def get_args():
    global args
    parser = argparse.ArgumentParser()

    parser.add_argument('input', help="Annotations file path")
    parser.add_argument('-o', '--output', help="Output file path", required=True)

    args = parser.parse_args()


if __name__ == "__main__":
    start_time = time.time()

    get_args()

    get_binary_embeddings(args.input, args.output)

    print("Time taken: " + str(time.time() - start_time) + " seconds")