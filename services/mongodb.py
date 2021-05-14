from pymongo import MongoClient
import datetime

class DBError(Exception):
    """ raised on critical db errors """
    pass

class DBTypeError(Exception):
    """ raised on db type errors """
    pass

class Database:
    client = None
    db = None

    def __init__(self, host, user, pwd, data, port=27017):
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
        try:
            self.client = MongoClient(f"mongodb://{user}:{pwd}@{host}:{port}/")
            self.db = self.client[data]
            print(self.client)
            print(self.db)
        except:
            raise DBError("Failed to connect.")

    def close(self):
        if self.db is not None:
            self.db.close()

    def insert(self, collection, fields):
        if not isinstance(collection, str):
            raise DBTypeError("'collection' param must be type of 'str'.")
        if not isinstance(fields, dict):
            raise DBTypeError("'fields' param must be type of 'dict'.")
        try:
            col = self.db[collection]
            return col.insert_one(fields)
        except:
            return None

    def update(self, collection, objectID, fields):
        if not isinstance(collection, str):
            raise DBTypeError("'collection' param must be type of 'str'.")
        if not isinstance(fields, dict):
            raise DBTypeError("'fields' param must be type of 'dict'.")

        try:
            col = self.db[collection]
            res = col.update_many({"id": objectID}, {"$set": fields})
            return res.modified_count
        except:
            return None

    def delete(self, collection, objectID):
        if not isinstance(collection, str):
            raise DBTypeError("'collection' param must be type of 'str'.")
        if not isinstance(objectID, str):
            raise DBTypeError("'objectID' param must be type of 'str' or 'ObjectID'.")
        try:
            col = self.db[collection]
            res = col.delete_many({"id": objectID})
            return res.deleted_count
        except:
            return -1

    def filter(self, collection, filterCriteria):
        if not isinstance(collection, str):
            raise DBTypeError("'collection' param must be type of 'str'.")

        try:
            col = self.db[collection]
            res = col.find(filterCriteria)
            return res
        except:
            return None


#
# Example usage as a standalone module
#
if __name__ == "__main__":
    HOST = ""
    PORT = 27017
    USER = "Admin"
    PASS = "Pwd"
    DATA = "admin"

    db = Database(HOST, USER, PASS, DATA, PORT)
    x = db.filter("users", "testUser1")
    print(f"Find: {x}")
    x = db.insert("users", {"name": "testUser1", "number": 3, "number2": 3.5, "addedOn": datetime.datetime.now()})
    print(f"Insert: {x}") #x.inserted_id
    x = db.filter("users", "testUser1")
    print(f"Find: {x}")
    x = db.update("users", "testUser1", {"number": 5, "number2": 7.75})
    print(f"Update: {x}")
    x = db.filter("users", "{user: 'testUser1'}")
    print(f"Find: {x}")
    x = db.delete("users", "testUser1")
    print(f"Delete: {x}")
    x = db.filter("users", "testUser1")
    print(f"Find: {x}")
