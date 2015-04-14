**********************************************************************************************
							README FILE FOR METHODOLOGY 1
							
							  CHAHNA DIXIT - B00695383
							  HARDIK DALAL - B00696939
							  UTSAV PATEL  - B00691151
**********************************************************************************************

The .txt file Cell_Phones_&_Accessories.txt is used as dataset.

How to run the program?

1. Run load.py
It converts the original text file to json format.

2. Edit transformToCSV.py, go to line 23 and edit the path to the path where your json file is created.
Run transformToCSV.py
It converts json format to data.csv.

3. Run Amazon.py
It performs pre-processing, extracts the features and creates extratced_features.csv.

4. Run model.py
According to the requirement, uncomment the line of code for the classifier to be used.
We have used 3 classification algorithms: Gradient Boosting Classifier, Naive Bayes Classifier, Decision tree classifier
model.py also finds the accuracy, precision, recall and fscore.