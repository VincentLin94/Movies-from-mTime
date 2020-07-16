# -*- coding:UTF-8 -*-

import time
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from StorageSQL import Storage


class SpiderMan(object):

    def __init__(self):
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.store = Storage()

    def crawl(self, root_url):
        content = self.downloader.root_download(root_url)
        urls = self.parser.parser_url(root_url, content)
        i = 0
        for url in urls:
            try:
                t = time.strftime('%Y%m%d%H%MS3282', time.localtime())
                rank_url = 'http://service.library.mtime.com/Movie.api' \
                           '?Ajax_CallBack=true' \
                           '&Ajax_CallBackType=Mtime.Library.Services' \
                           '&Ajax_CallBackMethod=GetMovieOverviewRating' \
                           '&Ajax_CrossDomain=1' \
                           '&Ajax_RequestUrl=%s' \
                           '&t=%s' \
                           '&Ajax_CallBackArgument0=%s' % (url[0], t, url[1])
                rank_content = self.downloader.download(rank_url)
                data = self.parser.parser_json(rank_url, rank_content)
                self.store.store_data(data)
                i += 1
                print('Crawling completion times: %s' % i)
            except Exception:
                print('Crawling failed!')
        self.store.store_end()
        print('Crawling finished!')


if __name__ == '__main__':
    root_url = 'http://movie.mtime.com/boxoffice/#CN/all'
    spider = SpiderMan()
    spider.crawl(root_url)

