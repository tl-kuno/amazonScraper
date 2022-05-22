# Program Name: Amazon Product Information Scraper
# Author: Taylor Kuno
# Created: 2022/04/29 16:32:37
# Last modified: 2022/05/22 10:25:17
# Description:  A simple web scraper created specifically to pull product information
#               from book, tv show and movie listings on Amazon


from flask import Flask, request
from scraper_functions import find_product_information
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_product_details():
    search_request = request.get_json()
    sr_dict = json.loads(search_request)
    product = sr_dict['product']
    file_name = product + ".json"
    find_product_information(product)
    with open(file_name, 'r') as prod_info:
        data = prod_info.read()

    os.remove(file_name)

    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)