import requests
from bs4 import BeautifulSoup
from dateparser import parse as date_parse
import sqlite3

conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link TEXT,
        title TEXT,
        content TEXT,
        date TEXT
    )
''')

conn.commit()
cursor.close()
conn.close()

url = 'https://nur.kz/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}

response = requests.get(url, headers=headers)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

for item in soup.find_all('div', class_='news-block'):
    link = item.find('a')['href']
    title = item.find('a').text.strip()
    content = item.find('div', class_='news-excerpt').text.strip()
    date = date_parse(item.find('div', class_='news-date').text.strip())

    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (link, title, content, date) VALUES (?, ?, ?, ?)",
                   (link, title, content, date))
    conn.commit()
    cursor.close()
    conn.close()
