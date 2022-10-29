import requests
from bs4 import BeautifulSoup
from flask import Flask,request,jsonify

app = Flask(__name__)
ebayurl="https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=headphones"

def get_data(ebayurl):
    r = requests.get(ebayurl)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

@app.route('/extract')
def parse():
    r = requests.get(ebayurl)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    thislist=[]
    for item in results:
        if 'to' not in item.find('span', {'class': 's-item__price'}).text.replace('$',''):
            product = {
                'title': item.find('div', {'class': 's-item__title'}).text,
                'price': item.find('span', {'class': 's-item__price'}).text.replace('$',''),
            }
            thislist.append(product)

    return jsonify(thislist)

if __name__ == '__main__':
    app.run(debug=True)