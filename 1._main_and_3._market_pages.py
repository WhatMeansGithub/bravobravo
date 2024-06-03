import json
from tkinter import messagebox
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import customtkinter as ctk
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# MARKET CODE =============================================================================================================

transaction_frame = None  # Define the "transaction_frame" variable
current_table = ""  # Track the current active table
current_webscraping_function = None  # Track the current webscraping function

def display_web_tables(soup, table_class, function_name):
    global current_table
    current_table = function_name  # Set the current active table
    tables = soup.find_all('table', class_=table_class)  # Find all tables with the specified class
    if tables:  # If at least one table is found
        combined_string = ""  # Create a string to store the text representation of all DataFrames
        if not os.path.exists('market files'):  # if the folder 'market' doesn't exist
            os.makedirs('market files')  # Create the folder 'market'
        combined_df = pd.DataFrame()  # DataFrame to hold all tables
        for i, table in enumerate(tables):  # Loop through each found table
            headers = [header.text.strip() for header in table.find_all('th')]  # Extract all headers from currently accessed table
            rows = []  # Create an empty list to store rows
            for row in table.find_all('tr')[1:]:  # Loop through each row (excluding the header row)
                columns = row.find_all('td')  # Extract columns from the row
                rows.append([col.text.strip() for col in columns])  # Append cleaned text to rows list
            df = pd.DataFrame(rows, columns=headers)  # Create DataFrame from headers and rows
            df.index = df.index + 1  # Increment index by 1 so it starts from 1 not 0
            file_name = f'{function_name}_{i+1}.csv'  # Save DataFrame to CSV file in the 'market' folder
            file_path = os.path.join('market files', file_name)  # Create the file path
            df.to_csv(file_path, index=False, mode='w')  # Save the DataFrame to the file path
            print(df)  # Display DataFrame
            combined_string += df.to_string() + "\n\n"  # Append the string representation of the DataFrame to the combined string
            combined_df = pd.concat([combined_df, df], ignore_index=True)  # Combine all tables into one DataFrame
        update_treeview(tree, combined_df.columns.tolist(), combined_df.values.tolist())
    else:
        print("No table found with the specified class.")  

def get_indices():
    url = 'https://www.investing.com/indices/major-indices'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    display_web_tables(soup, 'datatable-v2_table__93S4Y', 'indices')

def get_trending():
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

def load_stock_data(table_name):
    market_files_dir = 'market files'
    stock_data_file = os.path.join(market_files_dir, f'{table_name}_stocks.json')
    if os.path.exists(stock_data_file):
        with open(stock_data_file, 'r') as file:
            return json.load(file)
    return {}

def save_stock_data(table_name, stock_data):
    market_files_dir = 'market files'
    if not os.path.exists(market_files_dir):
        os.makedirs(market_files_dir)
    stock_data_file = os.path.join(market_files_dir, f'{table_name}_stocks.json')
    with open(stock_data_file, 'w') as file:
        json.dump(stock_data, file)

def update_treeview(tree, headers, rows):
    tree.delete(*tree.get_children())
    stock_data = load_stock_data(current_table)  # Load current stock data
    tree["columns"] = ["Index", "Stock Count"] + headers  # Add "Index" and "Stock Count" as the first columns
    tree.heading("Index", text="Index")  # Set the heading for the "Index" column
    tree.heading("Stock Count", text="Stock Count")  # Set the heading for the "Stock Count" column
    tree.column("Index", anchor='w', width=50, stretch=False)  # Set the width of the "Index" column and disable stretching
    tree.column("Stock Count", anchor='center', width=100, stretch=False)  # Set the width of the "Stock Count" column

    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, anchor='center', width=100, minwidth=50, stretch=True)
    for i, row in enumerate(rows, start=1):
        stock_index = row[0]  # Assume the first column uniquely identifies the stock
        stock_count = stock_data.get(str(i), 0)  # Get stock count for the current stock
        tree.insert("", "end", values=[i, stock_count] + row)  # Add the index and stock count as the first values in each row

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
        button = ctk.CTkButton(button_frame, text=text, width=290, height=100, anchor='center', font=('Helvetica', 50, 'bold'), fg_color='#294f73', hover_color='#1d8ab5')

        button.pack(padx=20, pady=(20))
        if text == "Employees":
            button.configure(command=lambda: os.system('python 2._employees.py'))
        elif text == "Market":
            button.configure(command=lambda: show_market_buttons())
            button.pack(pady=(0, 0))
        elif text == "Music":
            button.configure(command=lambda: os.system('python 4._music_player_Nessa.py'))
        elif text == "Exit":
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