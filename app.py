import requests
from lxml import html
import re
import json
import csv
import click

def write_to_json(filename, data):
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close

def write_to_csv(filename, data):
    headers = ['title', 'price', 'in_stock', 'description']
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerow(data)

@click.command()
@click.option('--bookurl', default='http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html', help='Please provide a bookurl from books.toscrape.com')
@click.option('--filename', default='output.json', help='Please provide a filename CSV/JSON')
def scrape(bookurl, filename):
    # bookurl = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    # filename = 'book.json'
    resp = requests.get(url=bookurl, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    })
    tree = html.fromstring(html = resp.text)
    product_main = tree.xpath("//div[contains(@class, 'product_main')]")[0]
    title = product_main.xpath(".//h1/text()")[0]
    price = product_main.xpath(".//p[1]/text()")[0]
    availibility = product_main.xpath(".//p[2]/text()")[1].strip()
    # in_stock = re.compile(r'\d+').findall(availibility)[0]
    in_stock = ''.join(list(filter(lambda x: x.isdigit(), availibility)))
    description = tree.xpath("//div[@id='product_description']/following-sibling::p/text()")[0]
    book_information = {
        'title': title,
        'price': price,
        'in_stock': in_stock,
        'description': description 
    }
    print(book_information)
    extension = filename.split('.')[1]
    if extension == 'json':
        write_to_json('book.json', book_information)
    elif extension == 'csv':
        write_to_csv('book.csv', book_information)
    else: 
        click.echo("The extension your provided is not supporter please use csv or json")

if __name__ == '__main__':
    scrape()
    # python .\project_1\app.py --bookurl="http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html" --filename="book.json"
    # keymap for format json Shift+Alt+F
    # python .\project_1\app.py --help