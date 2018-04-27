import pymysql.cursors

class Status(object):
    def __init__(self, f):
        self.save_info = f

class User(object):
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='070698yfcnz97',
                                          db='DarcMatter',
                                          charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor)

    def add_user(self, user):
        try:
            with self.connection.cursor() as cursor:
                sql = """insert into User (idUser) values (%s);"""
                cursor.execute(sql, (user.id,))
            self.connection.commit()
        except Exception as e:
            return e
        else:
            return True

    def update_NEM(self, user, NEM):
        with self.connection.cursor() as cursor:
            sql = """update User set NEM=%s where idUser=%s;"""
            cursor.execute(sql, (NEM, user.id))
        self.connection.commit()

    def update_twit(self, user, twit):
        with self.connection.cursor() as cursor:
            sql = """update User set twitter=%s where idUser=%s;"""
            cursor.execute(sql, (twit, user.id))
        self.connection.commit()

    def update_med(self, user, med):
        with self.connection.cursor() as cursor:
            sql = """update User set Medium=%s where idUser=%s;"""
            cursor.execute(sql, (med, user.id))
        self.connection.commit()

    def update_email(self, user, mail):
        with self.connection.cursor() as cursor:
            sql = """update User set email=%s where idUser=%s;"""
            cursor.execute(sql, (mail, user.id))
        self.connection.commit()

    def con_close(self):
        self.connection.close()

