import sqlite3

database = 'chat.db'


class Query:

    def __init__(self):
        try:
            self.__conn = sqlite3.connect(database)
        except sqlite3.Error as e:
            print(e)

    def select(self, user_id):
        msgs = []
        cur = None

        try:
            cur = self.__conn.cursor()
            cur.execute('''SELECT * FROM chat WHERE USER_ID=?''', (user_id,))
            rows = cur.fetchall()

            for row in rows:
                msgs.append(dict(
                    timestamp=row[4],
                    sender=row[3],
                    text=row[2]
                ))

            return msgs

        finally:
            if cur is not None:
                cur.close()

    def insert(self, *msgs):
        _msgs = []
        cur = None

        try:
            for msg in msgs:
                _msgs.append((
                    msg['user_id'],
                    msg['text'],
                    msg['sender'],
                    msg['timestamp']
                ))

            cur = self.__conn.cursor()
            cur.executemany('''INSERT INTO chat(USER_ID,TEXT,SENDER,TIMESTAMP) VALUES(?,?,?,?)''',
                            _msgs)

            self.__conn.commit()
        finally:
            if cur is not None:
                cur.close()

    def delete_by_id(self, user_id, id):
        cur = None

        try:
            p = (user_id, id)
            cur = self.__conn.cursor()
            cur.execute('''DELETE FROM chat WHERE USER_ID=? AND ID=?''', p)
            self.__conn.commit()

        finally:
            if cur is not None:
                cur.close()

    def delete_all(self, user_id):
        cur = None

        try:
            cur = self.__conn.cursor()
            cur.execute('''DELETE FROM chat WHERE USER_ID=?''', (user_id))
            self.__conn.commit()
        finally:
            if cur is not None:
                cur.close()
