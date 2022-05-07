from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer as Strainer
import requests as requests
import json

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
    # locate first extension for link to first product in search
    link_to_product = search_soup.find("a", attrs={"class": 'a-link-normal s-no-outline'})
    link_to_product_extension = link_to_product["href"]

    # concatenate extension to base url
    link_to_product_url = 'http://www.amazon.com' + link_to_product_extension
    return link_to_product_url

def retrieve_html(path):
    request_result = requests.get(path, headers=headers)
    return request_result.content

def save_html(html, path):
    with open(path, 'wb') as file:
        file.write(html)

def read_html(path):
    with open(path, 'rb') as file:
        return file.read()

def find_product_information(user_string):

    # construct url of the amazon search
    search_url = create_search_url(user_string)

    # retrieve html
    local_search_html =retrieve_html(search_url)

    # save html file
    save_html(local_search_html, 'search_result')

    # open html
    search_html = read_html('search_result')

    #strainers
    only_a = Strainer("a", attrs={"class":"a-link-normal s-no-outline"} )

    # parse file
    product_soup = Soup(search_html, features="html.parser", parse_only=only_a)

    product_page_url = find_product_page(product_soup)
    product_image_url =  find_product_image(product_soup)

    result_dict = {
        "product_url"   : product_page_url,
        "product_image" : product_image_url
    }
    
    with open("product_information.json", "w") as outfile:
        json.dump(result_dict, outfile)
