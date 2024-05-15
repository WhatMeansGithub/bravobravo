import time
from selenium import webdriver
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Function to scrape profile links using Selenium
def scrape_profile_links(main_page_url):
    print("Fetching main page:", main_page_url)
    driver = webdriver.Firefox()
    driver.get(main_page_url)

    # Wait for elements to be loaded (adjust timeout as needed)
    print("Waiting for elements to be loaded...")
    wait = WebDriverWait(driver, 20)
    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.m-profileImage')))
    except TimeoutException:
        print("Timeout occurred while waiting for elements to load.")
        return []

    print("Main page loaded successfully")

    # Find profile links
    profile_links = []
    for element in elements:
        profile_links.append(element.get_attribute('href'))

    driver.quit()
    print("WebDriver closed")
    print("Number of profile links found:", len(profile_links))
    return profile_links


# Create Tkinter GUI
root = tk.Tk()
root.title("Scraped Data")

# Function to update GUI with scraped data
def update_gui():
    print("Updating GUI...")
    scraped_data = []
    profile_urls = scrape_profile_links('https://www.epunkt.com/team')
    print("Profile URLs:", profile_urls)
    for profile_url in profile_urls:
        profile_data = scrape_profile(profile_url)
        scraped_data.append(profile_data)

    # Convert scraped data to DataFrame
    df = pd.DataFrame(scraped_data)

    # Display DataFrame in Treeview
    tree.delete(*tree.get_children())  # Clear existing data in Treeview
    for index, row in df.iterrows():
        tree.insert('', 'end', values=(row['Name'], row['Job Title'], row['Email'], row['Phone Number']))
    print("GUI updated successfully")

# Create Treeview to display scraped data
columns = ('Name', 'Job Title', 'Email', 'Phone Number')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill='both', expand=True)

# Button to update and display scraped data
update_button = tk.Button(root, text="Update Data", command=update_gui)
update_button.pack()

# Button to copy selected data
def copy_selected():
    selected_item = tree.selection()
    if selected_item:
        selected_values = tree.item(selected_item)['values']
        root.clipboard_clear()
        root.clipboard_append(selected_values)

copy_button = tk.Button(root, text="Copy Selected", command=copy_selected)
copy_button.pack()

# Run the GUI
root.mainloop()
