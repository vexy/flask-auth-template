# -*- coding: utf-8 -*-
from models.user import User

# represents a basic in memory storage heap
class UserDataStorage():
    allUsers = None

    def __init__(self):
        self.allUsers = []

    def store(self, userData):
        self.allUsers.append(userData)
        print("<STORAGE> New user stored.")

    # search all usernames and return matching user
    def getData(self, matchingUsername):
        retuslt = None
        for user in self.allUsers:
            if user.username == matchingUsername:
                result = user
        return result
