from operator import add
import sys
import time

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 get_sum_mean_embeddings.py <input:class_embeddings.lst> <input:annotations.lst> <output:sum_embeddings.lst> <output:mean_embeddings.lst>")
        exit()
    class_embeddings_file_name = sys.argv[1]
    annotations_file_name = sys.argv[2]
    sum_embeddings_file_name = sys.argv[3]
    mean_embeddings_file_name = sys.argv[4]

    class_embeddings = {}
    with open(class_embeddings_file_name, 'r') as f:
        for line in f:
            line_data = line.split()
            go_class = line_data[0]
            vector = line_data[1:]
            vector = [float(i) for i in vector]
            class_embeddings[go_class] = vector

    print("Class embeddings loaded: " + str(len(class_embeddings)))

    totals = {}
    counts = {}
    with open(annotations_file_name, 'r') as f:
        for line in f:
            line_data = line.split()
            protein = line_data[0]
            go_class = line_data[2]
            if protein not in totals:
                totals[protein] = class_embeddings[go_class]
                counts[protein] = 1
            else:
                old_total = totals[protein]
                new_vector = class_embeddings[go_class] 
                totals[protein] = list(map(add, old_total, new_vector))
                counts[protein] = counts[protein] + 1

    with open(sum_embeddings_file_name, 'w') as f:
        for protein in totals:
            total = [str(i) for i in totals[protein]]
            f.write(protein + ' ' + ' '.join(total) + '\n')

    with open(mean_embeddings_file_name, 'w') as f:
        for protein in totals:
            mean = [str(i/counts[protein]) for i in totals[protein]]
            f.write(protein + ' ' + ' '.join(mean) + '\n')

    print("Protein with embeddings outputted: " + str(len(totals)))

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Time taken: " + str(time.time() - start_time) + " seconds")