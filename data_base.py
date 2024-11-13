import pymysql

class data_base:
    def __init__(self):
        self.user = "root"
        self.host = "localhost"
        self.password = "123"
        self.database = "python_lock_in_iot"
        self.charset = "utf8"

    def register(self, qry):
        con = pymysql.connect(user=self.user, password=self.password, host=self.host, database=self.database, charset=self.charset)
        curses = con.cursor()
        curses.execute(qry)
        con.commit()
        con.close()
        return "null"

    def show(self,qry):
        con = pymysql.connect(user=self.user,password=self.password,host=self.host,database=self.database,charset=self.charset)
        curses= con.cursor()
        curses.execute(qry)
        data=curses.fetchall()
        return data

    def delete(self, qry):
        con = pymysql.connect(user=self.user, password=self.password, host=self.host, database=self.database,
                              charset=self.charset)
        curses = con.cursor()
        curses.execute(qry)
        con.commit()
        con.close()
        return "null"

