import time
import math
import sqlite3

class HDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu( self ):
        sql = """SELECT * FROM menu"""
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except Exception as e:
            print(f'Ошибка подключения к дб {e}')
        return []


    def addUser( self, username, useremail, password ):
        try:
            self.__cur.execute( "SELECT COUNT() as `count` FROM users WHERE email LIKE ?", (useremail,) )
            res = self.__cur.fetchone( )
            if res[ 'count' ] > 0:
                print( "Пользователь с таким URL уже существует" )
                return False

            tm = math.floor( time.time( ) )
            self.__cur.execute( """INSERT INTO users VALUES(NULL, ?, ?, ?, ?)""", (username, useremail, password, tm) )
            self.__db.commit( )
        except sqlite3.Error as e:
            print( f'Ошибка SQLITE users db {e}' )
            return False

        return True

    def addPost( self, titlel, textl , url):
        try:
            try:
                self.__cur.execute( "SELECT COUNT() as `count` FROM posts WHERE url LIKE ?", (url,) )
                res = self.__cur.fetchone( )
                if res[ 'count' ] > 0:
                    print( "Статья с таким url уже существует" )
                    return False
            except Exception as e:
                print("Ошибка addPost " + str(e))
                return False

            tm = math.floor(time.time())
            self.__cur.execute("""INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)""", (titlel, textl, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Ошибка SQLITE db {e}')
            return False

        return True

    def getPosts( self ):
        sql = """SELECT * FROM posts"""
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except Exception as e:
            print(f'Ошибка подключения к дб {e}')
        return []

    def getPost( self, alias ):
        try:
            self.__cur.execute("SELECT title, text FROM posts WHERE url LIKE ? LIMIT 1", (alias,))
            res = self.__cur.fetchone( )
            if res:
                return res
        except sqlite3.Error as e:
            print( "Ошибка получения статьи из БД " + str( e ) )

        return (False, False)