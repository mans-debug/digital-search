import requests
from bs4 import BeautifulSoup
import random


def get_page(link):
    resp = requests.get(link, timeout=2)
    if resp.status_code != 200:
        return None
    return resp.text


def get_links(page):
    bs_page = BeautifulSoup(page, 'html.parser')
    unfiltered_links = bs_page.find_all('a')
    unfiltered_links = [] if unfiltered_links is None else unfiltered_links
    return list(filter(lambda link: link[:4] == "http", map(lambda element: element.get('href'), unfiltered_links)))


def write_page(path, filename, file):
    with open(path + '/' + filename, 'w') as html_file:
        html_file.write(file)


def save_link(path, link):
    with open(path, 'a') as link_file:
        link_file.write(link + '\n')


def parse_links(links, counter, limit):
    links_location = 'scraped_links.txt'
    html_location = 'files'
    print('Counter:', counter)
    if counter > limit:
        return
    link = random.sample(links, 1)[0]
    links.remove(link)
    try:
        page = get_page(link)
        if page is None:
            print("Page is None")
            parse_links(links, counter, limit)
        else:
            scraped_links = get_links(page)
            save_link(links_location, link)
            write_page(html_location, 'index-' + str(counter) + '.html', page)
            parse_links(links.union(scraped_links), counter + 1, limit)
    except Exception as e:
        print(e)
        parse_links(links, counter, limit)


if __name__ == '__main__':
    starter_link = 'https://www.geeksforgeeks.org'
    counter = 0
    limit = 100
    link_pool = {starter_link}
    parse_links(link_pool, counter, limit)
