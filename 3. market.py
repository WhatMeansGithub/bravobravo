from bs4 import BeautifulSoup  # Importing BeautifulSoup to parse HTML content
import ttkbootstrap as ttk     # Does the same as 'from tkinter import ttk' but lets us customize the GUI even more with themes
import tkinter as tk           # Importing tkinter to create a GUI
import requests                # Importing requests to get HTML content from a website
import pandas as pd            # Importing pandas for data manipulation and file saving
import os                      # Importing os to use the clear function from the os

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
        output_string.set(df)                                       # Displaying a message in the GUI
    else:
        print("No table found with the specified class.")           # If the table does not exist, print this message (it was useful to check for errors)

def get_major_indices():                                              # Function to get the stock market for major indices from the web
    url = 'https://www.investing.com/indices/major-indices'    # URL of the website we will scrape
    page = requests.get(url)                                  # Requesting the HTML content of the website
    soup = BeautifulSoup(page.text, 'html.parser')            # Parsing the HTML content # Extracting text from each table and stripping whitespace
    all_variables = soup.find_all('table' , class_="datatable-v2_table__93S4Y dynamic-table-v2_dynamic-table__iz42m datatable-v2_table--mobile-basic__uC0U0 datatable-v2_table--freeze-column__uGXoD undefined")
    all_variables = [table.text.strip() for table in all_variables] # Extracting text from each table and stripping whitespace

    special_table = soup.find('table' , class_="datatable-v2_table__93S4Y dynamic-table-v2_dynamic-table__iz42m datatable-v2_table--mobile-basic__uC0U0 datatable-v2_table--freeze-column__uGXoD undefined")
    process_table(special_table)

    data = []                                           # we create a list to store data from the table
    for table in all_variables:                        # Looping through each table
        lines = table.split('\n')                       # Splitting the table into lines
        headers = lines[0].split()                      # Assuming the first line contains headers
        rows = [line.split() for line in lines[1:]]     # Assuming the rest of the lines contain rows
        data.append((headers, rows))                    # Appending headers and rows to the data list   
    for i, (headers, rows) in enumerate(data):          # Looping through the data list
        df = create_dataframe(headers, rows)            # Creating a DataFrame from the headers and rows
        filename = f'market_table_{i+1}.csv'            # Create a filename for each table
        df.to_csv(filename, index=False)                # Save the DataFrame to a CSV file
    
def get_trending_stocks():                                      # Function to get the stocks that are currently trending
    url = 'https://www.investing.com/equities/trending-stocks'    # URL of the website we will scrape
    page = requests.get(url)                                  # Requesting the HTML content of the website
    soup = BeautifulSoup(page.text, 'html.parser')            # Parsing the HTML content # Extracting text from each table and stripping whitespace
    all_variables = soup.find_all('table' , class_="datatable-v2_table__93S4Y dynamic-table-v2_dynamic-table__iz42m datatable-v2_table--mobile-basic__uC0U0 datatable-v2_table--freeze-column__uGXoD undefined")
    all_variables = [table.text.strip() for table in all_variables] # Extracting text from each table and stripping whitespace

    special_table = soup.find('table' , class_="datatable-v2_table__93S4Y dynamic-table-v2_dynamic-table__iz42m datatable-v2_table--mobile-basic__uC0U0 datatable-v2_table--freeze-column__uGXoD undefined")
    process_table(special_table)

    data = []                                           # we create a list to store data from the table
    for table in all_variables:                        # Looping through each table
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
window = ttk.Window(themename = 'darkly')               # Creating a tkinter window and customising it
window.title("Market Shares")                           # Setting the title of the window
window.geometry("1200x1000")                            # Setting the size of the window



# Button field
button_frame = ttk.Frame(master = window)                                                           # Creating a frame widget that holds the button widgets
button1 = ttk.Button(master = button_frame, text="Major Indices", command = get_major_indices)      # Creating a button widget
button1.pack(side = 'left' , padx = 10)                                                             # Displaying the button widget and positioning it to the left
button2 = ttk.Button(master = button_frame, text="Trending Stocks", command = get_trending_stocks)  # Creating a button widget
button2.pack(side = 'left')                                                                         # Displaying the button widget and positioning it to the left




entry_int = ttk.Entry(master = button_frame)                                                     # Creating an entry widget
button_frame.pack(pady = 20)                                                                     # Displaying the frame widget

# output field
output_string = tk.StringVar()                                                                  # Creating a string variable
output_lable = ttk.Label(master = window, font = 'Calibri 15' , textvariable = output_string)   # Creating a label widget
output_lable.pack()                                                                             # Displaying the label widget
output_string.set("Data has been saved to CSV files.")                                          # Displaying a message in the GUI

# run
window.mainloop()                                                                               # Running the tkinter window