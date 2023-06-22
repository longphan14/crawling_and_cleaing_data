import csv
import pandas as pd
import numpy as np
from googletrans import Translator
filename = 'kqdq_ceo.csv'
cleaned_data = []
encoder = 'utf-16'
csv_filename = 'data.csv'


# Read the data from the csv file
df = pd.read_csv(filename, encoding=encoder)
header_list = [column.split('\t') for column in df.columns]

first_header = pd.DataFrame(pd.concat([pd.Series(lst) for lst in header_list]))

# Convert rows into array
data_arrays = df.values
translator = Translator()


# Split elements in the array by '\t'
for i in range(len(data_arrays)):
    data_arrays[i] = [str(elem).split('\t') for elem in data_arrays[i]]

for i in range(len(data_arrays)):
    if '###' in data_arrays[i][0][0]:
        data_arrays[i][0][0] = data_arrays[i][0][0].split("###")[1]         
    else:        
        data_arrays[i][0][0] = translator.translate(data_arrays[i][0][0], dest = 'en').text

data_arrays = data_arrays.T
new_data = pd.DataFrame()
new_data = pd.concat([new_data, first_header], axis=1)
data_arrays = data_arrays.flatten()
for i in range(len(data_arrays)):
    new_data = pd.concat([new_data, pd.DataFrame(data_arrays[i])], axis=1)

# Store the header row in a separate variable
header_row = new_data.iloc[0]
#Fix first header line
header_row.values[0] = 'Balance Sheet'
# Drop the first row which was used as the header
new_data = new_data[1:].reset_index(drop=True)
new_data.columns = header_row.values

#Convert cleaned data to CSV format
new_data.to_csv(csv_filename, index=False)
print(f"CSV file '{csv_filename}' has been created successfully.")

