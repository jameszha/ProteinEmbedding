import argparse
import time
from tqdm import tqdm

args = None

def get_ec_numbers(enzyme_file_name, protein_file_name, ec_numbers_file_name, single=True):
    print("Loading proteins . . . ")
    proteins = set()
    with open(protein_file_name, 'r') as f:
        for line in tqdm(f):
            protein = line.strip()
            proteins.add(protein)
    print("Proteins loaded: " + str(len(proteins)))

    print("Looking for EC numbers . . . ")
    ec_numbers = {}
    ec_numbers_found = 0
    with open(enzyme_file_name, 'r') as f:
        current_id = None
        for line in tqdm(f):
            line_data = line.split()
            if (line_data[0] == "ID"):
                current_id = line_data[1]
                top_level_id = current_id.split('.')[0]

            if (line_data[0] == "DR"):
                for term in line_data:
                    protein = term.replace(',', '')
                    if protein in proteins:

                        if protein in ec_numbers:
                            ec_numbers[protein].add(top_level_id)
                        else:
                            ec_numbers[protein] = set(top_level_id)

                        ec_numbers_found = ec_numbers_found + 1

    print("EC Numbers found: " + str(ec_numbers_found) + " for " + str(len(ec_numbers)) + " unique proteins")

    print("Writing EC numbers out to file")
    count = 0
    with open(ec_numbers_file_name, 'w') as f:
        for protein in tqdm(ec_numbers):
            if (single == False or len(ec_numbers[protein]) == 1):
                f.write(protein + ' ' + ' '.join(sorted(ec_numbers[protein])) + '\n') 
                count = count + 1

    print("Wrote " + str(count) + " proteins with EC numbers out to file.")

def get_args():
    global args
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--enzymes', help="Input: Enzyme file path", required=True)
    parser.add_argument('-p', '--proteins', help="Input: proteins file path", required=True)
    parser.add_argument('-o', '--output', help="Output: annotations file path", required=True)
    parser.add_argument('-s', '--single', action='store_true', help="Only output proteins with single EC number")
    

    args = parser.parse_args()

if __name__ == "__main__":
    start_time = time.time()

    get_args()
    
    get_ec_numbers(args.enzymes, args.proteins, args.output, single=args.single)
    
    print("Time taken: " + str(time.time() - start_time) + " seconds")