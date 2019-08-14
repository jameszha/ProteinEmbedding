from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn import preprocessing

from sklearn.metrics import auc
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve


from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

import matplotlib.pyplot as plt
from scipy import interp

import argparse
import pickle
import sys
import time
from tqdm import tqdm

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

import numpy as np
np.random.seed(7898521)

args = None

def get_classifiers():
    if (args.load_classifier): 
        classifiers = pickle.load(open(args.load_classifier, "rb"))

    else:
        classifiers = {}
        classifiers["LR"] = LogisticRegression()
        classifiers["RF"] = RandomForestClassifier()
        classifiers["SVM"] = SVC(kernel='linear', C=1.0, probability=True)
        classifiers["MLP"] = MLPClassifier(hidden_layer_sizes=(800, 200,), max_iter=500)

    return classifiers


def test_default_classifiers(X_train, X_test, y_train, y_test):

    classifiers = get_classifiers()
    y_pred = {}

    print("\nTesting Logistic Regression . . . ")
    y_pred["LR"] = run_default_classifier(classifiers["LR"], X_train, X_test, y_train, y_test)

    print("\nTesting Random Forest . . . ")
    classifier = RandomForestClassifier()
    y_pred["RF"] = run_default_classifier(classifiers["RF"], X_train, X_test, y_train, y_test)

    print("\nTesting SVM . . . ")
    classifier =SVC(kernel='linear', probability=True)
    y_pred["SVM"] = run_default_classifier(classifiers["SVM"], X_train, X_test, y_train, y_test)

    print("\nTesting MLP  . . . ")
    classifier = MLPClassifier(hidden_layer_sizes=(800, 200,), max_iter=500)
    y_pred["MLP"] = run_default_classifier(classifiers["MLP"], X_train, X_test, y_train, y_test)

    if (args.save_classifier):
        pickle.dump(classifiers, open(args.save_classifier, "wb"))

    if (args.plot):
        plot_roc(y_test, y_pred)

def run_default_classifier(classifier, X_train, X_test, y_train, y_test):
    start = time.time()
    if (args.load_classifier == None):
        classifier.fit(X_train, y_train)

    y_true, y_pred = y_test, classifier.predict(X_test)
    print(classification_report(y_true, y_pred))
    print("Time taken: " + str(time.time() - start) + " seconds")
    sys.stdout.flush()

    y_pred = classifier.predict_proba(X_test)
    return y_pred
    
def get_macro_roc(y_true, y_pred):
    auc_type = "macro"
    classes = np.unique(y_true)
    n_classes = len(classes)
    class_fpr = dict()
    class_tpr = dict()
    class_roc_auc = dict()

    # Get One-vs-Rest ROC for each class
    for i in range(n_classes):
        class_y_true = [1 if j == classes[i] else 0 for j in y_true]
        class_fpr[i], class_tpr[i], _ = roc_curve(class_y_true, y_pred[:, i])
        class_roc_auc[i] = auc(class_fpr[i], class_tpr[i])

    # Calculate Macro average of ROCs
    fpr = np.unique(np.concatenate([class_fpr[i] for i in range(len(classes))]))
    tpr = np.zeros_like(fpr)
    for i in range(n_classes):
        tpr += interp(fpr, class_fpr[i], class_tpr[i])
    tpr /= n_classes

    roc_auc = auc(fpr, tpr)

    return fpr, tpr, roc_auc

def plot_roc(y_true, y_pred):
    if(args.plot_load):
        fig, axes = pickle.load(open(args.plot_load, "rb"))
    else:
        fig, axes = plt.subplots(2, 2, figsize=(20,10))

    name = args.line_name
    color = args.line_color

    fpr, tpr, roc_auc = get_macro_roc(y_true, y_pred["LR"])
    axes[0,0].plot(fpr, tpr, 'b', color=color, label='%s (AUC = %0.2f)' % (name, roc_auc))

    fpr, tpr, roc_auc = get_macro_roc(y_true, y_pred["RF"])
    axes[0,1].plot(fpr, tpr, 'b', color=color, label='%s (AUC = %0.2f)' % (name, roc_auc))

    fpr, tpr, roc_auc = get_macro_roc(y_true, y_pred["SVM"])
    axes[1,0].plot(fpr, tpr, 'b', color=color, label='%s (AUC = %0.2f)' % (name, roc_auc))

    fpr, tpr, roc_auc = get_macro_roc(y_true, y_pred["MLP"])
    axes[1,1].plot(fpr, tpr, 'b', color=color, label='%s (AUC = %0.2f)' % (name, roc_auc))

    axes[0,0].set_title("Logistic Regression")
    axes[0,1].set_title("Random Forest")
    axes[1,0].set_title("SVM")
    axes[1,1].set_title("MLP")

    fig.subplots_adjust(wspace = 1, hspace=0.3, right=0.7)
    for axis in axes.flat:
        axis.set_aspect('equal')
        axis.legend(loc = 'center left', bbox_to_anchor=(1, 0.5))
        axis.plot([0, 1], [0, 1],'r--')
        axis.set_xlim([0, 1])
        axis.set_ylim([0, 1])
        axis.set_ylabel('TPR')
        axis.set_xlabel('FPR')

    if(args.plot_save):
        pickle.dump((fig, axes), open(args.plot_save, "wb"))
    if(args.plot_export):
        fig.savefig(args.plot_export, dpi=300, quality=100)

    plt.show()

def get_args():
    global args
    parser = argparse.ArgumentParser()

    parser.add_argument('input', help="Input dataset file path")

    parser.add_argument('-l', '--load_classifier', help="Load classifier from Pickle file")
    parser.add_argument('-s', '--save_classifier', help="Save classifier to Pickle file")

    parser.add_argument('-p', '--plot', action='store_true', help="Plot ROC curve")
    parser.add_argument('-ln', '--line_name', help="Name of line in plot")
    parser.add_argument('-lc', '--line_color', help="Name of color in plot", default="blue")

    parser.add_argument('-pl', '--plot_load', help="Load plot from Pickle file")
    parser.add_argument('-ps', '--plot_save', help="Load plot from Pickle file")
    parser.add_argument('-pe', '--plot_export', help="Export plot to PNG file")
    
    args = parser.parse_args()
    if args.plot and (args.line_name is None):
        parser.error("--plot requires --line_name")

def main():
    print("Loading data . . . ")
    sys.stdout.flush()
    X = []
    y = []
    temp = 0
    with open(args.input, 'r') as f:
        for line in tqdm(f):
            # Extract target and features from SVM Light format.
            # <line> .=. <target> <feature>:<value> <feature>:<value> ... <feature>:<value>
            line_data = line.split()
            target = int(line_data[0])
            data = line_data[1:]
            data = [float(val.split(':')[1]) for val in data]

            X.append(data)
            y.append(target)

    # Split data into training (70%) and testing (30%) sets
    X = preprocessing.scale(X)
    print("Partitioning data into training/testing sets . . . ")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    print("Training samples loaded: " + str(len(y_train)))
    print("Testing samples loaded: " + str(len(y_test)))
    sys.stdout.flush()

    print("TESTING DEFAULT PARAMETERS . . .")
    test_default_classifiers(X_train, X_test, y_train, y_test)


if __name__ == '__main__':
    start_time = time.time()
    get_args()
    main()
    print("\nTotal time taken: " + str(time.time() - start_time) + " seconds")
    sys.stdout.flush()
