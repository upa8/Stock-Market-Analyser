from bs4 import BeautifulSoup

import requests

url = "https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json"

r  = requests.get(url)

data = r.text

soup = BeautifulSoup(data)

print soup