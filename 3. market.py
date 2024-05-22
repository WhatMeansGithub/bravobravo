from bs4 import BeautifulSoup  # Importing BeautifulSoup to parse HTML content
import tkinter as tk           # Importing tkinter to create a GUI
from tkinter import ttk        # Importing ttk to create themed widgets
import requests                # Importing requests to get HTML content from a website
import pandas as pd            # Importing pandas for data manipulation and file saving
import os                      # Importing os to clear the terminal

# FUNCTIONS ============================================================================================================

clear = lambda: os.system('clear') # Function to clear the terminal
clear()                            # Clear terminal output

def create_dataframe(headers, rows):         # Function that converts data into a DataFrame similar to a table
    df = pd.DataFrame(rows, columns=headers) # Creating a DataFrame with rows and columns
    return df                                # Returning the DataFrame

def menu():                                  # Function that displays the menu options
    print("1. Indices" , "2. Stocks" , "3. Commodities" , "4. Currencies" , "5. EFTs" , "\n" , "6. Bonds" , "7. Funds" , "8. Cryptocurrencies" , "9. Exit")
    choice = input("Enter your choice: ")    # Asking the user to enter a choice

def process_table(table):                                           # Function that processes the tables from the web pages
    if table:                                                       # If the table exists                         
        headers = [header.text for header in table.find_all('th')]  # Extracting header's text/titles from the table 
        rows = []                                                   # Creating an empty list to store rows
        for row in table.find_all('tr')[1:]:                        # Looping through each row in the table (excluding the header row)
            columns = row.find_all('td')                            # Extracting columns from the row
            rows.append([col.text.strip() for col in columns])      # Appending each column to the rows list
        df = pd.DataFrame(rows, columns=headers)                    # Creating a DataFrame from the headers and rows
        df.index = df.index + 1                                     # Incrementing the index by 1 so it starts from 1 not 0
        print(df)                                                   # Displaying the DataFrame (table basically)
    else:
        print("No table found with the specified class.")           # If the table does not exist, print this message (it was useful to check for errors)

def get_major_indices():                                              # Function to get the stock market for major indices from the web
    url1 = 'https://www.investing.com/indices/major-indices'    # URL of the website we will scrape
    page1 = requests.get(url1)                                  # Requesting the HTML content of the website
    soup1 = BeautifulSoup(page1.text, 'html.parser')            # Parsing the HTML content # Extracting text from each table and stripping whitespace
    all_variables1 = soup1.find_all('table' , class_="datatable-v2_table__93S4Y dynamic-table-v2_dynamic-table__iz42m datatable-v2_table--mobile-basic__uC0U0 datatable-v2_table--freeze-column__uGXoD undefined")
    all_variables1 = [table.text.strip() for table in all_variables1] # Extracting text from each table and stripping whitespace

    special_table = soup1.find('table' , class_="datatable-v2_table__93S4Y dynamic-table-v2_dynamic-table__iz42m datatable-v2_table--mobile-basic__uC0U0 datatable-v2_table--freeze-column__uGXoD undefined")
    process_table(special_table)

    data = []                                           # we create a list to store data from the table
    for table in all_variables1:                        # Looping through each table
        lines = table.split('\n')                       # Splitting the table into lines
        headers = lines[0].split()                      # Assuming the first line contains headers
        rows = [line.split() for line in lines[1:]]     # Assuming the rest of the lines contain rows
        data.append((headers, rows))                    # Appending headers and rows to the data list   
    for i, (headers, rows) in enumerate(data):          # Looping through the data list
        df = create_dataframe(headers, rows)            # Creating a DataFrame from the headers and rows
        filename = f'market_table_{i+1}.csv'            # Create a filename for each table
        df.to_csv(filename, index=False)                # Save the DataFrame to a CSV file

def get_trending_stocks():                                      # Function to get the stocks that are currently trending
    url1 = 'https://www.investing.com/equities/trending-stocks'    # URL of the website we will scrape
    page1 = requests.get(url1)                                  # Requesting the HTML content of the website
    soup1 = BeautifulSoup(page1.text, 'html.parser')            # Parsing the HTML content # Extracting text from each table and stripping whitespace
    all_variables1 = soup1.find_all('table' , class_="datatable-v2_table__93S4Y dynamic-table-v2_dynamic-table__iz42m datatable-v2_table--mobile-basic__uC0U0 datatable-v2_table--freeze-column__uGXoD undefined")
    all_variables1 = [table.text.strip() for table in all_variables1] # Extracting text from each table and stripping whitespace

    special_table = soup1.find('table' , class_="datatable-v2_table__93S4Y dynamic-table-v2_dynamic-table__iz42m datatable-v2_table--mobile-basic__uC0U0 datatable-v2_table--freeze-column__uGXoD undefined")
    process_table(special_table)

    data = []                                           # we create a list to store data from the table
    for table in all_variables1:                        # Looping through each table
        lines = table.split('\n')                       # Splitting the table into lines
        headers = lines[0].split()                      # Assuming the first line contains headers
        rows = [line.split() for line in lines[1:]]     # Assuming the rest of the lines contain rows
        data.append((headers, rows))                    # Appending headers and rows to the data list   
    for i, (headers, rows) in enumerate(data):          # Looping through the data list
        df = create_dataframe(headers, rows)            # Creating a DataFrame from the headers and rows
        filename = f'market_table_{i+1}.csv'            # Create a filename for each table
        df.to_csv(filename, index=False)                # Save the DataFrame to a CSV file

# MAIN CODE ============================================================================================================

# window
window = tk.Tk()                # Creating a tkinter window
window.title("Market Shares")   # Setting the title of the window
window.geometry("800x600")      # Setting the size of the window

# title
title = ttk.Label(master = window, text="Major Indices", font=("Calibri 30 bold"))   # Creating a label widget
title.pack()                                                                # Displaying the label widget

# input field
input_frame = ttk.Frame(master = window)                    # Creating a frame widget
entry = ttk.Entry(master = input_frame)                     # Creating an entry widget
button = ttk.Button(master = input_frame, text="Search")    # Creating a button widget
entry.pack(side = 'left', padx = 10)                                  # Displaying the entry widget
button.pack(side = 'left')                                # Displaying the button widget
input_frame.pack(pady = 20)                                          # Displaying the frame widget


# run
window.mainloop()               # Running the tkinter window