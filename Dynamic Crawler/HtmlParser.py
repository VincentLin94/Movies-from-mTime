# -*- coding:UTF-8 -*-

import re
from bs4 import BeautifulSoup
from HtmlDownloader import HtmlDownloader
import json


class HtmlParser(object):

    def parser_url(self, page_url, response):
        pattern = re.compile(r'(http://movie.mtime.com/(\d+))')
        urls = pattern.findall(response)
        if urls is not None:
            return list(set(urls))
        else:
            return None

    def parser_json(self, page_url, response):
        '''
        Parse the response using json
        :param page_url:
        :param response:
        :return:
        '''
        # Extract contents from between '=' and ';'
        pattern = re.compile(r'=(.*?);')
        result = pattern.findall(response)[0]
        if result is not None:
            # load the strings by json module
            value = json.loads(result)
            try:
                isRelease = value.get('value').get('isRelease')
            except Exception:
                print('Value Error')
                return None
            if isRelease:
                if value.get('value').get('hotValue') is None:
                    return self._parser_release(page_url, value)
                else:
                    return self._parser_no_release(page_url, value, isRelease=2)
            else:
                return self._parser_no_release(page_url, value)

    def _parser_release(self, page_url, value):
        '''
        Parse the released movies
        :param page_url:
        :param value:
        :return:
        '''
        try:
            isRelease = 1
            movieRating = value.get('value').get('movieRating')
            boxOffice = value.get('value').get('boxOffice')
            movieTitle = value.get('value').get('movieTitle')
            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')
            RatingFinal = movieRating.get('RatingFinal')

            MovieId = movieRating.get('MovieId')
            Usercount = movieRating.get('Usercount')
            AttitudeCount = movieRating.get('AttitudeCount')

            TotalBoxOffice = boxOffice.get('TotalBoxOffice')
            TotalBoxOfficeUnit = boxOffice.get('TotalBoxOfficeUnit')
            TodayBoxOffice = boxOffice.get('TodayBoxOffice')
            TodayBoxOfficeUnit = boxOffice.get('TodayBoxOfficeUnit')

            ShowDays = boxOffice.get('ShowDays')
            try:
                Rank = boxOffice.get('Rank')
            except Exception:
                Rank = 0
            return (MovieId, movieTitle, RatingFinal, ROtherFinal, RPictureFinal,
                    RDirectorFinal, RStoryFinal, Usercount, AttitudeCount,
                    TotalBoxOffice+TotalBoxOfficeUnit,
                    TodayBoxOffice+TodayBoxOfficeUnit,
                    Rank, ShowDays, isRelease)
        except Exception:
            return None

    def _parser_no_release(self, page_url, value, isRelease = 0):
        '''
        Parse the unreleased movies
        :param page_url:
        :param value:
        :param isRelease:
        :return:
        '''
        try:
            movieRating = value.get('value').get('movieRating')
            movieTitle = value.get('value').get('movieTitle')
            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')
            RatingFinal = movieRating.get('RatingFinal')

            MovieId = movieRating.get('MovieId')
            Usercount = movieRating.get('Usercount')
            AttitudeCount = movieRating.get('AttitudeCount')
            try:
                Rank = value.get('value').get('hotValue').get('Ranking')
            except Exception:
                Rank = 0
            return (MovieId, movieTitle, RatingFinal, ROtherFinal, RPictureFinal,
                    RDirectorFinal, RStoryFinal, Usercount, AttitudeCount,
                    'Not applicable', 'Not applicable',
                    Rank, 0, isRelease)
        except Exception:
            print(page_url, value)
            return None



    # def __init__(self):
    #     self.home_cont = HtmlDownloader().download('http://www.mtime.com/')
    #     self.page_urls = self._parse_home(self.home_cont)
    #
    # def _parse_home(self, home_cont):
    #     '''
    #     Extract all valid links from the home page
    #     :param home_cont: Downloaded home page content
    #     :return:
    #     '''
    #     if home_cont is None:
    #         return
    #     soup = BeautifulSoup(home_cont, 'html.parser')
    #     new_urls = []
    #     hrefs = soup.find('ul', class_='saling-list')
    #     hrefs = hrefs.find_all('a', href=re.compile('\.com\/\d*\/'), title=False)
    #     for i in hrefs:
    #         new_urls.append(i['href'])
    #     return new_urls
    #
    # def parse(self):
    #     '''
    #     Extract wanted data from the movie page
    #     :param page_url: Target page url
    #     :param html_cont: Downloaded movie page content
    #     :return:
    #     '''
    #     page_urls = []
    #     titles = []
    #     tags = []
    #     hotnesses = []
    #     musics = []
    #     graphs = []
    #     directors = []
    #     tales = []
    #     box_offices = []
    #     for url in self.page_urls:
    #         page_url = url
    #         html_cont = HtmlDownloader().download(url)
    #         soup = BeautifulSoup(html_cont, 'lxml')
    #         title = soup.find('div', pan='M14_Movie_Overview_Name').get_text().replace('\n', '')
    #         tag = soup.find('div', class_='otherbox __r_c_').get_text()
    #         titles.append(title)
    #         tags.append(tag)
    #     return titles, tags, hotnesses, musics, graphs, directors, tales, box_offices, page_urls


# Troubleshoot for this section

if __name__ == '__main__':
    page_url = 'http://movie.mtime.com/boxoffice/#CN/all'
    content = HtmlDownloader().root_download('http://movie.mtime.com/boxoffice/#CN/all')
    res = HtmlParser().parser_url(page_url, content)
    print(res)





