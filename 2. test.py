import re
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import datetime
import concurrent.futures

# Function to scrape data from the main page
def scrape_main_page(driver, page_url):
    driver.get(page_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-profileImage')))
    profiles = driver.find_elements(By.CSS_SELECTOR, '.m-profileImage')
    data = []
    for profile in profiles:
        name = profile.find_element(By.CLASS_NAME, 'm-profileImage__name').text.strip()
        job_title = profile.find_element(By.CLASS_NAME, 'm-profileImage__jobDescription').text.strip()
        profile_link = profile.get_attribute('href')
        data.append({'Name': name, 'Job Title': job_title, 'Profile Link': profile_link})
    return data

# Function to scrape data from a profile page
def scrape_profile_page(profile):
    profile_url = profile['Profile Link']
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    try:
        driver.get(profile_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'a-mailto')))
        email_elem = driver.find_element(By.CLASS_NAME, 'a-mailto')
        email = email_elem.get_attribute('href')
        if email.startswith("mailto:"):
            email = email.split(":")[1]
        else:
            email = email_elem.text.strip()
        phone_elem = driver.find_element(By.XPATH, "//a[starts-with(@href, 'tel:')]")
        phone = phone_elem.get_attribute('href').split(":")[1]
        profile.update({'Email': email, 'Phone Number': phone})
    except Exception as e:
        print(f"Failed to scrape profile page {profile_url}: {e}")
    finally:
        driver.quit()
    return profile

# Function to export data to CSV file with a unique name
def export_to_csv(data):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"profiles_{timestamp}.csv"
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    messagebox.showinfo('Export Successful', f'Data exported to {filename}!')

# Function to update the GUI with scraped data
def update_gui(page_num=None):
    global profiles_data
    profiles_data = []
    if page_num is None or page_num.strip() == "":
        page_numbers = range(1, 12)
    else:
        try:
            page_numbers = [int(page_num)]
        except ValueError:
            messagebox.showwarning('Invalid Input', 'Please enter a valid page number.')
            return
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_page = {executor.submit(fetch_page_data, num): num for num in page_numbers}
        for future in concurrent.futures.as_completed(future_to_page):
            profiles_data.extend(future.result())
    
    print("Main page data fetching complete")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        profiles_data = list(executor.map(scrape_profile_page, profiles_data))
    
    print("Profile data fetching complete")
    update_treeview()

def fetch_page_data(page_num):
    page_url = f"https://www.epunkt.com/team/p{page_num}"
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    try:
        return scrape_main_page(driver, page_url)
    except Exception as e:
        print(f"Failed to fetch data from page {page_num}: {e}")
        return []
    finally:
        driver.quit()

# Function to update the Treeview with scraped data
def update_treeview():
    tree.delete(*tree.get_children())
    for profile in profiles_data:
        tree.insert('', 'end', values=(profile['Name'], profile['Job Title'], profile['Profile Link'], profile.get('Email', ''), profile.get('Phone Number', '')))

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

# Function to sort the Treeview column
def sort_column(col):
    global profiles_data
    profiles_data.sort(key=lambda x: x[col], reverse=sort_orders[col])
    sort_orders[col] = not sort_orders[col]
    update_treeview()

# Initialize Selenium WebDriver
options = Options()
options.headless = True
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

# Initialize tkinter GUI
root = tk.Tk()
root.title("Scraped Profiles")

# Label and Entry for page number input
page_number_label = tk.Label(root, text="Page Number:")
page_number_label.pack()
page_number_entry = tk.Entry(root)
page_number_entry.pack()

# Create Treeview to display scraped data
columns = ('Name', 'Job Title', 'Profile Link', 'Email', 'Phone Number')
tree = ttk.Treeview(root, columns=columns, show='headings')
sort_orders = {col: False for col in columns}  # Dictionary to keep track of sort orders

for col in columns:
    tree.heading(col, text=col, command=lambda _col=col: sort_column(_col))
tree.pack(fill='both', expand=True)

# Button to update and display scraped data
update_button = tk.Button(root, text="Gimme the Juice", command=lambda: update_gui(page_number_entry.get()))
update_button.pack()

# Button to export selected data
export_selected_button = tk.Button(root, text="Export Selected", command=export_selected)
export_selected_button.pack()

# Button to export all data
export_all_button = tk.Button(root, text="Export All", command=export_all)
export_all_button.pack()

# Button to copy selected data
copy_selected_button = tk.Button(root, text="Copy Selected", command=copy_selected)
copy_selected_button.pack()

# Button to copy all data
copy_all_button = tk.Button(root, text="Copy All", command=copy_all)
copy_all_button.pack()

# Run the GUI
root.mainloop()

# Quit Selenium WebDriver
driver.quit()
