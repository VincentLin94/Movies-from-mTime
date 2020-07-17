# -*- coding:UTF-8 -*-

import re
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


# Troubleshoot for this section
'''
if __name__ == '__main__':
    page_url = 'http://movie.mtime.com/boxoffice/#CN/all'
    content = HtmlDownloader().root_download('http://movie.mtime.com/boxoffice/#CN/all')
    res = HtmlParser().parser_url(page_url, content)
    print(res)

'''



