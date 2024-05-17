from bs4 import BeautifulSoup  # importing BeautifulSoup so we can use it to take the requested information from the HTML content of the website
import requests                # Importing requests so we can request the HTML content of the website
import os

clear = lambda: os.system('clear') # This function is used to clear the output of the terminal
clear()                            # Clearing the terminal every time cuz its annoying doing it manually

url1 = 'https://www.investing.com/'         # URL of the website we want to scrape
page1 = requests.get(url1)                        # Requesting the HTML content of the website under the variable name page ofr later use
soup1 = BeautifulSoup(page1.text, 'html.parser')  # Parsing the HTML content of the website (taking the html code in the form of text) 

all_titles = soup1.find_all('table' , class_="datatable-v2_table__93S4Y dynamic-table-v2_dynamic-table__iz42m datatable-v2_table--mobile-basic__uC0U0 datatable-v2_table--freeze-column__uGXoD datatable-v2_table--freeze-column-first__zMZNN undefined")
all_titles = [title.text.strip() for title in all_titles]                         # Stripping the pure text of the titles and adding them to a list
useful_titles = all_titles[3:10]                                                  # Adding only the titles we need to the list of useful_titles
# print(", ".join(useful_titles))

import pandas as pd
df = pd.DataFrame(columns = useful_titles)
print(df)

more_content = soup1.find_all("a",{"class":"basic-table__link-B1P_UJ cnn-pcl-fyz6fg"}) # Extracting the titles of all tables from the website
print(more_content)




