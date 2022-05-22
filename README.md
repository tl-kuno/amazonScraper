<h1> CS 361 Microservice </h1>
<h2> Amazon Web Scraper </h2>

<p> This project employs the BeautifulSoup package to scrape product information from Amazon web sites. 
  Example code to call this service is show below </p>
  
<hr>
  
<code> import requests as requests</code><br>
<code> import json </code><br>
<br>
<code> api_url = "http://127.0.0.1:5000/"</code><br>
<br>
<code>def search_product(product):</code><br>
<code>  product_dict = {"product": product}</code><br>
<code>  product_json = json.dumps(product_dict, indent=4)</code><br>
<code>  details = requests.get(api_url, json=product_json)</code><br>
<code>  return details.json()</code><br>
<br>
<br>
<code>print(search_product("Train to Busan"))</code><br>
<code>print("")</code><br>
<code>print(search_product("The Walking Dead Season 1"))</code><br>
<code>print("")</code><br>
<code>print(search_product("World War Z book"))</code><br>
