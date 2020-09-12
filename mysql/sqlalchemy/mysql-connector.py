import mysql.connector


class Database:
    def __init__(self, **kwargs):
        """
        example:
            CREATE TABLE `user` (
              `id` int NOT NULL AUTO_INCREMENT,
              `account_id` int DEFAULT NULL,
              `name` varchar(255) DEFAULT NULL,
              `updated_at` datetime DEFAULT NULL,
              `created_at` datetime DEFAULT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

        :param kwargs:
        """
        self.db_config = kwargs
        self.con = mysql.connector.connect(**self.db_config)
        self.cur = self.con.cursor()

    def __del__(self):
        # ReferenceError: weakly-referenced object no longer exists
        # self.cur.close()
        self.con.close()


if __name__ == '__main__':
    micro_db = Database(host="127.0.0.1", port=3306, user="root", passwd="yangxinyue")

    micro_db.cur.execute('SELECT id, name FROM merchant.user where account_id = {}'.format(1))
    res = micro_db.cur.fetchall()  # list(tuple)
    print(res)
    # show last sql sentence
    print(micro_db.cur.statement)
    print(micro_db.cur.lastrowid)

    sql = 'INSERT INTO merchant.user  (account_id, name) values (%s,%s)' % (1, 2)
    micro_db.cur.execute(sql)
    micro_db.con.commit()
