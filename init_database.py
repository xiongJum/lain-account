import sys, os
sys.path.append(os.getcwd())

from my_sqlite3 import Db
from config import TableName

def sql_list():

    created_bill = """CREATE TABLE bill(
                        account_id PRIMARY KEY      NOT NULL,
                        date       DATE     NOT NULL DEFAULT (date('now', 'localtime')),
                        amount     REAL      NOT NULL,
                        bcategory  CHAR(50) NOT NULL,
                        scategory  CHAR(50) NOT NULL,
                        pay        CHAR(50) NOT NULL,
                        wallet     CHAR(50) NOT NULL,
                        books      CHAR(20) NOT NULL,
                        tag        TEXT             ,
                        city       CHAR(10)         ,
                        remark     TEXT             ,
                        date_created timeStamp NOT NULL DEFAULT (datetime('now', 'localtime')),
                        foreign key(bcategory) references config(config_id),
                        foreign key(scategory) references config(config_id),
                        foreign key(pay) references config(config_id),
                        foreign key(wallet) references config(config_id),
                        foreign key(books) references config(config_id)
    ) """

    created_config = """CREATE TABLE config(
                        config_id    PRIMARY KEY       NOT NULL,
                        config_name  TEXT      NOT NULL,
                        type         CHAR(20)  NOT NULL,
                        bcategory    CHAR(50)         ,
                        is_flag      INT       NOT NULL DEFAULT 0,
                        date_created timeStamp NOT NULL DEFAULT (datetime('now', 'localtime')),
                        foreign key(bcategory) references config(config_id)
    ) """

    created_fund = """CREATE TABLE fund(
                        fund_id      PRIMARY KEY       NOT NULL,
                        wallet    TEXT UNIQUE     NOT NULL,
                        start_amount REAL  NOT NULL,
                        date_created timeStamp NOT NULL DEFAULT (datetime('now', 'localtime')),
                        foreign key(wallet) references config(config_id)
    ) """
    global created_sql
    created_sql = locals()

def initialize():

    sql_list()
    db = Db(db='account.db')
    def sum_table(tablename):

        sql = f"select count(*) from sqlite_master where type='table' and name ='{tablename}';"
        return db.cx(sql_str=sql)
    
    for i in TableName.TABLE_NAME:
        sum = sum_table(i)

        if sum == 0:
            for value in created_sql.values():
                if i in value:
                    db.other(sql_str=value)



# sql = "insert into bill ('account_id', 'amount', 'bcategory', 'scategory', 'pay', 'wallet', 'tag', 'city', 'remark') values ('2023-0', 13.00, '食物', '早餐', '支付宝', '支付宝零钱', '测试', '宁波', '测试')"

if __name__ == '__main__':

    initialize()