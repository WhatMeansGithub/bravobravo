from bs4 import BeautifulSoup  # Importing BeautifulSoup to parse HTML content
import requests                # Importing requests to get HTML content from a website
import os
import pandas as pd            # Importing pandas for data manipulation and file saving

# Function to clear the terminal
clear = lambda: os.system('clear')
clear()  # Clear terminal output

# URL of the website to scrape
url1 = 'https://www.investing.com/'
page1 = requests.get(url1)  # Requesting the HTML content of the website
soup1 = BeautifulSoup(page1.text, 'html.parser')  # Parsing the HTML content

# Finding all relevant tables with specific classes
all_variables = soup1.find_all('table', class_="datatable-v2_table__93S4Y dynamic-table-v2_dynamic-table__iz42m datatable-v2_table--mobile-basic__uC0U0 datatable-v2_table--freeze-column__uGXoD datatable-v2_table--freeze-column-first__zMZNN undefined")

# Extracting text from each table and stripping whitespace
all_variables = [table.text.strip() for table in all_variables]

# Splitting the extracted text into lines and columns
data = []
for table in all_variables:
    lines = table.split('\n')
    headers = lines[0].split()  # Assuming the first line contains headers
    rows = [line.split() for line in lines[1:]]
    data.append((headers, rows))

# Function to convert data into a DataFrame
def create_dataframe(headers, rows):
    df = pd.DataFrame(rows, columns=headers)
    return df

# Creating a DataFrame for each table and saving it to a file
for i, (headers, rows) in enumerate(data):
    df = create_dataframe(headers, rows)
    filename = f'table_{i+1}.csv'  # Create a filename for each table
    df.to_csv(filename, index=False)  # Save the DataFrame to a CSV file

# Finding the first relevant table with specific classes
first_table = soup1.find('table', class_="datatable-v2_table__93S4Y dynamic-table-v2_dynamic-table__iz42m datatable-v2_table--mobile-basic__uC0U0 datatable-v2_table--freeze-column__uGXoD datatable-v2_table--freeze-column-first__zMZNN undefined")

# Extracting text from the first table and stripping whitespace
if first_table:
    headers = [header.text for header in first_table.find_all('th')]  # Extracting headers
    rows = []
    for row in first_table.find_all('tr')[1:]:  # Skipping the header row
        columns = row.find_all('td')
        rows.append([col.text.strip() for col in columns])
    
    # Creating a DataFrame from the extracted data
    df = pd.DataFrame(rows, columns=headers)
    
    # Printing the DataFrame
    print(df)
else:
    print("No table found with the specified class.")