import requests
from bs4 import BeautifulSoup
import pprint

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):    
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes' : points })
    return sort_stories_by_votes(hn)

def scrap_page(page):
    hn = []    
    links = []
    subtext = []
    for i in range(page):
        res = requests.get('https://news.ycombinator.com/news?p=%s' % str(i + 1))
        soup = BeautifulSoup(res.text, 'html.parser')        
        links += soup.select('.storylink')
        subtext += soup.select('.subtext')
    hn += create_custom_hn(links, subtext)       
    return sort_stories_by_votes(hn)

pprint.pprint(scrap_page(1))