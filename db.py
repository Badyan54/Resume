import sqlite3, math, time

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    
    def get_comment(self):
        query = "SELECT comments.comment, users.NickName, users.Rang\
         FROM comments\
         JOIN users ON comments.id = users.id\
         ORDER BY comments.ROWID DESC;"
        
        try:
            self.__cur.execute(query )
            res = self.__cur.fetchall()

            if res: return res
        except:
            print("error")
        return []
    
    def addPost(self, text, NickName):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("SELECT id FROM users WHERE NickName == ?", (NickName,))
            id = self.__cur.fetchone()
            self.__cur.execute("INSERT INTO comments VALUES(?, ?)", (id["id"], text,))
            self.__db.commit()
        except sqlite3.Error as e:
            print("reror" + str(e))
            return False
        return True

    def get_user(self, user, password):
        query = "SELECT * FROM users WHERE NickName == ? AND password == ?;"
        try:
            self.__cur.execute(query, (user, password))
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("error")

    def addUser(self, NickName, password, rang):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users (NickName, password, rang) VALUES(?, ?, ?)", (NickName, password, rang))
            self.__db.commit()
        except sqlite3.Error as e:
            print("reror" + str(e))
            return False
        return True

