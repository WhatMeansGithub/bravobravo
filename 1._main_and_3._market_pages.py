from tkinter import messagebox
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import customtkinter as ctk
import ttkbootstrap as ttk
import pandas as pd
import requests
import json
import os

# MARKET CODE =============================================================================================================

transaction_frame = None                                                            # Define the "transaction_frame" variable
current_table = ""                                                                  # Track the current active table
current_webscraping_function = None                                                 # Track the current webscraping function

def display_web_tables(soup, table_class, function_name):                           # complicated function to scrape and save tables from the web
    global current_table                                                            # accessing the global variable 'current_table' so we know which table we are currently working with
    current_table = function_name                                                   # the current table = 'indices' or 'trending_stocks' or etc.
    tables = soup.find_all('table', class_=table_class)                             # find all tables with the 'table' tag and the specified class
    if tables:                                                                      # if at least one table is found we continue with the code
        if not os.path.exists('market files'):                                      #   if the folder 'market' doesn't exist
            os.makedirs('market files')                                             #       create the folder 'market'
        combined_tb = pd.DataFrame()                                                #   creating a DataFrame on the go to hold all tables
        for i, table in enumerate(tables):                                          #   loop through each found table (example: government bonds has 73 tabes on the same page so the loop works 73 times)
            headers = [header.text.strip() for header in table.find_all('th')]      #       extract all headers from currently accessed table
            rows = []                                                               #       create an empty list to store rows
            for row in table.find_all('tr')[1:]:                                    #       loop through each row (excluding the header row)
                columns = row.find_all('td')                                        #           extract all columns from each row
                rows.append([col.text.strip() for col in columns])                  #           insert the cleaned text to rows list (which later goes in the DataFrame)
            tb = pd.DataFrame(rows, columns=headers)                                #       create DataFrame from headers and rows
            tb.index = tb.index + 1                                                 #       make it so the list index starts from 1 not 0 as usual 
            file_name = f'{function_name}_{i+1}.csv'                                #       make it so the saved file has a specific name
            file_path = os.path.join('market files', file_name)                     #       save the CSV file in the 'market files' folder
            tb.to_csv(file_path, index=False, mode='w')                             #       save the scraped table as a CSV file in the 'market files' folder with a specific name
            print(tb)                                                               #       prints the table
            combined_tb = pd.concat([combined_tb, tb], ignore_index=True)           #       add the table to the list of all tables for the current page
        update_treeview(tree, combined_tb.columns.tolist(), combined_tb.values.tolist())# update the Treeview with the combined tables list (all tables from the current page)
    else:                                                                           # if no tables are found
        print("No table found with the specified class.")                           #   print a message to the terminal

def get_indices():                                                                  # Function to scrape the indices table from the web
    url = 'https://www.investing.com/indices/major-indices'                         # we get the URL of the website under the variable 'url'
    page = requests.get(url)                                                        # this simulates opening the website in a browser
    soup = BeautifulSoup(page.text, 'html.parser')                                  # this lets us take the HTML code of the website and use it as a string
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'indices')                # this looks for the specific html code and table name that contain the table we want to scrape

def get_trending():                                                                 # Function to scrape the trending stocks table from the web
    url = 'https://www.investing.com/equities/trending-stocks'                      # we get the URL of the website under the variable 'url'
    page = requests.get(url)                                                        # this simulates opening the website in a browser
    soup = BeautifulSoup(page.text, 'html.parser')                                  # this lets us take the HTML code of the website and use it as a string
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'trending_stocks')        # this looks for the specific html code and table name that contain the table we want to scrape

def get_commodity_futures():                                                        # Function to scrape the commodity futures table from the web
    url = 'https://www.investing.com/commodities/real-time-futures'                 # we get the URL of the website under the variable 'url'
    page = requests.get(url)                                                        # this simulates opening the website in a browser
    soup = BeautifulSoup(page.text, 'html.parser')                                  # this lets us take the HTML code of the website and use it as a string 
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'commodity_futures')      # this looks for the specific html code and table name that contain the table we want to scrape             
      
def get_exchange_rates():                                                           # Function to scrape the exchange rates table from the web
    url = 'https://www.investing.com/currencies/streaming-forex-rates-majors'       # we get the URL of the website under the variable 'url'
    page = requests.get(url)                                                        # this simulates opening the website in a browser         
    soup = BeautifulSoup(page.text, 'html.parser')                                  # this lets us take the HTML code of the website and use it as a string        
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'exchange_rates')         # this looks for the specific html code and table name that contain the table we want to scrape                

def get_etfs():                                                                     # Function to scrape the ETFs table from the web
    url = 'https://www.investing.com/etfs/major-etfs'                               # we get the URL of the website under the variable 'url'
    page = requests.get(url)                                                        # this simulates opening the website in a browser          
    soup = BeautifulSoup(page.text, 'html.parser')                                  # this lets us take the HTML code of the website and use it as a string                
    display_web_tables(soup, 'genTbl closedTbl crossRatesTbl elpTbl elp40', 'etfs') # this looks for the specific html code and table name that contain the table we want to scrape                               

def get_government_bonds():                                                         # Function to scrape the government bonds table from the web
    url = 'https://www.investing.com/rates-bonds/world-government-bonds'            # we get the URL of the website under the variable 'url'
    page = requests.get(url)                                                        # this simulates opening the website in a browser                 
    soup = BeautifulSoup(page.text, 'html.parser')                                  # this lets us take the HTML code of the website and use it as a string             
    display_web_tables(soup, 'genTbl closedTbl crossRatesTbl', 'government_bonds')  # this looks for the specific html code and table name that contain the table we want to scrape                     

def get_funds():                                                                    # Function to scrape the funds table from the web
    url = 'https://www.investing.com/funds/major-funds'                             # we get the URL of the website under the variable 'url'
    page = requests.get(url)                                                        # this simulates opening the website in a browser                  
    soup = BeautifulSoup(page.text, 'html.parser')                                  # this lets us take the HTML code of the website and use it as a string            
    display_web_tables(soup, 'genTbl closedTbl crossRatesTbl elpTbl elp40', 'funds')# this looks for the specific html code and table name that contain the table we want to scrape                          

def get_cryptocurrencies():                                                         # Function to scrape the cryptocurrencies table from the web
    url = 'https://markets.businessinsider.com/cryptocurrencies'                    # we get the URL of the website under the variable 'url'
    page = requests.get(url)                                                        # this simulates opening the website in a browser                               
    soup = BeautifulSoup(page.text, 'html.parser')                                  # this lets us take the HTML code of the website and use it as a string                                     
    display_web_tables(soup, 'table table--col-1-font-color-black table--suppresses-line-breaks table--fixed', 'cryptocurrencies')# this looks for the specific html code and table name that contain the table we want to scrape

def load_stock_data(table_name):                                                    # Function to load stock data from a JSON file
    market_files_dir = 'market files'                                               # giving the folder name a variable for later use
    stock_data_file = os.path.join(market_files_dir, f'{table_name}_stocks.json')   # telling the code where to load the file from and under what name
    if os.path.exists(stock_data_file):                                             # if the file exists
        with open(stock_data_file, 'r') as file:                                    #   open the file in read mode allowing us to read data from it
            return json.load(file)                                                  #       load the stock data from the file
    return {}                                                                       # if the file doesn't exist return an empty dictionary

def save_stock_data(table_name, stock_data):                                        # Function to save the bought stocks data to a JSON file
    market_files_dir = 'market files'                                               # giving the folder name a variable for later use
    if not os.path.exists(market_files_dir):                                        # if the folder doesn't exist
        os.makedirs(market_files_dir)                                               #   create the folder
    stock_data_file = os.path.join(market_files_dir, f'{table_name}_stocks.json')   # telling the code where to save the file and under what name
    with open(stock_data_file, 'w') as file:                                        # open the file in write mode
        json.dump(stock_data, file)                                                 #   write the stock data to the file

def update_treeview(tree, headers, rows):                                           # Function to update the Treeview with the scraped data
    tree.delete(*tree.get_children())                                               # this deletes all the table info from the Treeview widget
    stock_data = load_stock_data(current_table)                                     # load the stock data from the JSON file
    tree["columns"] = ["Index", "Stock Count"] + headers                            # add "Index" and "Stock Count" as the first columns
    tree.heading("Index", text="#")                                                 # set the text of the "Index" column to "#" to indicate the index
    tree.heading("Stock Count", text="Owned")                                       # set the text of the "Stock Count" column to "Owned" to indicate owned stocks
    tree.column("Index", anchor='w', width=25, stretch=False)                       # set the width of the "Index" column and disable stretching so it doesnt change to a smaller size
    tree.column("Stock Count", anchor='center', width=60, stretch=False)            # set the width of the "Stock Count" column and disable stretching so it doesnt change to a smaller size
    for header in headers:                                                          # loop - for each header in the table
        tree.heading(header, text=header)                                           #   set the text of the header to the header name
        tree.column(header, anchor='center', width=80, minwidth=50)                 #   set the width of the header column and allow stretching
    for i, row in enumerate(rows, start=1):                                         # loop - for each row in the table
        stock_count = stock_data.get(str(i), 0)                                     #   get stock count for the current stock which is loaded from the JSON file
        tree.insert("", "end", values=[i, stock_count] + row)                       #   insert the row into the Treeview widget with the new stock count

def update_stock_count_in_treeview(tree):
    stock_data = load_stock_data(current_table)
    for item in tree.get_children():
        stock_index = tree.item(item, 'values')[0]
        stock_count = stock_data.get(str(stock_index), 0)
        current_values = tree.item(item, 'values')
        new_values = [current_values[0], stock_count] + current_values[2:]
        tree.item(item, values=new_values)

def clear_treeview(tree):
    tree.delete(*tree.get_children())
    tree["columns"] = []  # Clear the column headers
    tree.heading("#0", text="")  # Clear the heading of the first column

def show_treeview():
    treeview_frame.pack(padx=(330, 0), pady=0, fill='both', expand=True)

def hide_transaction_frame():
    if transaction_frame.winfo_ismapped():
        transaction_frame.place_forget()

def show_market_buttons():
    show_treeview()

    def buy_stocks():
        try:
            amount = int(search_bar.get())
            selected_items = tree.selection()
            if selected_items:
                stock_data = load_stock_data(current_table)
                for item in selected_items:
                    stock_index = tree.item(item, 'values')[0]
                    if str(stock_index) not in stock_data:
                        stock_data[str(stock_index)] = 0
                    stock_data[str(stock_index)] += amount
                save_stock_data(current_table, stock_data)
                messagebox.showinfo("Transaction Successful", f"Bought {amount} of each selected stock")
                current_webscraping_function()  # Re-scrape the current table
            else:
                messagebox.showwarning("No Selection", "Please select a stock to buy.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def sell_stocks():
        try:
            amount = int(search_bar.get())
            selected_items = tree.selection()
            if selected_items:
                stock_data = load_stock_data(current_table)
                for item in selected_items:
                    stock_index = tree.item(item, 'values')[0]
                    if str(stock_index) in stock_data:
                        if stock_data[str(stock_index)] >= amount:
                            stock_data[str(stock_index)] -= amount
                            if stock_data[str(stock_index)] == 0:
                                del stock_data[str(stock_index)]
                            messagebox.showinfo("Transaction Successful", f"Sold {amount} of {stock_index}")
                        else:
                            messagebox.showwarning("Not Enough Stocks", f"Not enough stocks to sell {amount} of {stock_index}.")
                    else:
                        messagebox.showwarning("No Stocks", f"No stocks available to sell for {stock_index}.")
                save_stock_data(current_table, stock_data)
                current_webscraping_function()  # Re-scrape the current table
            else:
                messagebox.showwarning("No Selection", "Please select a stock to sell.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def show_selected_stock_info():
        selected_items = tree.selection()
        stock_data = load_stock_data(current_table)
        total_stocks = 0
        for item in selected_items:
            stock_index = tree.item(item, 'values')[0]
            total_stocks += stock_data.get(str(stock_index), 0)
        messagebox.showinfo("Stock Information", f"Total stocks selected: {total_stocks}")

    global transaction_frame
    if transaction_frame is not None:
        transaction_frame.place_forget()

    transaction_frame = ttk.Frame(root)
    transaction_frame.place(relx=0, rely=0.461)

    search_bar = ttk.Entry(transaction_frame, width=20, font=('Helvetica', 15))
    search_bar.pack(side='bottom', padx=(20, 0), fill='x')
    search_bar.insert(0, "Enter number")

    buy_button = ctk.CTkButton(transaction_frame, text="BUY", font=('Helvetica', 40, 'bold'), width=140, height=110, fg_color='#137501', hover_color='#39c146', command=buy_stocks)
    buy_button.pack(side='left', padx=(20, 5), pady=(0, 10))

    sell_button = ctk.CTkButton(transaction_frame, text="Sell", font=('Helvetica', 30, 'bold'), width=140, height=50, fg_color="#750e01", hover_color='#e05c5c', command=sell_stocks)
    sell_button.pack(padx=(5, 0), pady=(0, 10))

    info_button = ctk.CTkButton(transaction_frame, text="Info", font=('Helvetica', 30, 'bold'), width=140, height=50, fg_color="#007bff", hover_color='#0056b3', command=show_selected_stock_info)
    info_button.pack(padx=(5, 0), pady=(0, 10))

    market_buttons = [
        ("Indices", get_indices),
        ("Trending Stocks", get_trending),
        ("Commodity Futures", get_commodity_futures),
        ("Exchange Rates", get_exchange_rates),
        ("ETFs", get_etfs),
        ("Government Bonds", get_government_bonds),
        ("Funds", get_funds),
        ("Cryptocurrencies", get_cryptocurrencies)]

    for widget in button_frame.winfo_children():
        widget.destroy()

    for text, command in market_buttons:
        button = ctk.CTkButton(button_frame, text=text, width=290, height=25, anchor='right', font=('Helvetica', 18, 'bold'))
        button.pack(padx=20, ipady=(5), pady=(10, 0))
        button.configure(command=lambda cmd=command: [show_treeview(), cmd(), set_current_webscraping_function(cmd)])

    refresh_button = ctk.CTkButton(button_frame, text="Clear Screen", width=290, height=100, anchor='right', font=('Helvetica', 40, 'bold'), fg_color='#294f73', hover_color='#1d8ab5')
    refresh_button.pack(padx=20, pady=(210, 10))
    refresh_button.configure(command=lambda: clear_treeview(tree))
    refresh_button.configure(command=lambda: [clear_treeview(tree), search_bar.delete(0, 'end')])
    refresh_button.configure(command=lambda: [clear_treeview(tree), search_bar.delete(0, 'end'), search_bar.insert(0, "Enter number")])

    back_button = ctk.CTkButton(button_frame, text="Main Menu", width=290, height=100, anchor='right', font=('Helvetica', 45, 'bold'), fg_color='#294f73', hover_color='#1d8ab5')
    back_button.pack(padx=20, pady=(0, 20))
    back_button.configure(command=lambda: return_to_main_page())

def set_current_webscraping_function(function):
    global current_webscraping_function
    current_webscraping_function = function

# MAIN PAGE CODE ==========================================================================================================

def return_to_main_page():
    treeview_frame.pack_forget()
    for widget in button_frame.winfo_children():
        widget.destroy()
    if transaction_frame is not None:
        transaction_frame.place_forget()

    main_buttons = ["Employees", "Market", "Music", "Exit"]
    for text in main_buttons:

        if text == "Employees":
            button = ctk.CTkButton(button_frame, text=text, width=290, height=100, anchor='center', font=('Helvetica', 45, 'bold'), fg_color='#174487', hover_color='#5391f5', bg_color='#1d1e1f')
            button.configure(command=lambda: os.system('python 2._employees.py'))
            button.pack(padx=20, pady=(20,0))
        elif text == "Market":
            button = ctk.CTkButton(button_frame, text=text, width=290, height=100, anchor='center', font=('Helvetica', 45, 'bold'), fg_color='#0f6961', hover_color='#19d1b9', bg_color='#1d1e1f')
            button.configure(command=lambda: show_market_buttons())
            button.pack(padx=20, pady=(20))
        elif text == "Music":
            button = ctk.CTkButton(button_frame, text=text, width=290, height=100, anchor='center', font=('Helvetica', 45, 'bold'), fg_color='#268717', hover_color='#59d119', bg_color='#1d1e1f')
            button.configure(command=lambda: os.system('python 4._music_player_Nessa.py'))
            button.pack(padx=20, pady=(0,20))
        elif text == "Exit":
            button = ctk.CTkButton(button_frame, text=text, width=290, height=100, anchor='center', font=('Helvetica', 45, 'bold'), fg_color='#8f9110', hover_color='#d1d119', bg_color='#1d1e1f')
            button.configure(command=lambda: root.destroy())
            button.pack(padx=20, pady=(0, 320))

root = ttk.Window(themename='darkly')  # Creating a tkinter window and customising it

root.wm_attributes('-alpha', 1)
root.title("The CEO Program")
root.geometry("1200x800+400+150")
root.resizable(False, False)

background_image = 'program files/main_page_background.jpg'
img = Image.open(background_image)
img = ImageTk.PhotoImage(img)
img_label = ttk.Label(root, image=img)
img_label.place(x=0, y=0, relwidth=1, relheight=1)

button_frame = ttk.Frame(root)
button_frame.place(relx=0, rely=0.5, anchor='w')

treeview_frame = ttk.Frame(root)
treeview_frame.pack(padx=(300, 7), pady=7, fill='both', expand=True)
tree = ttk.Treeview(treeview_frame, show='headings', style="Treeview")
scrollbar = ttk.Scrollbar(treeview_frame, orient='vertical', command=tree.yview)
scrollbar.pack(side='right', fill='y')
tree.config(yscrollcommand=scrollbar.set)
tree.pack(side='left', fill='both', expand=True)
treeview_frame.pack_forget()  # Initially hide the Treeview frame

return_to_main_page()
root.mainloop()