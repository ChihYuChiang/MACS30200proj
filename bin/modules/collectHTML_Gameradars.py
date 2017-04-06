import requests #for http requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from urllib import request
import os
import re
from bs4 import BeautifulSoup


output_fldr = '../data/raw/'
if not os.access(output_fldr, os.F_OK):
    os.mkdir(output_fldr)

def getHTML(url):
    searchStr = re.search('/([a-z0-9]*\-)+[a-z0-9]*/$', url).group(0)[1:-1] # extract id from url for filenane
    response = request.urlopen(url)
    html = response.read().decode('utf-8')
    content = open(output_fldr + searchStr + '.html', 'w+')
    content.write(html)
    content.close()

reviewLinks = []
def getURL(page):
    response = request.urlopen('http://www.gamesradar.com/all-platforms/reviews/page/' + str(page)+'/')
    html = response.read().decode('utf-8')
    html = BeautifulSoup(html, 'html.parser')

    for i in list(range(1, 21)):
        productDivs = html.findAll('div', attrs={'class' : 'listingResult small result' + str(i) + " "})
        for div in productDivs:
            result = div.find('a')['href']
            reviewLinks.append(result)
    return reviewLinks
