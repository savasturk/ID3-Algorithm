ID3 ALGORITHM IMPLEMENTATION

This is the entry point of the application. The main funtion that calls the 
create decision tree algorithm is run_app. This in turn is called from main

To run
=======
python -u run.py train.dat test.dat

Data Strucutre
---------------

The funtion: create_decision_tree(examples, attributes, target_attribute, heuristic_funtion)
takes in the following input:

examples (train or test data) : list of dicts (python dictionaries)
attributes : list
target_attribute: string
heuristic_funtion: funtion pointer to "gain" funtion
