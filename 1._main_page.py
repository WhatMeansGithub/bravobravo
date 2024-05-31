import json
from tkinter import messagebox
import tkinter as tk                    # Importing tkinter as tk to create the GUI
import ttkbootstrap as ttk              # Does the same as 'from tkinter import ttk' but lets us customize the GUI even more with themes
from tkinter import font as tkFont      # Importing font as tkFont to customize the font of the GUI
from PIL import Image, ImageTk          # Importing Image and ImageTk from PIL to display images in the GUI
import customtkinter as ctk             # Importing customtkinter as ctk to create custom buttons
import os                               # Importing os to run the python files of the other pages
import requests                         # Importing requests to get HTML content from a website
from bs4 import BeautifulSoup           # Importing BeautifulSoup to parse HTML content
import pandas as pd                     # Importing pandas for data manipulation and file saving


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
            try:                                                    # using try and except because Markus said so
                print(df)                                               # Display DataFrame
                combined_string += df.to_string() + "\n\n"              # Append the string representation of the DataFrame to the combined string
                update_treeview(tree, headers, rows)
            except:
                print("Error displaying the table.")
    else:
        print("No table found with the specified class.")  

def get_indices():
    url = 'https://www.investing.com/indices/major-indices'         
    page = requests.get(url)                                        
    soup = BeautifulSoup(page.text, 'html.parser')                  
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'indices')

def get_trending_stocks():
    url = 'https://www.investing.com/equities/trending-stocks'      
    page = requests.get(url)                                        
    soup = BeautifulSoup(page.text, 'html.parser')                  
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'trending_stocks')

def get_commodity_futures():
    url = 'https://www.investing.com/commodities/real-time-futures' 
    page = requests.get(url)                                        
    soup = BeautifulSoup(page.text, 'html.parser')                  
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'commodity_futures')

def get_exchange_rates():
    url = 'https://www.investing.com/currencies/streaming-forex-rates-majors'
    page = requests.get(url)                                        
    soup = BeautifulSoup(page.text, 'html.parser')                  
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'exchange_rates')

def get_etfs():
    url = 'https://www.investing.com/etfs/major-etfs'               
    page = requests.get(url)                                        
    soup = BeautifulSoup(page.text, 'html.parser')                  
    display_web_tables(soup, 'genTbl closedTbl crossRatesTbl elpTbl elp40', 'etfs')

def get_government_bonds():
    url = 'https://www.investing.com/rates-bonds/world-government-bonds'
    page = requests.get(url)                                        
    soup = BeautifulSoup(page.text, 'html.parser')                  
    display_web_tables(soup, 'genTbl closedTbl crossRatesTbl', 'government_bonds')

def get_funds():
    url = 'https://www.investing.com/funds/major-funds'             
    page = requests.get(url)                                        
    soup = BeautifulSoup(page.text, 'html.parser')                  
    display_web_tables(soup, 'genTbl closedTbl crossRatesTbl elpTbl elp40', 'funds')

def get_cryptocurrencies():
    url = 'https://markets.businessinsider.com/cryptocurrencies'    
    page = requests.get(url)                                        
    soup = BeautifulSoup(page.text, 'html.parser')                  
    display_web_tables(soup, 'table table--col-1-font-color-black table--suppresses-line-breaks table--fixed', 'cryptocurrencies')

def update_treeview(tree, headers, rows):
    tree.delete(*tree.get_children())
    tree["columns"] = ["Index"] + headers                           # Add "Index" as the first column
    tree.heading("Index", text="Index")                             # Set the heading for the "Index" column
    tree.column("Index", anchor='w', width=50, stretch=False)       # Set the width of the "Index" column and disable stretching

    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, anchor='center', width=120, minwidth=120, stretch=True)
    for i, row in enumerate(rows, start=1):
        tree.insert("", "end", values=[i] + row)                   # Add the index as the first value in each row

def clear_treeview(tree):
    tree.delete(*tree.get_children())
    tree["columns"] = []  # Clear the column headers
    tree.heading("#0", text="")  # Clear the heading of the first column

root = ttk.Window(themename = 'darkly')                             # Creating a tkinter window and customising it

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

def show_treeview():
    treeview_frame.pack(padx=(330, 0), pady=0, fill='both', expand=True)

def hide_treeview():
    treeview_frame.pack_forget()

def show_market_buttons():
    show_transaction_buttons()

    market_buttons = [
        ("Indices", get_indices),
        ("Trending Stocks", get_trending_stocks),
        ("Commodity Futures", get_commodity_futures),
        ("Exchange Rates", get_exchange_rates),
        ("ETFs", get_etfs),
        ("Government Bonds", get_government_bonds),
        ("Funds", get_funds),
        ("Cryptocurrencies", get_cryptocurrencies)]

    for widget in button_frame.winfo_children():
        widget.destroy()

    for text, command in market_buttons:
        button = ctk.CTkButton(button_frame, text=text, width=290, height=30, anchor='right', font=('Helvetica', 18, 'bold'))
        button.pack(padx=20, ipady=(5), pady=(5, 0))
        button.configure(command=lambda cmd=command: [show_treeview(), cmd()])

    back_button = ctk.CTkButton(button_frame, text="Main Menu", width=290, height=100, anchor='right', font=('Helvetica', 30, 'bold'), fg_color='#294f73', hover_color='#1d8ab5')
    back_button.pack(padx=20, pady=(320, 20))
    back_button.configure(command=lambda: reset_main_buttons())

def reset_main_buttons():
    for widget in button_frame.winfo_children():
        widget.destroy()
    hide_treeview()

    main_buttons = ["Employees", "Market", "Music", "Exit"]
    for text in main_buttons:
        button = ctk.CTkButton(button_frame, text=text, width=290, height=100, anchor='center', font=('Helvetica', 30, 'bold'), fg_color='#294f73', hover_color='#1d8ab5')  # 
        button.pack(padx=20, pady=50)
        if text == "Employees":
            button.configure(command=lambda: os.system('python 2._employees.py'))
        elif text == "Market":
            button.configure(command=lambda: show_market_buttons())
        elif text == "Music":
            button.configure(command=lambda: os.system('python 4._music_player_Nessa.py'))
        elif text == "Exit":
            button.configure(command=lambda: root.destroy())

# Stock data file
stock_data_file = 'stock_data.json'

# Initialize stock data
if os.path.exists(stock_data_file):
    with open(stock_data_file, 'r') as file:
        stock_data = json.load(file)
else:
    stock_data = {}

# Add BUY and SELL buttons and search bar
transaction_frame = ttk.Frame(root)
transaction_frame.pack(pady=(0, 20))

def save_stock_data():
    market_files_dir = 'market files'
    if not os.path.exists(market_files_dir):
        os.makedirs(market_files_dir)
    stock_data_file = os.path.join(market_files_dir, 'owned_stocks.json')
    with open(stock_data_file, 'w') as file:
        json.dump(stock_data, file)

def show_transaction_buttons():
    def buy_stocks():
        try:
            amount = int(search_bar.get())
            selected_items = tree.selection()
            if selected_items:
                for item in selected_items:
                    stock_name = tree.item(item, 'values')[0]
                    if stock_name not in stock_data:
                        stock_data[stock_name] = 0
                    stock_data[stock_name] += amount
                save_stock_data()
                messagebox.showinfo("Transaction Successful", f"Bought {amount} of each selected stock")
            else:
                messagebox.showwarning("No Selection", "Please select a stock to buy.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
 
    def sell_stocks():
        try:
            amount = int(search_bar.get())
            selected_items = tree.selection()
            if selected_items:
                for item in selected_items:
                    stock_name = tree.item(item, 'values')[0]
                    if stock_name in stock_data:
                        stock_data[stock_name] -= amount
                        if stock_data[stock_name] <= 0:
                            del stock_data[stock_name]
                            messagebox.showinfo("Transaction Successful", f"All stocks from {stock_name} are sold.")
                        else:
                            messagebox.showinfo("Transaction Successful", f"Sold {amount} of {stock_name}")
                save_stock_data()
            else:
                messagebox.showwarning("No Selection", "Please select a stock to sell.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    search_bar = ttk.Entry(transaction_frame)
    search_bar.pack(side='bottom', padx=5, pady=(0,5), fill='x')
    search_bar.insert(0, "Enter number")

    buy_button = ctk.CTkButton(transaction_frame, text="BUY", width=100, height=50, fg_color="green", command=buy_stocks)
    buy_button.pack(side='left', padx=(5,0), pady=5)

    sell_button = ctk.CTkButton(transaction_frame, text="SELL", width=100, height=50, fg_color="red", command=sell_stocks)
    sell_button.pack(side='left', padx=5, pady=5)

reset_main_buttons()
root.mainloop()