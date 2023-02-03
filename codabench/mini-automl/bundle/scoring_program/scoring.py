
# Imports
import json
import os
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

# Path
reference_dir = os.path.join('/app/input/', 'ref')  # Ground truth data
prediction_dir = os.path.join('/app/input/', 'res') # Prediction made by the model
output_dir = '/app/output/' # To write the scores
score_file = os.path.join(output_dir, 'scores.json')          # Scores
html_file = os.path.join(output_dir, 'detailed_results.html') # Detailed feedback

def write_file(file, content):
    """ Write content in file.
    """
    with open(file, 'w', encoding="utf-8") as f:
        f.write(content)

def get_dataset_names():
    """ Return the names of the datasets.
    """
    return ['dataset1', 'dataset2', 'dataset3', 'dataset4']

def get_data(dataset):
    """ Get ground truth (y_test) and predictions (y_pred) from the dataset name.
    """
    y_test = pd.read_csv(os.path.join(reference_dir, dataset + 'reference_test.csv'))
    y_test = np.array(y_test)
    y_pred = np.genfromtxt(os.path.join(prediction_dir, dataset + '.predict'))
    return y_test, y_pred

def print_bar():
    """ Display a bar ('----------')
    """
    print('-' * 10)

def main():
    """ The scoring program.
    """
    print('Scoring program.')
    print_bar()
    # Initialized detailed results
    write_file(html_file, '<t1>Detailed results</t1>') # Create the file to give real-time feedback
    scores = {}
    for dataset in get_dataset_names(): # Loop over datasets
        print_bar()
        print(dataset)
        print_bar()
        # Read data
        print('Reading prediction')
        y_test, y_pred = get_data(dataset)
        print_bar()
        # Compute score
        accuracy = accuracy_score(y_true, y_pred)
        print('Accuracy: {}'.format(accuracy))
        scores[dataset] = accuracy
        print_bar()
    # Get duration
    with open(os.path.join(prediction_dir, 'metadata.json')) as f:
        duration = json.load(f).get('duration', -1)
    scores['duration'] = duration
    # Write scores
    print_bar()
    print('Scoring program finished. Writing scores.')
    print(scores)
    write_file(score_file, json.dumps(scores))

if __name__ == '__main__':
    main()
