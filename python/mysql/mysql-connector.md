```

import mysql.connector

class Database:
    def __init__(self, **kwargs):
        """
        example:
            micro_db = Database(host=f"{host}", port=3306, user="root", passwd="xinyue")

            micro_db.cur.execute('SELECT id, name FROM merchant.shop where account_id = {}'.format(account_id))
            res = micro_db.cur.fetchall() # list(tuple)


            # show last sql sentence
            print(micro_db.cur.statement)

            connection.insert_id()
            cursor.lastrowid

            sql = 'INSERT INTO database.shop  (a, b ) values (%s,%s)' % (1, 2)
            conn_db.cur.execute(sql)
            conn_db.con.commit()

        :param kwargs:
        """
        self.db_config = kwargs
        self.con = mysql.connector.connect(**self.db_config)
        self.cur = self.con.cursor()

    def __del__(self):
        # ReferenceError: weakly-referenced object no longer exists
        # self.cur.close()
        self.con.close()

```
