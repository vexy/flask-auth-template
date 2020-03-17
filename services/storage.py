# -*- coding: utf-8 -*-
from models.user import User

# represents a basic in memory storage heap
class UserDataStorage():
    def __init__(self):
        self.allUsers = []

    def store(self, userData):
        self.allUsers.append(userData)
        print(f"<STORAGE> New user stored: {userData.username}")

    # search all usernames and return matching user
    def find(self, targetUsername):
        result = None
        for user in self.allUsers:
            if user.username == targetUsername:
                result = user
                break
        return result

    # returns a list of all stored objects
    def asList(self):
        return list(self.allUsers)

    def totalCount(self):
        return len(list(self.allUsers))


# shared reference to a single storage
sharedStorage = UserDataStorage()
