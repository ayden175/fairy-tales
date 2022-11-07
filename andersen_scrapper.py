import requests
from bs4 import BeautifulSoup

import re
import os

# https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def get_all_links():
    url = 'https://andersen.sdu.dk/vaerk/hersholt/index_e.html'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find(id='hersholtliste').find_all('a')
    valid_links = [link['href'] for link in links if link['href'].startswith('http')]
    return valid_links


if __name__ == '__main__':

    folder = 'andersen'
    urls = get_all_links()
    l = len(urls)
    print(f'Found {l} fairy tales')
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

    for i, url in enumerate(urls):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find(id='content')
        title = content.find('h2').contents[0]
        text = content.find('div', {'class' : 'tekst'}).text

        filename = re.sub(r'[^\w]', '', title.lower().replace(' ', '_')) + '.txt'
        with open(os.path.join(folder, filename), 'w', encoding="utf-8") as f:
            f.write(text)

        printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)