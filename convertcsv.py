import csv
import pandas as pd
import numpy as np
filename = 'data17.txt'
cleaned_data = []

# Read the data from the text file
with open(filename, 'r') as file:
    lines = file.readlines()


# Clean the data by remove regex
for line in lines:
    values = line.strip().split('\t')
    
    for i in range(len(values)):
        col = values[i].split()[0].replace('Â', '').replace('\xa0', '').replace('%', '').replace(',','.')

        # Create empty inner list if necessary
        while len(cleaned_data) <= i:
            cleaned_data.append([])
            
        cleaned_data[i].append(col)        


#split company name and datetime
first_subarray = cleaned_data[0]
split_array = [elem.split('.') for elem in first_subarray]
company_name, transaction_date = zip(*split_array)
# new_list_of_arrays = [[item] for item in first_subarray] + cleaned_data[1:]
cleaned_data[0] = company_name
cleaned_data.insert(1, transaction_date)


df = pd.DataFrame(cleaned_data).transpose()
#print(df)

#process by using cumulative sum
company_group = df.groupby(0)
#print(df)
for group_name, group_indices in company_group.groups.items():
    for i in range (2, df.shape[1] - 2):
        colvalues = company_group.get_group(group_name)[i]
        col_reversed = colvalues[::-1].str.replace('.','').astype(float).cumsum()
        col_result = col_reversed[::-1]

        df.loc[group_indices, i] = col_result
        
#Process last 2 col because it not mean cumulative sum
for i in range (df.shape[1] - 2, df.shape[1]):
    col = df.loc[:,i].replace('',None)
    col_results = col.bfill()
    df.loc[:,i] = col_results    
    # print(df.loc[:,i])
    
    

# Convert date column to string format
df[1] = pd.to_datetime(df[1], dayfirst=True)
#print(df[1])

#Convert cleaned data to CSV format
csv_filename = 'data.csv'
df.to_csv(csv_filename, index=False)
print(f"CSV file '{csv_filename}' has been created successfully.")