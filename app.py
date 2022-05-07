# Program Name: Amazon Product Information Scraper
# Author: Taylor Kuno
# Created: 2022/04/29 16:32:37
# Last modified: 2022/05/07 15:30:34
# Description:  A simple web scraper created specifically to pull product information
#               from book, tv show and movie listings on Amazon


from flask import Flask, request
from scraper_functions import find_product_information
import json

app = Flask(__name__)

with open('./product_information.json', 'r') as prod_info:
    data = prod_info.read()

@app.route('/', methods=['POST'])
def get_product_details():
    search_request = request.get_json()
    sr_dict = json.loads(search_request)
    product = sr_dict['product']
    find_product_information(product)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

