import sqlite3

def dict_factory(cursor, row):
    save_dict = {}
    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]
    return save_dict

def update_format_args(sql, parameters: dict):
    sql = f"{sql} WHERE "
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, list(parameters.values())

def update_format(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cur = self.connection.cursor()

    def start_bot(self, colorama):
        #БД с пользователями
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS
        users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        lang TEXT,
        username TEXT)""")


        self.cur.execute(""" 
        CREATE TABLE IF NOT EXISTS 
        exchange(
        increment INTEGER PRIMARY KEY AUTOINCREMENT,
        exchange_id INTEGER,
        exchange_name TEXT)""")

        self.cur.execute(""" 
        CREATE TABLE IF NOT EXISTS 
        exchange_recill(
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        bot TEXT,
        secret_key TEXT, 
        Api_id TEXT,
        exchange_name TEXT)""")



        self.connection.commit()
        print(colorama.Fore.RED + "--- Базы данных подключены ---")




    def registation_user(self, user_id, username, lang):
        try:
            self.cur.execute(f"INSERT INTO users(user_id, username, lang) VALUES (?, ?, ?)", (user_id, username, lang))
        except sqlite3.IntegrityError:
            self.cur.execute("UPDATE users SET (lang, username) = (?, ?) WHERE user_id = ?", (lang, username, user_id))
        self.connection.commit()

    def check_user(self, user_id):
        member = self.cur.execute(f"SELECT user_id, lang FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if member == None:
            return False
        else:
            try:
                return member[1]
            except:
                return member['lang']



    def get_all_info(self, exchange):
        self.cur.row_factory = dict_factory
        sql = f"SELECT * FROM {exchange}"
        return self.cur.execute(sql).fetchall()

    # Добавление категории
    def add_exchange(self, exchange_id, exchange_name):
        self.cur.row_factory = dict_factory
        self.cur.execute("INSERT INTO exchange (exchange_id, exchange_name) VALUES (?, ?)", [exchange_id, exchange_name])
        self.connection.commit()

    def add_exchange_recill(self, user_id, username, bot, secret_key, api_id, exchange_name ):
        self.cur.row_factory = dict_factory
        self.cur.execute("INSERT INTO exchange_recill (user_id, username, bot, secret_key, Api_id, exchange_name) VALUES (?, ?, ?, ?, ?, ?)", [user_id, username, bot, secret_key, api_id, exchange_name])
        self.connection.commit()


    def get_exchange(self, **kwargs):
        self.cur.row_factory = dict_factory
        sql = f"SELECT * FROM exchange"
        sql, parameters = update_format_args(sql, kwargs)
        return self.cur.execute(sql, parameters).fetchone()


    def update_exchange(self,  exchange_id, **kwargs):
        self.cur.row_factory = dict_factory
        sql = f"UPDATE exchange SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(exchange_id)
        self.cur.execute(sql + "WHERE exchange_id = ?", parameters)
        self.connection.commit()

    def delete_exchange(self, **kwargs):
        self.cur.row_factory = dict_factory
        sql = "DELETE FROM exchange"
        sql, parameters = update_format_args(sql, kwargs)
        self.cur.execute(sql, parameters)
        self.connection.commit()


    def clear_all_exchange(self):
        self.cur.row_factory = dict_factory
        sql = "DELETE FROM exchange"
        self.cur.execute(sql)
        self.connection.commit()

