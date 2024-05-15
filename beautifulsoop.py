import time
import re
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
def scrape_profile_page(driver, profile_url):
    driver.get(profile_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'a-mailto')))
    email = driver.find_element(By.CLASS_NAME, 'a-mailto').text.strip()
    phone = re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', driver.page_source).group(0)
    return {'Email': email, 'Phone Number': phone}

# Function to export data to CSV file
def export_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    messagebox.showinfo('Export Successful', f'Data exported to {filename}!')

# Function to update the GUI with scraped data
def update_gui():
    global profiles_data
    profiles_data = []
    for page_num in range(1, 12):  # Assuming 11 pages in total
        page_url = f"https://www.epunkt.com/team/p{page_num}"
        profiles_data += scrape_main_page(driver, page_url)
    update_treeview()

# Function to update the Treeview with scraped data
def update_treeview():
    tree.delete(*tree.get_children())
    for profile in profiles_data:
        tree.insert('', 'end', values=(profile['Name'], profile['Job Title'], profile['Profile Link']))

# Function to export selected profiles to CSV file
def export_selected():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning('No Selection', 'Please select at least one profile to export.')
        return
    selected_profiles = [profiles_data[int(item)-1] for item in selected_items]
    export_to_csv(selected_profiles, 'selected_profiles.csv')

# Function to export all profiles to CSV file
def export_all():
    export_to_csv(profiles_data, 'all_profiles.csv')

# Initialize Selenium WebDriver
driver = webdriver.Firefox()

# Initialize tkinter GUI
root = tk.Tk()
root.title("Scraped Profiles")

# Create Treeview to display scraped data
columns = ('Name', 'Job Title', 'Profile Link')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill='both', expand=True)

# Button to update and display scraped data
update_button = tk.Button(root, text="Update Data", command=update_gui)
update_button.pack()

# Button to export selected data
export_selected_button = tk.Button(root, text="Export Selected", command=export_selected)
export_selected_button.pack()

# Button to export all data
export_all_button = tk.Button(root, text="Export All", command=export_all)
export_all_button.pack()

# Run the GUI
root.mainloop()

# Quit Selenium WebDriver
driver.quit()
