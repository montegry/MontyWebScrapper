from urllib.request import urlopen
import re
"""This scrapper was created by montrgy with help of book Webite Scrapping with python. 
        It just printing all html tags by regular ex in link_reg var."""

def d_page(url):
    """reding all page from url"""
    return urlopen(url).read().decode('utf-8')


def ex_link(page):
    """Take s a web page, returns all by reg ex"""
    link_reg = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return link_reg.findall(page)

if __name__ == '__main__':
    t_url = "http://www.whiteguide-nordic.com/"
    n_page = d_page(t_url)

    links = ex_link(n_page)

    for link in links:
        print(link)
