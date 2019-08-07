import argparse
import time
from tqdm import tqdm

args = None

def interleave_links(input_file_name, output_file_name):
    positive = []
    negative = []

    with open(input_file_name, 'r') as f:
        for line in tqdm(f):
            line_data = line.split()
            if line_data[2] == '1':
                positive.append(line)
            else:
                negative.append(line)

    print("Positive links found: " + str(len(positive)))
    print("Negative links found: " + str(len(negative)))

    min_len = min(len(positive), len(negative))
    print("Truncating lists to len: " + str(min_len))
    positive = positive[:min_len]
    negative = negative[:min_len]

    interleaved = [link for pair in zip(positive, negative) for link in pair]
    print("Writing total of " + str(len(interleaved)) + " links to file")

    with open(output_file_name, 'w') as f:
        for link in tqdm(interleaved):
            f.write(link)

def get_args():
    global args
    parser = argparse.ArgumentParser()

    parser.add_argument('input', help="Protein Links file path")
    parser.add_argument('-o', '--output', help="Output file path", required=True)

    args = parser.parse_args()


if __name__ == "__main__":
    start_time = time.time()

    get_args()

    interleave_links(args.input, args.output)

    print("Time taken: " + str(time.time() - start_time) + " seconds")