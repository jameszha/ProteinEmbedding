import sys
import time


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 get_ec_embeddings.py <input:single_ec_numbers.lst> <input:embedding.lst> <output:ec_embeddings.lst>")
        exit()

    input_ec_file_name = sys.argv[1]
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

    with open(input_ec_file_name, 'r') as f:
        for line in f:
            line_data = line.split()
            protein = line_data[0]
            target = line_data[1]

            if (protein in embeddings):
                features = embeddings[protein]
                for i, value, in enumerate(features):
                    features[i] = str(i+1) + ':' + value
                features = ' '.join(features)

                output_file.write(target + ' ' + features + '\n')

                converted_protein_count = converted_protein_count + 1
                if (converted_protein_count % 1000 == 0): print("Converted links: " + str(converted_protein_count) + "\r" , end ='')

            else:
                no_embedding_count = no_embedding_count + 1

    print("\033[K",end='') 
    print("Proteins successfully converted: " + str(converted_protein_count))
    print("Proteins with no embedding found: " + str(no_embedding_count))

    output_file.close()

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("Time taken: " + str(time.time() - start_time) + " seconds")