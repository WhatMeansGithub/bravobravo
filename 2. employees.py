import re
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import datetime
import concurrent.futures
import smtplib
import dns.resolver

# Function to initialize Selenium WebDriver
def initialize_driver():
    options = Options()
    options.headless = True
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

def verify_email_smtp(email):
    try:
        if '@' not in email:
            print(f"Invalid email format: {email}")
            return False
        
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        
        if not mx_records:
            print(f"No MX records found for domain: {domain}")
            return False
        
        mx_record = str(mx_records[0].exchange)
        
        smtp_user = os.getenv('SMTP_USER')
        smtp_password = os.getenv('SMTP_PASSWORD')

        if not smtp_user or not smtp_password:
            print("SMTP credentials are not in environment variables.")
            return False

        # Use Gmail SMTP server for checking
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.mail(smtp_user)
        code, message = server.rcpt(email)
        server.quit()
        
        if code == 250:
            return True
        else:
            print(f"SMTP server responded with code: {code}, message: {message}")
            return False
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        print(f"DNS resolution error for domain: {domain}")
        return False
    except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError, smtplib.SMTPHeloError) as e:
        print(f"SMTP connection error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during SMTP verification: {e}")
        return False

# Testing the function
email = "example@example.com"
is_valid = verify_email_smtp(email)
print(f"Email {email} validation result: {is_valid}")
    
# Function to scrape data from the main page
def scrape_main_page(page_url):
    driver = initialize_driver()
    driver.get(page_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-profileImage')))
    profiles = driver.find_elements(By.CSS_SELECTOR, '.m-profileImage')
    data = []
    for profile in profiles:
        name = profile.find_element(By.CLASS_NAME, 'm-profileImage__name').text.strip()
        job_title = profile.find_element(By.CLASS_NAME, 'm-profileImage__jobDescription').text.strip()
        profile_link = profile.get_attribute('href')
        data.append({'Name': name, 'Job Title': job_title, 'Profile Link': profile_link})
    driver.quit()
    return data

# Function to scrape data from a profile page
def scrape_profile_page(profile):
    driver = initialize_driver()
    profile_url = profile['Profile Link']
    driver.get(profile_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'a-mailto')))
    email_elem = driver.find_element(By.CLASS_NAME, 'a-mailto')
    email = email_elem.get_attribute('href')
    if email.startswith("mailto:"):
        email = email.split(":")[1]
    else:
        email = email_elem.text.strip()
    
          # SMTP validation
    if not verify_email_smtp(email):
        email = 'Email does not exist'

    phone_elem = driver.find_element(By.XPATH, "//a[starts-with(@href, 'tel:')]")
    phone = phone_elem.get_attribute('href').split(":")[1]
    driver.quit()
    profile.update({'Email': email, 'Phone Number': phone})
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
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        main_page_futures = [executor.submit(scrape_main_page, f"https://www.epunkt.com/team/p{num}") for num in page_numbers]
        for future in concurrent.futures.as_completed(main_page_futures):
            profiles_data.extend(future.result())

        profile_page_futures = [executor.submit(scrape_profile_page, profile) for profile in profiles_data]
        profiles_data = [future.result() for future in concurrent.futures.as_completed(profile_page_futures) if future.result() is not None]

    print("Data fetching complete")
    update_treeview()

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
for col in columns:
    tree.heading(col, text=col)
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