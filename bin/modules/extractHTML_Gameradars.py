import requests #for http requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from urllib import request
import os
import re
from bs4 import BeautifulSoup

# Make soup of all files in a specified folder
HTMLfldr = '../data/raw/'
datafldr = '../data/'

soupCauldron = []
def makeSoup(fldr):
    for filename in os.listdir(fldr):
        content = open(fldr + filename, 'r')
        soupCauldron.append((BeautifulSoup(content.read(), 'html.parser'), filename))
        content.close()
    return soupCauldron

soupCauldron = makeSoup(HTMLfldr)

def extractSoup(soup, filename, webSource):
    if webSource == 'gamesradar':
        # Game title
        try: gameTitle = filename#soup.find(class_ = 'score-area').h4.get_text().rstrip().lstrip()
        except: gameTitle = None

        # GS review score
        try: ReviewerScore = soup.find(class_ = 'out-of-score-text').p.get_text()
        except: ReviewerScore = None

        try: verdict = soup.find(class_="game-verdict").get_text()
        except: verdict = None

        # review
        Review = ""
        try:
            for divs in soup.find_all('div', attrs={"class" : "text-copy bodyCopy auto"}):
                for ptag in divs.find_all('p'):
                    result = ptag.text
                    Review = Review + '' + result
        except: Review = None
        #try: Review = soup.find(class_ = 'text-copy bodyCopy auto').p.get_text()
        # Review = ""
        # try:
        #     chunks = soup.select('#default-content p')
        #     for chunk in chunks:
        #         result = chunk.get_text()
        #         Review = Review + ' ' + result
        # except:
        #     Review = None

        # Author name
        try: authorName = soup.find(class_ = 'no-wrap by-author').span.get_text()
        except: authorName = None

        # # Release date
        # try: releaseDate = soup.find(class_ = 'pod-objectStats-info__release').span.get_text()
        # except: releaseDate = None
        #
        # # Game short description
        # try: shortDescript = soup.find(class_ = 'pod-objectStats-info__deck').get_text()
        # except: shortDescript = None
        #
        # # ESRB category
        # try: ESRB = soup.find(class_ = 'pod-objectStats__esrb').dt.get_text()
        # except: ESRB = None

        # main table
        try:
            df_main = {
                'Game Title'       : gameTitle,
                 'Reviewer Score'  : ReviewerScore,
                 'Verdict'         : verdict,
                 'Author Name'     : authorName,
                # 'Release Date'     : releaseDate,
                # 'Short Description': shortDescript,
                 'Review'           : Review,
                # 'ESRB'             : ESRB,
                # 'File Name'        : filename
            }
            df_main = pd.DataFrame(df_main, index = [1])
        except: df_main = None

        # # ----------------------------------------------------------------------
        # # Platforms
        # platform = []
        # try:
        #     chunks = soup.select('.clearfix strong')
        #     for chunk in chunks:
        #         result = chunk.get_text()
        #         platform.append(result)
        # except: platform = None
        #
        # # platform table
        # try:
        #     df_platform = {
        #         'Game Title': np.repeat(gameTitle, len(platform)),
        #         'Platform'  : platform
        #     }
        #     df_platform = pd.DataFrame(df_platform)
        # except: df_platform = None
        #
        # # ----------------------------------------------------------------------
        # # scrape for developer, publisher, genre
        # chunks = soup.find(class_ = 'pod-objectStats-additional').find_all('dd')
        #
        #
        # # Developer
        # developer = []
        # try:
        #     results = chunks[0].find_all('a')
        #     for res in results:
        #         result = res.get_text()
        #         developer.append(result)
        # except: developer = None
        #
        # # developer table
        # try:
        #     df_developer = {
        #         'Game Title': np.repeat(gameTitle, len(developer)),
        #         'Developer' : developer
        #     }
        #     df_developer = pd.DataFrame(df_developer)
        # except: df_developer = None
        #
        # # ----------------------------------------------------------------------
        # # Publisher
        # publisher = []
        # try:
        #     results = chunks[1].find_all('a')
        #     for res in results:
        #         result = res.get_text()
        #         publisher.append(result)
        # except: publisher = None
        #
        # # publisher table
        # try:
        #     df_publisher = {
        #         'Game Title': np.repeat(gameTitle, len(publisher)),
        #         'Publisher' : publisher
        #     }
        #     df_publisher = pd.DataFrame(df_publisher)
        # except: df_publisher = None
        #
        # # ----------------------------------------------------------------------
        # # genre
        # genre = []
        # try:
        #     results = chunks[2].find_all('a')
        #     for res in results:
        #         result = res.get_text()
        #         genre.append(result)
        # except: genre = None
        #
        # # genre table
        # try:
        #     df_genre = {
        #         'Game Title': np.repeat(gameTitle, len(genre)),
        #         'Genre'     : genre
        #     }
        #     df_genre = pd.DataFrame(df_genre)
        # except: df_genre = None
        #

        return (df_main)

df_cb_main      = []

for soup, filename in soupCauldron:
    df_main = extractSoup(soup, filename, 'gamesradar')
    df_cb_main.append(df_main)

print(df_cb_main)



 # df_cb_platform  = []
# df_cb_developer = []
# df_cb_publisher = []
# df_cb_genre     = []
# for soup, filename in soupCauldron:
#     df_main, df_platform, df_developer, df_publisher, df_genre = extract.extractSoup(soup, filename, 'GameSpot')
#     df_cb_main.append(df_main)
#     df_cb_platform.append(df_platform)
#     df_cb_developer.append(df_developer)
#     df_cb_publisher.append(df_publisher)
#     df_cb_genre.append(df_genre)

df_cb_main      = pd.concat(df_cb_main, ignore_index = True)
# df_cb_platform  = pd.concat(df_cb_platform, ignore_index = True)
# df_cb_developer = pd.concat(df_cb_developer, ignore_index = True)
# df_cb_publisher = pd.concat(df_cb_publisher, ignore_index = True)
# df_cb_genre     = pd.concat(df_cb_genre, ignore_index = True)

# Save data for future analysis
df_cb_main.to_csv(datafldr + 'df_cb_main_Gameradars.csv')
# df_cb_platform.to_csv(datafldr + 'df_cb_platform.csv')
# df_cb_developer.to_csv(datafldr + 'df_cb_developer.csv')
# df_cb_publisher.to_csv(datafldr + 'df_cb_publisher.csv')
# df_cb_genre.to_csv(datafldr + 'df_cb_genre.csv')
