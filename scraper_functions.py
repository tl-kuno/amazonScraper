from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer as Strainer
import requests as requests
import json
import os

# This is a standard user-agent of Chrome browser running on Windows 10
headers = {'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
           'AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/71.0.3578.98 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip',
           'DNT': '1',
           'Connection': 'close'}

def create_search_url(search_string):
    """
    :param search_string: user supplied string they would like to search on amazon
    :return: url of amazon search
    """
    search_url = 'http://www.amazon.com/s?k='

    for char in search_string:
        if char == " ":
            search_url = search_url + '+'
        else:
            search_url = search_url + char

    return search_url

def find_product_image(search_soup):
    """
    :param: search_soup: soup data of an amazon search page
    :return: product image of first returned product
    """
    # locate first product image
    photo_object = search_soup.find("img", attrs={"class": 's-image'})
    photo_path = photo_object["src"]
    return photo_path

def find_product_page(search_soup):
    """
    :param: search_soup: soup data of an amazon search page
    :return: url of product page of first returned product
    """
    link_to_product = search_soup.find("a", attrs={"class": 'a-link-normal s-no-outline'})
    link_to_product_extension = link_to_product["href"]

    link_to_product_url = 'http://www.amazon.com' + link_to_product_extension
    return link_to_product_url

def retrieve_html(path):
    """
    :param: url
    :return: request object content of site
    """
    request_result = requests.get(path, headers=headers)
    return request_result.content

def save_html(html, path):
    """
    :param: html: html data to be written
    :param: path: path of where to write
    :return: saves html as file
    """
    with open(path, 'wb') as file:
        file.write(html)

def read_html(path):
    """file to read
    :return: file contents
    """
    with open(path, 'rb') as file:
        return file.read()

def find_product_information(user_string):
    """
    :param: user_string: product name as string
    scrapes the web page of the amazon web search of that product and writes a json file
    containing to path to the product page and image of the first returned product
    """

    search_url = create_search_url(user_string)

    local_search_html =retrieve_html(search_url)

    html_file_name = user_string + ".html"
    save_html(local_search_html, html_file_name)

    search_html = read_html(html_file_name)

    only_a = Strainer("a", attrs={"class":"a-link-normal s-no-outline"} )

    product_soup = Soup(search_html, features="html.parser", parse_only=only_a)

    product_page_url = find_product_page(product_soup)
    product_image_url =  find_product_image(product_soup)

    json_file_name = user_string + ".json"

    result_dict = {
        "product_url"   : product_page_url,
        "product_image" : product_image_url,
    }
    
    with open(json_file_name, "w") as outfile:
        json.dump(result_dict, outfile)
    
    os.remove(html_file_name)
