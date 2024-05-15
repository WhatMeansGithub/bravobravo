from bs4 import BeautifulSoup
import requests

url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'

page = requests.get(url)

soup = BeautifulSoup(page.text, features='lxml')
soup.find('table', class_='wikitable sortable')

table = soup.find('table', class_='wikitable sortable')



print(soup.prettify)

