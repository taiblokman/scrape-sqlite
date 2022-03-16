import sqlite3
import requests
from bs4 import BeautifulSoup

# scraping sand box, no pagination
start_url = 'https://books.toscrape.com'

# Get a page from url and pass it to bs4
def get_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features='html.parser')
    return soup

# parse the page and save the books info in a tuple within a list
# since the database already provides the column headers
def parse_page(soup):
    book_list = []
    article = soup.find_all('article', {'class': 'product_pod'})
    for books in article:
        title = books.find('img', {'class': 'thumbnail'})['alt']
        price = float(books.find('p', {'class': 'price_color'}).text.strip().replace('Â','').replace('£',''))
        stock = books.find('p', {'class': 'instock availability'}).text.strip()
        book_list.append((title,price,stock))   
    return book_list

# set up the run method
def main():
    # set up the database
    con = sqlite3.connect('books.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS books
                    (title text PRIMARY KEY, price real, stock text)''')    
    # start the job
    soup = get_page(start_url)
    book_list = parse_page(soup)
    print(book_list)
    
    # save the data into books db
    cur.executemany("INSERT OR IGNORE INTO books VALUES (?,?,?)", book_list)
    con.commit()

# run main()
if __name__ == '__main__':
    main()