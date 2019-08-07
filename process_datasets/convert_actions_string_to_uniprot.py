import argparse
import time
from tqdm import tqdm

args = None

def convert_actions_string_to_uniprot(input_file_name, mapping_file_name, output_file_name):

    mapping = {}
    with open(mapping_file_name, 'r') as f:
        for line in tqdm(f):
            line_data = line.split()
            string_name = line_data[0]
            uniprot_name = line_data[1]
            mapping[string_name] = uniprot_name

    print("Protein mappings loaded: " + str(len(mapping)))

    acceptable_actions = {'activation', 'binding', 'catalysis', 'reaction', 'inhibition'}
    converted_actions = set()
    unconverted_count = 0
    with open(input_file_name, 'r') as f:
        next(f) # skip header row
        for line in tqdm(f):
            line_data = line.split()
            protein_1 = line_data[0]
            protein_2 = line_data[1]
            action = line_data[2]
            if (protein_1 in mapping and protein_2 in mapping and action in acceptable_actions):
                protein_1 = mapping[protein_1]
                protein_2 = mapping[protein_2]
                converted_actions.add(protein_1 + ' ' + protein_2 + ' ' + action)
            else:
                unconverted_count = unconverted_count + 1


    print("Protein action types converted: " + str(len(converted_actions)))
    print("Protein action types not converted: " + str(unconverted_count))

    with open(output_file_name, 'w') as f:
        for action in tqdm(converted_actions):
            f.write(action + '\n')

def get_args():
    global args
    parser = argparse.ArgumentParser()

    parser.add_argument('input', help="Protein Actions file path")
    parser.add_argument('-m', '--mapping', help="String to Uniprot Mapping file path", required=True)
    parser.add_argument('-o', '--output', help="Output file path", required=True)
    

    args = parser.parse_args()

if __name__ == "__main__":
    start_time = time.time()

    get_args()
    
    convert_actions_string_to_uniprot(args.input, args.mapping, args.output)
    
    print("Time taken: " + str(time.time() - start_time) + " seconds")