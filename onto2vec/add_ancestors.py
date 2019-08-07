import re
import sys
import time

def main():
    annotations_file_name = "annotationAxiom.lst"
    axioms_file_name = "axioms.lst"
    output_file_name = "annotationAxiom_ancestors.lst"

    print("\nFinding all SubClassOf/EquivalentTo relations . . . ")
    parents = {}
    parent_count = 0
    with open(axioms_file_name, 'r') as f:
        for axiom in f:
            axiom_data = axiom.split()
            subclass_match = re.match("(\S+)\s+SubClassOf\s+(.*)", axiom)
            equivalence_match = re.match("(\S+)\s+EquivalentTo\s+(.*)", axiom)
            if (subclass_match):
                subclass = subclass_match.group(1)
                supclass = subclass_match.group(2)
            elif (equivalence_match):
                subclass = equivalence_match.group(1)
                supclass = equivalence_match.group(2)
            else: 
                continue


            if (subclass in parents):
                # if supclass not in parents[subclass]:
                parents[subclass].append(supclass)
            else:
                parents[subclass] = [supclass]
            parent_count = parent_count + 1

    print("SubClassOf/EquivalentTo relations found: " + str(parent_count))

    print("\nFinding current annotations . . . ")
    with open(annotations_file_name, 'r') as f:
        annotations = f.read().splitlines()

    print("Annotations found: " + str(len(annotations)))



    print("\nFinding new annotations . . . ")
    annotations_count = 0
    i = 0
    with open(output_file_name, 'w') as f:
        for annotation in annotations:
            f.write(annotation + '\n')

        while len(annotations) > 0:
            annotation = annotations.pop()
            annotation_match = re.match("(\S+)\s+hasFunction\s+(.*)", annotation)
            protein = annotation_match.group(1)
            old_class = annotation_match.group(2)
            if (old_class in parents):
                for parent in parents[old_class]:
                    new_annotation = protein + " hasFunction " + parent
                    f.write(new_annotation + '\n')
                    annotations.append(new_annotation)
                    annotations_count = annotations_count + 1
                    if (annotations_count % 100 == 0): print("Current progress: " + str(annotations_count) + " new annotations found\r" , end ='')

    print("\033[K",end='') 
    # annotations = set(annotations)
    print("New annotations found: " + str(annotations_count))

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Time taken: " + str(time.time() - start_time) + " seconds")