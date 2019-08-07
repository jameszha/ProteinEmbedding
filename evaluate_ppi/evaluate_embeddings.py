from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold

from sklearn.metrics import classification_report

from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

import sys
import time
from tqdm import tqdm

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

import numpy as np
np.random.seed(7898521)

# USAGE: OMP_NUM_THREADS=4 python3 evaluate_embeddings.py <input_SVM_Light_format> | tee out.txt
# If running in background: Currently, stdout is being flushed periodically. Can also use
# -u flag to unbuffer all output. 

def test_default_classifiers(X_train, X_test, y_train, y_test):

    print("\nTesting Logistic Regression . . . ")
    classifier = LogisticRegression()
    run_default_classifier(classifier, X_train, X_test, y_train, y_test)

    print("\nTesting Random Forest . . . ")
    classifier = RandomForestClassifier()
    run_default_classifier(classifier, X_train, X_test, y_train, y_test)

    print("\nTesting SVM . . . ")
    classifier =SVC(kernel='linear')
    run_default_classifier(classifier, X_train, X_test, y_train, y_test)

    print("\nTesting MLP  . . . ")
    classifier = MLPClassifier(hidden_layer_sizes=(800, 200,), max_iter=500)
    run_default_classifier(classifier, X_train, X_test, y_train, y_test)

def run_default_classifier(classifier, X_train, X_test, y_train, y_test):
    start = time.time()
    classifier.fit(X_train, y_train)
    y_true, y_pred = y_test, classifier.predict(X_test)
    print(classification_report(y_true, y_pred))
    print("Time taken: " + str(time.time() - start) + " seconds")
    sys.stdout.flush()



def tune_svm(X_train, X_test, y_train, y_test): 
    classifier = SVC() 
    tuning_parameters = [{'kernel': ['rbf'], 
                          'gamma': [1e-1, 1e-2, 1e-3, 1e-4, 1e-5], 
                          'C': [0.1, 1, 10, 100, 1000, 10000]},
                         {'kernel': ['linear'], 
                          'C': [0.1, 1, 10, 100, 1000, 10000]}]

    print("\nTuning hyper-parameters for SVM . . . ")
    sys.stdout.flush()
    tune_classifier(classifier, tuning_parameters, X_train, X_test, y_train, y_test)

def tune_random_forest(X_train, X_test, y_train, y_test): 
    classifier = RandomForestClassifier() 
    tuning_parameters = [{'bootstrap': [True, False], 
                          'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None], 
                          'max_features': ['auto', 'sqrt'],
                          'min_samples_leaf': [1, 2, 4],
                          'min_samples_split': [2, 5, 10],
                          'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]}]

    print("\nTuning hyper-parameters for Random Forest . . . ")
    sys.stdout.flush()
    tune_classifier(classifier, tuning_parameters, X_train, X_test, y_train, y_test)

def tune_mlp(X_train, X_test, y_train, y_test): 
    classifier = MLPClassifier()
    tuning_parameters = [{'hidden_layer_sizes': [(800,200), (200,800), (400,400), (200), (400)],
                          'activation': ['tanh', 'relu'],
                          'solver': ['sgd', 'adam'],
                          'alpha': [0.0001, 0.001, 0.01],
                          'learning_rate': ['constant','adaptive']}]

    print("\nTuning hyper-parameters for MLP . . . ")
    sys.stdout.flush()
    tune_classifier(classifier, tuning_parameters, X_train, X_test, y_train, y_test)

def tune_classifier(classifier, tuning_parameters, X_train, X_test, y_train, y_test):
    start = time.time()
    clf = GridSearchCV(classifier, tuning_parameters, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=7898521), scoring='accuracy', n_jobs=4, verbose=0)
    clf.fit(X_train, y_train)

    print("Best parameters found:\n")
    print(clf.best_params_)

    print("\nGrid scores on development set:\n")
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
    print()

    print("Detailed classification report:\n")
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))
    print("Time taken: " + str(time.time() - start) + " seconds")
    sys.stdout.flush()



def main():
    print("Loading data . . . ")
    sys.stdout.flush()
    data_file_name = sys.argv[1]
    X = []
    y = []
    temp = 0
    with open(data_file_name, 'r') as f:
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
    print("Partitioning data into training/testing sets . . . ")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.95, random_state=0)
    print("Training samples loaded: " + str(len(y_train)))
    print("Testing samples loaded: " + str(len(y_test)))
    sys.stdout.flush()

    print("TESTING DEFAULT PARAMETERS . . .")
    test_default_classifiers(X_train, X_test, y_train, y_test)

    # print("TUNING PARAMETERS USING GRIDSEARCH . . .")
    # tune_svm(X_train, X_test, y_train, y_test)
    # tune_random_forest(X_train, X_test, y_train, y_test)
    # tune_mlp(X_train, X_test, y_train, y_test)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("\nTotal time taken: " + str(time.time() - start_time) + " seconds")
    sys.stdout.flush()
