import sqlite3

class Db():

    def __init__(self, db='bill.db') -> None:
        
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        # 打开 sqlite3 的外键限制
        self.cur.execute("PRAGMA FOREIGN_KEYS=ON;")
        
    def cx(self, sql_str, is_sole=False):

        self.cur.execute(sql_str)

        if is_sole:
            return self.cur.fetchone()
        
        data = self.cur.fetchall()
        if data: 
            if len(data[0]) == 1:
                return data[0][0]
        return data
        
    def other(self, sql_str):
        # print(sql_str)
        self.cur.execute(sql_str)
        self.con.commit()

    def __del__(self):

        self.cur.close()
        self.con.close()

