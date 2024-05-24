import pandas as pd
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
<<<<<<< HEAD
from selenium.webdriver.chrome.options import Options
=======
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
>>>>>>> 1a09e3a1b7db0d1e6a1ac1056c1752b6e067b112
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import datetime
import os

# Function to initialize WebDriver
def initialize_driver():
    try:
        # Attempt to use Firefox
        firefox_options = FirefoxOptions()
        firefox_options.headless = False
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(options=firefox_options)
        print("Using Firefox WebDriver")
    except Exception as e:
        print(f"Failed to initialize Firefox WebDriver: {e}")
        try:
            # Attempt to use Chrome
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            print("Using Chrome WebDriver")
        except Exception as e:
            print(f"Failed to initialize Chrome WebDriver: {e}")
            raise RuntimeError("No suitable WebDriver found. Please ensure you have either geckodriver or chromedriver installed.")
    return driver

# Function to scrape data from the main page
<<<<<<< HEAD
def scrape_main_page(driver, page_url):
    driver.get(page_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-profileImage')))  # This tells the webdriver to wait 10 seconds until the css element ".m-profileimage" is loaded
    profiles = driver.find_elements(By.CSS_SELECTOR, '.m-profileImage')                                    # This allows us to access and manipulate the selected elements later     
    data = []                                                                                              # Creates an empty list for data 
    for profile in profiles:
=======
def scrape_main_page(driver, page_url):                                                                      
    driver.get(page_url)                                                                                    
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-profileImage')))    
    profiles = driver.find_elements(By.CSS_SELECTOR, '.m-profileImage')                                     
    data = []                                                                                               
    for profile in profiles:                                                                                
>>>>>>> 1a09e3a1b7db0d1e6a1ac1056c1752b6e067b112
        name = profile.find_element(By.CLASS_NAME, 'm-profileImage__name').text.strip()
        job_title = profile.find_element(By.CLASS_NAME, 'm-profileImage__jobDescription').text.strip()
        profile_link = profile.get_attribute('href')                                                        
        data.append({'Name': name, 'Job Title': job_title, 'Profile Link': profile_link})                   
    return data

# Function to scrape data from a profile page
def scrape_profile_page(driver, profile_url):
    driver.get(profile_url)                                                                                 
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'a-mailto')))             
    email_elem = driver.find_element(By.CLASS_NAME, 'a-mailto')                                             
    email = email_elem.get_attribute('href')
<<<<<<< HEAD
    if email.startswith("mailto:"):                                                             # Checks whether the email variable starts with "mailto"
        email = email.split(":")[1]                                                             # Splits the string each time it encounters a ":", the "[1]" refers to the second item in the list       
=======
    if email.startswith("mailto:"):
        email = email.split(":")[1]                                 # Splits the string each time it encounters a ":", the "[1]" refers to the second item in the list
>>>>>>> 1a09e3a1b7db0d1e6a1ac1056c1752b6e067b112
    else:
        email = email_elem.text.strip()
    phone_elem = driver.find_element(By.XPATH, "//a[starts-with(@href, 'tel:')]")
    phone = phone_elem.get_attribute('href').split(":")[1]
    return {'Email': email, 'Phone Number': phone}

# Function to export data to CSV file with a unique name
def export_to_csv(data):
    if not os.path.exists('employees files'):                                                               
        os.makedirs('employees files')                                                                      
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")                                             
    filename = os.path.join('employees files', f"profiles_{timestamp}.csv")                                 
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    messagebox.showinfo('Export Successful', f'Data exported to {filename}!')

# Function to update the GUI with scraped data
def update_gui(page_num=None):
    global profiles_data
    profiles_data = []
    if page_num is None or page_num.strip() == "":
        page_numbers = range(1, 12)  # Gets pages 1-11 from the website if there's no input for page numbers
    else:
        try:
            page_numbers = [int(page_num)]
        except ValueError:
            messagebox.showwarning('Invalid Input', 'Please enter a valid page number.')
            return
    
    driver = initialize_driver()
    for num in page_numbers:
        print(f"Fetching data from page {num}")                                   # print statement to check if the program hangs fetching a certain page
        page_url = f"https://www.epunkt.com/team/p{num}"
<<<<<<< HEAD
        profiles_data += scrape_main_page(driver, page_url)
        for profile in profiles_data:
            profile.update(scrape_profile_page(driver, profile['Profile Link']))  # Update with email and phone
=======
        page_data = scrape_main_page(driver, page_url)  # Use a temporary list to store the current page data
        for profile in page_data:
            profile.update(scrape_profile_page(driver, profile['Profile Link']))
        profiles_data += page_data  # Merge the current page data into the main profiles_data list
>>>>>>> 1a09e3a1b7db0d1e6a1ac1056c1752b6e067b112
    print("Data fetching complete")
    update_treeview()
    driver.quit


# Function to update the Treeview with scraped data
def update_treeview():
    tree.delete(*tree.get_children())
    for profile in profiles_data:
        tree.insert('', 'end', values=(profile['Name'], profile['Job Title'], profile['Profile Link'], profile['Email'], profile['Phone Number']))

# Function to export selected profiles to CSV file
def export_selected():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning('No Selection', 'Please select at least one profile to export.')
        return
    selected_profiles = []
    for item in selected_items:
        profile_id = item[1:]  # Remove the "I" prefix
        try:
            index = int(profile_id) - 1
            if 0 <= index < len(profiles_data):
                selected_profiles.append(profiles_data[index])
            else:
                print(f"Index {index} out of range. Skipping.")
        except ValueError:
            print(f"Cannot convert {profile_id} to integer. Skipping.")
    if selected_profiles:
        export_to_csv(selected_profiles)

# Function to export all profiles to CSV file
def export_all():
    export_to_csv(profiles_data)

# Function to copy selected profiles to clipboard
def copy_selected():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning('No Selection', 'Please select at least one profile to export.')
        return
    selected_profiles = []
    for item in selected_items:
        profile_id = item[1:]  # Remove the "I" prefix
        try:
            index = int(profile_id) - 1
            if 0 <= index < len(profiles_data):
                selected_profiles.append(profiles_data[index])
            else:
                print(f"Index {index} out of range. Skipping.")
        except ValueError:
            print(f"Cannot convert {profile_id} to integer. Skipping.")
    pyperclip.copy(str(selected_profiles))
    messagebox.showinfo('Copy Successful', 'Selected profiles copied to clipboard!')

# Function to copy all profiles to clipboard
def copy_all():
    pyperclip.copy(str(profiles_data))
    messagebox.showinfo('Copy Successful', 'All profiles copied to clipboard!')

<<<<<<< HEAD
# Initialize Selenium WebDriver
options = Options()
options.headless = True
options.add_argument("--headless")  # Add this line to run the browser in headless mode
driver = webdriver.Chrome(options=options)
=======
# Function to sort the Treeview column
def sort_column(col):
    global profiles_data
    profiles_data.sort(key=lambda x: x[col], reverse=sort_orders[col])
    sort_orders[col] = not sort_orders[col]
    update_treeview()

# Initialize customtkinter GUI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
>>>>>>> 1a09e3a1b7db0d1e6a1ac1056c1752b6e067b112

root = ctk.CTk()
root.title("Scraped Profiles")
# Style for Treeview
style = ttk.Style()
style.theme_use("clam")  # set the theme to use for ttk

# Customize the Treeview
style.configure("Treeview",
                background="#2e2e2e",
                foreground="white",
                rowheight=25,
                fieldbackground="#2e2e2e")

style.map('Treeview', background=[('selected', '#5a5a5a')])

# Customize the Treeview headings
style.configure("Treeview.Heading",
                background="#1FA557",
                foreground="white",
                relief="flat")

style.map("Treeview.Heading",
          background=[('active', '#14702B')])

# Label and Entry for page number input
page_number_label = ctk.CTkLabel(root, text="Page Number:")
page_number_label.pack(pady=5)
page_number_entry = ctk.CTkEntry(root, placeholder_text="Input page number...")
page_number_entry.pack(pady=5)

# Create Treeview to display scraped data using ttk
columns = ('Name', 'Job Title', 'Profile Link', 'Email', 'Phone Number')
<<<<<<< HEAD
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill='both', expand=True)
=======
tree = ttk.Treeview(root, columns=columns, show='headings', style="Treeview")
sort_orders = {col: False for col in columns}  # Dictionary to keep track of sort orders

for col in columns:
    tree.heading(col, text=col, command=lambda _col=col: sort_column(_col))
tree.pack(fill='both', expand=True, pady=5)

# Container frame for the buttons
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)

# Uniform button style
button_style = {"corner_radius": 10, "fg_color": "#1FA557", "hover_color": "#14702B", "text_color": "#ffffff"}
>>>>>>> 1a09e3a1b7db0d1e6a1ac1056c1752b6e067b112

# Button to update and display scraped data
update_button = ctk.CTkButton(button_frame, text="Gimme the Juice", command=lambda: update_gui(page_number_entry.get()), **button_style)
update_button.pack(side="left", padx=5)

# Button to export selected data
export_selected_button = ctk.CTkButton(button_frame, text="Export Selected", command=export_selected, **button_style)
export_selected_button.pack(side="left", padx=5)

# Button to export all data
export_all_button = ctk.CTkButton(button_frame, text="Export All", command=export_all, **button_style)
export_all_button.pack(side="left", padx=5)

# Button to copy selected data
copy_selected_button = ctk.CTkButton(button_frame, text="Copy Selected", command=copy_selected, **button_style)
copy_selected_button.pack(side="left", padx=5)

# Button to copy all data
copy_all_button = ctk.CTkButton(button_frame, text="Copy All", command=copy_all, **button_style)
copy_all_button.pack(side="left", padx=5)

# Run the GUI
root.mainloop()



