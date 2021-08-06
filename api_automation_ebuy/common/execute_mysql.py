# -*- coding: utf-8 -*-


import pymysql
from common.logger import output_log


class ExecuteMysql(object):

    def __init__(self):
        # 连接数据库 可设置获取dict类型数据 添加设置cursorclass=pymysql.cursors.DictCursor
        self.con = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            database='easybuy',
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        output_log.info('数据库连接成功, host --> {}, database --> {}'.format('localhost','easybuy'))
        # 创建游标
        self.cur = self.con.cursor()

    def find_one(self, sql):
        output_log.info('正在执行查询数据库, sql --> {}'.format(sql))
        # 执行sql语句
        self.cur.execute(sql)
        # 刷新数据，并返回查询结果
        self.con.commit()
        res = self.cur.fetchone()
        output_log.info('数据库查询成功, 查询结果 --> {}'.format(res))
        return res

    def find_many(self, sql, number):
        output_log.info('正在执行查询数据库, sql --> {}'.format(sql))
        # 执行sql语句
        self.cur.execute(sql)
        # 刷新数据，并返回查询结果
        self.con.commit()
        return self.cur.fetchmany(number)

    def find_all(self, sql):
        # 执行sql语句
        self.cur.execute(sql)
        # 刷新数据，并返回查询结果
        self.con.commit()
        return self.cur.fetchall()

    def find_count(self, sql):
        count = self.cur.execute(sql)
        self.con.commit()
        return count

    def close(self):
        self.con.close()


if __name__ == '__main__':

    login_name = 'admin'
    db = ExecuteMysql()
    sql = f'select id from easybuy_user where loginName="{login_name}";'
    db_res = db.find_one(sql)
    print(db_res)
    print(type(db_res))
