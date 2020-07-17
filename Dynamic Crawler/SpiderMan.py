# -*- coding:UTF-8 -*-

import time
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
import StorageSQL
import StorageXlsx


class SpiderMan(object):

    def __init__(self):
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.store_db = StorageSQL.Storage()
        self.store_xlsx = StorageXlsx.Storage()

    def crawl_db(self, root_url):
        '''
        Initialize the crawler with an original url --database version
        :param root_url: The original url
        :return:
        '''
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
                self.store_db.store_data(data)
                i += 1
                print('Crawling completion: %s times.' % i)
            except Exception:
                print('Crawling failed!')
        self.store_db.store_end()
        print('Crawling finished! Exiting programme...')

    def crawl_xlsx(self, root_url):
        '''
        Initialize the crawler with an original url --xlsx version
        :param root_url: The original url
        :return:
        '''
        content = self.downloader.root_download(root_url)
        urls = self.parser.parser_url(root_url, content)
        i = 0
        row = 1
        self.store_xlsx.write_head()
        for url in urls:
            try:
                i += 1
                row += 1
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
                self.store_xlsx.write_data(row, data)
                print('Crawling completion: %s times.' % i)
            except Exception:
                print('Crawling failed!')
        self.store_xlsx.write_end()
        print('Crawling finished! Exiting programme...')


if __name__ == '__main__':
    root_url = 'http://movie.mtime.com/boxoffice/#CN/all'
    spider = SpiderMan()
    # spider.crawl_db(root_url)  # Store data using MySQL database
    # spider.crawl_xlsx(root_url)  # Store data using openpyxl

