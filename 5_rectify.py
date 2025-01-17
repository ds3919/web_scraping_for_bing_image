import csv
import pandas as pd

# Read the CSV
df = pd.read_csv('results_fixed.csv', encoding='latin1')

currentWordGroup = ""
numOfImages = 0
incompleteImageSet = []

# Lists any classes with less than 10 images
for index, row in df.iterrows():
    word = row['word']
    validity = row['categorization']

    if word == currentWordGroup and validity == True:
        numOfImages+=1
        continue
    elif word == currentWordGroup and validity == False:
        continue
    elif word != currentWordGroup and validity == True:
        
        if numOfImages < 10:
            incompleteImageSet.append(currentWordGroup)
        
        currentWordGroup = word
        numOfImages = 1
        continue
    elif word != currentWordGroup and validity == False:

        if numOfImages < 10:
            incompleteImageSet.append(currentWordGroup)
        
        currentWordGroup = word
        numOfImages = 0

for image in incompleteImageSet: print(image)