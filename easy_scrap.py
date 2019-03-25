from urllib.request import urlopen
import re


def d_page(url):
    return urlopen(url).read().decode('utf-8')


def ex_link(page):
    link_reg = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return link_reg.findall(page)

if __name__ == '__main__':
    t_url = "http://www.whiteguide-nordic.com/"
    n_page = d_page(t_url)

    links = ex_link(n_page)

    for link in links:
        print(link)
