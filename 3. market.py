from bs4 import BeautifulSoup  # Importing BeautifulSoup to parse HTML content
import ttkbootstrap as ttk     # Does the same as 'from tkinter import ttk' but lets us customize the GUI even more with themes
import tkinter as tk           # Importing tkinter to create a GUI
import requests                # Importing requests to get HTML content from a website
import pandas as pd            # Importing pandas for data manipulation and file saving
import os                      # Importing os to use the clear function from the os and create a folder to store the exported files

# FUNCTIONS ============================================================================================================

clear = lambda: os.system('clear')                                  # Function to clear the terminal
clear()                                                             # Clear terminal output

def display_web_tables(soup, table_class, function_name):
    tables = soup.find_all('table', class_=table_class)             # Find all tables with the specified class
    if tables:                                                      # If at least one table is found
        combined_string = ""                                        # Create a string to store the text representation of all DataFrames
        if not os.path.exists('market files'):                      # if the folder 'market' doesn't exist
            os.makedirs('market files')                             # Create the folder 'market'
        for i, table in enumerate(tables):                          # Loop through each found table
            headers = [header.text.strip() for header in table.find_all('th')]  # Extract all headers from currently accessed table
            rows = []                                               # Create an empty list to store rows
            for row in table.find_all('tr')[1:]:                    # Loop through each row (excluding the header row)
                columns = row.find_all('td')                        # Extract columns from the row
                rows.append([col.text.strip() for col in columns])  # Append cleaned text to rows list
            df = pd.DataFrame(rows, columns=headers)                # Create DataFrame from headers and rows
            df.index = df.index + 1                                 # Increment index by 1 so it starts from 1 not 0
            file_name = f'{function_name}_{i+1}.csv'                # Save DataFrame to CSV file in the 'market' folder
            file_path = os.path.join('market files', file_name)     # Create the file path
            df.to_csv(file_path, index=False, mode='w')             # Save the DataFrame to the file path
            print(df)                                               # Display DataFrame
            combined_string += df.to_string() + "\n\n"              # Append the string representation of the DataFrame to the combined string
            update_treeview(tree, headers, rows)
    else:
        print("No table found with the specified class.")  

def get_indices():                                                  # Function that gets the stock market for major indices (from the web like the rest)
    url = 'https://www.investing.com/indices/major-indices'         # URL of the website we will scrape
    page = requests.get(url)                                        # Requesting the HTML content of the website
    soup = BeautifulSoup(page.text, 'html.parser')                  # Parsing the HTML content # Extracting text from each table and stripping whitespace
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'indices')# display the table in the terminal and GUI and add it to a CSV file in a table format
    
def get_trending_stocks():                                          # Function that gets the stocks that are currently trending
    url = 'https://www.investing.com/equities/trending-stocks'      # URL of the website we will scrape
    page = requests.get(url)                                        # Requesting the HTML content of the website
    soup = BeautifulSoup(page.text, 'html.parser')                  # Parsing the HTML content
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'trending_stocks')# Calling the display_web_tables function

def get_commodity_futures():                                        # Function that gets the stocks of commodity futures
    url = 'https://www.investing.com/commodities/real-time-futures' # URL of the website we will scrape
    page = requests.get(url)                                        # Requesting the HTML content of the website
    soup = BeautifulSoup(page.text, 'html.parser')                  # Parsing the HTML content # Extracting text from each table and stripping whitespace
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'commodity_futures')# Calling the display_web_tables function

def get_exchange_rates():                                           # Function that gets the exchange rates of different currencies
    url = 'https://www.investing.com/currencies/streaming-forex-rates-majors'# URL of the website we will scrape
    page = requests.get(url)                                        # Requesting the HTML content of the website
    soup = BeautifulSoup(page.text, 'html.parser')                  # Parsing the HTML content # Extracting text from each table and stripping whitespace
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'exchange_rates')# Calling the display_web_tables function

def get_etfs():                                                     # Function that gets the stocks of ETFs (Exchange Traded Funds)
    url = 'https://www.investing.com/etfs/major-etfs'               # URL of the website we will scrape
    page = requests.get(url)                                        # Requesting the HTML content of the website
    soup = BeautifulSoup(page.text, 'html.parser')                  # Parsing the HTML content # Extracting text from each table and stripping whitespace
    display_web_tables(soup, 'genTbl closedTbl crossRatesTbl elpTbl elp40', 'etfs')# Calling the display_web_tables function

def get_government_bonds():                                         # Function that gets the stocks of government bonds
    url = 'https://www.investing.com/rates-bonds/world-government-bonds'# URL of the website we will scrape
    page = requests.get(url)                                        # Requesting the HTML content of the website
    soup = BeautifulSoup(page.text, 'html.parser')                  # Parsing the HTML content # Extracting text from each table and stripping whitespace
    display_web_tables(soup, 'genTbl closedTbl crossRatesTbl', 'government_bonds')# Calling the display_web_tables function

def get_funds():                                                    # Function that gets the stocks of funds
    url = 'https://www.investing.com/funds/major-funds'             # URL of the website we will scrape
    page = requests.get(url)                                        # Requesting the HTML content of the website
    soup = BeautifulSoup(page.text, 'html.parser')                  # Parsing the HTML content # Extracting text from each table and stripping whitespace
    display_web_tables(soup, 'genTbl closedTbl crossRatesTbl elpTbl elp40', 'funds')# Calling the display_web_tables function

def get_cryptocurrencies():                                         # Function that gets the stocks of cryptocurrencies
    url = 'https://markets.businessinsider.com/cryptocurrencies'             # URL of the website we will scrape
    page = requests.get(url)                                        # Requesting the HTML content of the website
    soup = BeautifulSoup(page.text, 'html.parser')                  # Parsing the HTML content # Extracting text from each table and stripping whitespace
    display_web_tables(soup, 'table table--col-1-font-color-black table--suppresses-line-breaks table--fixed', 'cryptocurrencies')# Calling display_web_tables

def update_treeview(tree, headers, rows):
    # Clear existing data
    tree.delete(*tree.get_children())
    
    # Set new columns
    tree["columns"] = ["Index"] + headers                           # Add "Index" as the first column
    tree.heading("Index", text="Index")                             # Set the heading for the "Index" column
    tree.column("Index", anchor='center', width=50, stretch=True)  # Set the width of the "Index" column and disable stretching
    
    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, anchor='center', width=50, minwidth=50, stretch=True) 
    # Insert new rows
    for i, row in enumerate(rows, start=1):  # Start the index from 1
        tree.insert("", "end", values=[i] + row)  # Add the index as the first value in each row

# MAIN CODE ============================================================================================================


root = ttk.Window(themename = 'darkly')                           # Creating a tkinter window and customising it
root.title("Market Shares")                                       # Setting the title of the window
root.geometry("1200x800")  # Setting the fixed size of the window
root.resizable(False, False)  # Disabling window resizing

# Buttons and their frame / visual functions
buttons = [
    ("Indices", get_indices),
    ("Trending Stocks", get_trending_stocks),
    ("Commodity Futures", get_commodity_futures),
    ("Exchange Rates", get_exchange_rates),
    ("ETFs", get_etfs),
    ("Government Bonds", get_government_bonds),
    ("Funds", get_funds),
    ("Cryptocurrencies", get_cryptocurrencies)
]
combined_string = ""  # Define the variable "combined_string"
button_frame = ttk.Frame(root)
button_frame.pack(anchor='e', padx=15, pady=10)
for text, command in buttons:
    ttk.Button(button_frame, text=text, command=command).pack(side='left', padx=5) 
button_frame.pack(pady=20)  # Displaying the frame widget

tree = ttk.Treeview(root)
tree.pack(side='right', padx=20, pady=20, fill='y')

root.mainloop()
        