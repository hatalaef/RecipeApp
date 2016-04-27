import testHeaders
from bs4 import BeautifulSoup

def make_soup(url, useragent):
    params = testHeaders.fetch(url, agent = useragent)
    return BeautifulSoup(params["data"], "lxml")
    
def get_links(the_url, useragent):
    soup = make_soup(the_url, useragent)
    main_col = soup.find("div", "main-col")
    links = [a.get("href") for a in main_col.findAll("a")]
    return links