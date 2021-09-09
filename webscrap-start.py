# Created on 9/03/2021

# @author: Nightmare-King-Grimm
import pandas as pd
from bs4 import BeautifulSoup
import requests


# get the URL list
list1 = []

a = 'https://stackoverflow.com/questions/55140604/news-site-scrape-with-python'
list1.append(a) 
# define the variables
url = "https://stackoverflow.com/questions/55140604/news-site-scrape-with-python"
list2 = list1 [0:10]
type(list2)



results = pd.DataFrame()
for url in list2:

    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    href = url
    title = soup.find("h1", "title").text
    #title = soup.find("h1", "title").string
    #title.extend(soup.find("h1", "title").string) # the title string
    subtitle = soup.find("div", "descr").text
    #subtitle.extend(soup.find("div", "descr").string) # the subtitle string
    time = soup.find("div", "art_author").text
    #time.extend(soup.find("div", "art_author").text)
    #par = soup.find("div", id="art_start").find_all("p")
    art1 = soup.find("div", id="art_start").find_all("p")

    article = []
    for a in art1:
        if 'googletag.cmd.push' not in a.text:
            article.append(a.text.strip())
    article = ' '.join(article)



    temp_df = pd.DataFrame([[title, subtitle, time, article]], columns = ['title','subtitle','time','article'])
    results = results.append(temp_df).reset_index(drop=True)

results.to_csv("Scraped.csv", index=False, encoding='utf-8-sig')