import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
from tkinter import ttk
import pandas as pd

# Function to scrape main page and extract profile links
def scrape_main_page(main_page_url):
    response = requests.get(main_page_url)
    print("Main Page Status Code:", response.status_code)  # Print status code for debugging
    soup = BeautifulSoup(response.content, 'html.parser')
    
    profile_links = []
    profiles = soup.find_all('a', class_='o-employeeList__item')
    print("Number of Profile Links Found:", len(profiles))  # Print number of profile links found for debugging
    for profile in profiles:
        profile_links.append(profile['href'])
    
    return profile_links

# Function to scrape profile page and extract information
def scrape_profile(profile_url):
    response = requests.get(profile_url)
    print("Profile Page Status Code:", response.status_code)  # Print status code for debugging
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract name
    name_elem = soup.find('h1', class_='o-employeeIntro__name')
    name = name_elem.text.strip() if name_elem else ''
    
    # Extract job title
    job_title_elem = soup.find('div', class_='o-employeeIntro__jobDescription')
    job_title = job_title_elem.text.strip() if job_title_elem else ''
    
    # Extract email
    email_link = soup.find('a', class_='a-mailto')
    email = re.search(r'mailto:(.*)', email_link['href']).group(1) if email_link else ''
    
    # Extract phone number (if available)
    phone_number_elem = soup.find('div', class_='o-employeeIntro__contactbox')
    phone_number = phone_number_elem.text.strip() if phone_number_elem else ''
    
    # Return the scraped data
    return {'Name': name, 'Job Title': job_title, 'Email': email, 'Phone Number': phone_number}

# Create Tkinter GUI
root = tk.Tk()
root.title("Scraped Data")

# Function to update GUI with scraped data
def update_gui():
    scraped_data = []
    profile_urls = scrape_main_page('https://www.epunkt.com/team')
    for profile_url in profile_urls:
        profile_data = scrape_profile(profile_url)
        scraped_data.append(profile_data)
    
    # Convert scraped data to DataFrame
    df = pd.DataFrame(scraped_data)
    
    # Display DataFrame in Treeview
    tree.delete(*tree.get_children())  # Clear existing data in Treeview
    for index, row in df.iterrows():
        tree.insert('', 'end', values=(row['Name'], row['Job Title'], row['Email'], row['Phone Number']))

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
