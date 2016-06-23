import scrapy
from bs4 import BeautifulSoup
from erostory_finder.items import ErostoryFinderItem
import requests
import logging


class StoryFinderSpider(scrapy.Spider):
    name = 'StoryFinder'
    allowed_domain = 'https://www.literotica.com/'
    start_urls = ['https://www.literotica.com/c/loving-wives/1-page']
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        item = ErostoryFinderItem()
        search_list = ['blonde', 'black', 'boyfriend', 'girlfriend', 'bed', 'down', 'up', 'sofa']
        while True:
            try:
                links = soup.select('.b-story-list .w-34t')
                for link in links:
                    try:
                        story_url = link.find('a', attrs={'class': 'r-34i'})
                        res = requests.get(story_url.get('href'))
                        story_soup = BeautifulSoup(res.text, 'lxml')
                        pages = story_soup.select('#sbar-l-wrp .b-pager')[0]
                        if len(pages.find_all('a')) != 0:
                            continue

                        story = story_soup.find('div', attrs={'class': 'b-story-body-x'}).get_text()
                        for key in search_list:
                            if key not in story:
                                break
                        else:
                            item['name'] = story_url.string
                            item['url'] = story_url.get('href')
                            yield item

                    except Exception, e:
                        self.logger.error(e.message)

                next_page = soup.find('a', text='Next')
                if next_page:
                    soup = BeautifulSoup(requests.get(next_page.get('href')).text, 'lxml')
                else:
                    break

            except Exception, e:
                self.logger.error(e.message)

