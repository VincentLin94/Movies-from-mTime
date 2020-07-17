# -*- coding:utf-8 -*-

import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class HtmlDownloader(object):

    def download(self, url):
        '''
        Download the whole page for parsing
        :param url: Target url
        :return:
        '''
        if url is None:
            return None
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.116 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            return r.text
        return None

    def root_download(self, url):
        '''
        Get page source using Selenium
        :param url: Target url
        :return:
        '''
        chrome_set = Options()
        chrome_set.add_argument('--headless')
        chrome_set.add_argument('disable-gpu')
        chrome_set.add_argument('--window-size=1600,900')
        browser = webdriver.Chrome(options=chrome_set)
        browser.get(url)
        # Page 1
        page1 = browser.find_element_by_xpath('/html/body/div[3]/div[1]/ul/li[1]/dl/dt[3]/a')
        page1.click()
        time.sleep(1.5)
        page_content1 = browser.page_source
        # Page 2
        page2 = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/a[2]')
        page2.click()
        time.sleep(1.5)
        page_content2 = browser.page_source
        # Page 3
        page3 = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/a[3]')
        page3.click()
        time.sleep(1.5)
        page_content3 = browser.page_source
        # Page 4
        page4 = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/a[4]')
        page4.click()
        time.sleep(1.5)
        page_content4 = browser.page_source
        # Page 5
        page5 = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/a[5]')
        page5.click()
        time.sleep(1.5)
        page_content5 = browser.page_source
        browser.close()
        response = page_content1 + page_content2 + page_content3 + page_content4 + page_content5
        return response


# Troubleshoot for this section
'''
if __name__ == '__main__':
    res = HtmlDownloader().download('http://service.library.mtime.com/Movie.api'
                                    '?Ajax_CallBack=true'
                                    '&Ajax_CallBackType=Mtime.Library.Services'
                                    '&Ajax_CallBackMethod=GetMovieOverviewRating'
                                    '&Ajax_CrossDomain=1'
                                    '&Ajax_RequestUrl=http://movie.mtime.com/262895/'
                                    '&t=202007151817'
                                    '&Ajax_CallBackArgument0=242129')
    print(res)
'''

'''
if __name__ == '__main__':
    res = HtmlDownloader().root_download('http://movie.mtime.com/boxoffice/#CN/all')
    print(res)

'''