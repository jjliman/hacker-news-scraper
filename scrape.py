import requests
from bs4 import BeautifulSoup
import pprint


# returns a list of 2 lists: the 1st list contains storylinks, the 2nd list contains subtexts
def get_hn_data(num_pages):
    data = [[], []]
    for i in range(num_pages):
        link = 'https://news.ycombinator.com/news'
        if i > 0:
            link = link + f'?p={i+1}'
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        data[0].extend(soup.select('.storylink'))
        data[1].extend(soup.select('.subtext'))
    return data


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True )


def create_custom_hn(links, subtexts):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtexts[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


hn_data = get_hn_data(2)
pprint.pprint(create_custom_hn(hn_data[0], hn_data[1]))
