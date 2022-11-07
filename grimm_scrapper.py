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

def get_response(url, retries, timeout):
    i = 0
    while i < retries:
        try:
            response = requests.get(url, timeout=timeout)
            return response
        except requests.exceptions.ConnectionError as e:
            print(f'Connection error, trying again. {i+1}/{retries}')
            i += 1

def get_all_links():
    url = 'https://www.grimmstories.com/en/grimm_fairy-tales/list'
    response = get_response(url, 5, 10)

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find('ul', {'class': 'bluelink'}).find_all('a')
    valid_links = [link['href'] for link in links]
    return valid_links


if __name__ == '__main__':

    folder = 'grimm'
    urls = get_all_links()
    l = len(urls)
    print(f'Found {l} fairy tales')
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

    for i, url in enumerate(urls):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find(id='plainText')
        title = content.find('h1', {'class': 'title'}).contents[0]
        text = content.find('div', {'class': 'text'}).text

        filename = re.sub(r'[^\w]', '', title.lower().strip().replace(' ', '_')) + '.txt'
 
        with open(os.path.join(folder, filename), 'w', encoding="utf-8") as f:
            f.write(text)

        printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        