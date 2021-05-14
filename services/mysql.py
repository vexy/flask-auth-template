import pymysql as mysql
import datetime
import time

class DBError(Exception):
    # raised when there's a fatal database error
    pass

class DBTypeError(TypeError):
    # raised when there's a database type error (currently supports 'str', 'float', 'int', 'None', 'bool' and datetime.datetime)
    pass

class Database:
    db = None
    dbc = None
    autocommit = True
    autoreconnect = True

    def __init__(self, host, user, pwd, data, port=3306, autocommit=True, autoreconnect=True):
        if not isinstance(host, str):
            raise DBTypeError("'host' param must be type of 'str'.")
        if not isinstance(user, str):
            raise DBTypeError("'user' param must be type of 'str'.")
        if not isinstance(pwd, str):
            raise DBTypeError("'pwd' param must be type of 'str'.")
        if not isinstance(data, str):
            raise DBTypeError("'data' param must be type of 'str'.")
        if not isinstance(port, int):
            raise DBTypeError("'port' param must be type of 'int'.")
        if not isinstance(autocommit, bool):
            raise DBTypeError("'port' param must be type of 'bool'.")
        if not isinstance(autoreconnect, bool):
            raise DBTypeError("'port' param must be type of 'bool'.")
        try:
            self.db = mysql.connect(host=host, user=user, password=pwd, database=data, port=port)
            self.dbc = self.db.cursor()
            self.autocommit = autocommit
            self.db.ping(reconnect=autoreconnect)
        except Exception as e:
            raise DBError(f"Exception while trying to connect to the database: {e}")

    def close(self):
        if self.db is not None:
            self.db.close()

    def insert(self, table, fields):
        if not isinstance(table, str):
            raise DBTypeError("'table' param must be type of 'str'.")
        if not isinstance(fields, dict):
            raise DBTypeError("'fields' param must be type of 'dict', ie. Dict['field'] = value")
        length = len(fields)
        if length == 0:
            raise DBTypeError("'fields' parameter must not be empty.")
        table = _escape(table)
        query = f"INSERT INTO {table} ("
        i = 0
        querypt1 = ''
        querypt2 = ''
        for key in fields:
            i += 1
            key = _escape(key)
            if not isinstance(key, str):
                raise DBTypeError("A 'fields' key must be type of 'str' only.")
            if isinstance(fields[key], str):
                fields[key] = _escape(fields[key])
                querypt1 += f"{key}"
                querypt2 += f"'{fields[key]}'"
            elif isinstance(fields[key], int) or isinstance(fields[key], float) or isinstance(fields[key], bool):
                querypt1 += f"{key}"
                querypt2 += f"{fields[key]}"
            elif fields[key] is None:
                querypt1 += f"{key}"
                querypt2 += f"NULL"
            elif isinstance(fields[key], datetime.datetime):
                querypt1 += f"{key}"
                querypt2 += f"'{fields[key].strftime('%Y%m%d%H%M%S')}'"
            else:
                raise DBTypeError("A 'fields' value must be type of 'int', 'float', 'bool', 'str', 'datetime.datetime' or 'None' only.")
            if i != length:
                querypt1 += ","
                querypt2 += ","
        try:
            query += querypt1 + ") VALUES (" + querypt2 + ")"
            self.dbc.execute(query)
            return True
        except Exception as e:
            print(e)
            return False

    def update(self, table, userID, fields):
        if not isinstance(table, str):
            raise DBTypeError("'table' param must be type of 'str'.")
        if not isinstance(fields, dict):
            raise DBTypeError("'fields' param must be type of 'dict', ie. Dict['field'] = value")
        if not isinstance(userID, int):
            raise DBTypeError("'userID' param must be type of 'int'.")
        length = len(fields)
        table = _escape(table)
        if length == 0:
            raise DBTypeError("'fields' parameter must not be empty.")
        query = f"UPDATE {table} SET "
        i = 0
        for key in fields:
            i += 1
            key = _escape(key)
            if not isinstance(key, str):
                raise DBTypeError("A 'fields' key must be type of 'str' only.")
            if isinstance(fields[key], str):
                fields[key] = _escape(fields[key])
                query += f"{key} = '{fields[key]}'"
            elif isinstance(fields[key], int) or isinstance(fields[key], float) or isinstance(fields[key], bool):
                query += f"{key} = {fields[key]}"
            elif isinstance(fields[key], datetime.datetime):
                query += f"{fields[key].strftime('%Y%m%d%H%M%S')}"
            elif fields[key] is None:
                query =+ f"{key} = NULL"
            else:
                raise DBTypeError("A 'fields' value must be type of 'int', 'float', 'bool', 'str', 'datetime.datetime' or 'None' only.")
            if i != length:
                query += ","
        query += f" WHERE ID = {userID}"
        try:
            self.dbc.execute(query)
            if self.autocommit:
                self.db.commit()
            return self.dbc.rowcount
        except Exception:
            return -1

    def delete(self, table, userID):
        if not isinstance(table, str):
            raise DBTypeError("'table' param must be type of 'str'.")
        if not isinstance(userID, int):
            raise DBTypeError("'userID' param must be type of 'int'.")
        table = _escape(table)
        query = f"DELETE FROM {table} WHERE ID = {userID}"
        try:
            self.dbc.execute(query)
            if self.autocommit:
                self.db.commit()
            return self.dbc.rowcount
        except Exception:
            return -1

    def filter(self, table, userName):
        if not isinstance(table, str):
            raise DBTypeError("'table' param must be type of 'str'.")
        if not isinstance(userName, str):
            raise DBTypeError("'userName' param must be type of 'str'.")
        userName = _escape(userName)
        table = _escape(table)
        query = f"SELECT * FROM {table} WHERE name = '{userName}'"
        try:
            self.dbc.execute(query)
            if self.autocommit:
                self.db.commit()
            x = list(self.dbc.fetchall())
            for i in range(len(x)):
                x[i] = list(x[i])
            return x
        except Exception:
            return None

def _escape(text):
    return text.replace("'", "''")

#
# Example usage as a standalone module
#
if __name__ == "__main__":
    USER = ""
    HOST = ""
    PASS = ""
    DATA = ""
    db = Database(HOST, USER, PASS, DATA, autocommit=True, autoreconnect=True)
    x = db.filter("users", "test8")
    print(f"Select: {x}")
    d = datetime.datetime(year=2020, month=3, day=5, hour=17, minute=10, second=59)
    x = db.insert("users", {"name":"test8","pwd":"x","salt":"y","token":"z","number":310,"number2":3.13421,"date":d})
    print(f"Insert: {x}")
    x = db.filter("users", "test8")
    print(f"Select: {x}")
    _id = x[0][0]
    x = db.update("users", _id, {"number": 72, "number2": 127.4})
    print(f"Update: {x}")
    x = db.filter("users", "test8")
    print(f"Select: {x}")
    x = db.delete("users", _id)
    print(f"Delete: {x}")
    x = db.filter("users", "test8")
    print(f"Select: {x}")
    db.close()
