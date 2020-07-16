# -*- coding:UTF-8 -*-

import mysql.connector


class Storage(object):

    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='94_Vince',
            database='mtime'
        )
        self.cur = self.db.cursor()
        self.create_table('mtime')
        self.datas = []

    def create_table(self, table_name):
        '''
        Create the table in database
        :param table_name:
        :return:
        '''
        values = '''
        id integer auto_increment primary key,
        MovieId integer,
        MovieTitle varchar(40) NOT NULL,
        RatingFinal REAL NOT NULL DEFAULT 0.0,
        ROtherFinal REAL NOT NULL DEFAULT 0.0,
        RPictureFinal REAL NOT NULL DEFAULT 0.0,
        RDirectorFinal REAL NOT NULL DEFAULT 0.0,
        RStoryFinal REAL NOT NULL DEFAULT 0.0,
        Usercount integer NOT NULL DEFAULT 0,
        AttitudeCount integer NOT NULL DEFAULT 0,
        TotalBoxOffice varchar(20) NOT NULL,
        TodayBoxOffice varchar(20) NOT NULL,
        `Rank` integer NOT NULL DEFAULT 0,
        `ShowDays` integer NOT NULL DEFAULT 0,
        `isRelease` integer NOT NULL
        '''
        self.cur.execute('CREATE TABLE IF NOT EXISTS %s(%s)' % (table_name, values))

    def store_data(self, data):
        '''
        Store extracted data
        :param data:
        :return:
        '''
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas) > 2:
            self.store_db('mtime')

    def store_db(self, table_name):
        '''
        Store the datas in MySQL
        :param table_name:
        :return:
        '''
        for data in self.datas:
            self.cur.execute('INSERT INTO mtime (MovieId, MovieTitle, '
                             'RatingFinal, ROtherFinal, RPictureFinal, '
                             'RDirectorFinal, RStoryFinal, Usercount, '
                             'AttitudeCount, TotalBoxOffice, TodayBoxOffice, '
                             '`Rank`, `ShowDays`, `isRelease`) '
                             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data)
            self.datas.remove(data)
        self.db.commit()

    def store_end(self):
        if len(self.datas) > 0:
            self.store_db('mtime')
        self.db.close()


# Troubleshoot for this section
'''
if __name__ == '__main__':
    


'''

