import sys
import time
from tqdm import tqdm

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 get_ppi_embeddings.py <input:protein_links.lst> <input:embedding.lst> <output:ppi_embeddings.lst>")
        exit()

    input_links_file_name = sys.argv[1]
    input_vectors_file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    embeddings = dict()
    
    with open(input_vectors_file_name, 'r') as f:
        for line in f:
            line_data = line.split()
            protein = line_data[0]
            vector = line_data[1:]
            embeddings[protein] = vector

    print("Protein embeddings loaded: " + str(len(embeddings)))


    output_file = open(output_file_name, 'w')

    converted_protein_count = 0
    no_embedding_count = 0

    with open(input_links_file_name, 'r') as f:
        for line in tqdm(f):
            line_data = line.split()
            protein_1 = line_data[0]
            protein_2 = line_data[1]
            target = line_data[2]

            if (protein_1 in embeddings and protein_2 in embeddings):
                features = embeddings[protein_1] + embeddings[protein_2]
                for i, value, in enumerate(features):
                    features[i] = str(i+1) + ':' + value
                features = ' '.join(features)

                output_file.write(target + ' ' + features + '\n')

                converted_protein_count = converted_protein_count + 1

            else:
                no_embedding_count = no_embedding_count + 1

    print("Samples successfully converted: " + str(converted_protein_count))
    print("Samples with no embedding found: " + str(no_embedding_count))

    output_file.close()

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("Time taken: " + str(time.time() - start_time) + " seconds")