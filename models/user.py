# -*- coding: utf-8 -*-

class User():
    def __init__(self, username = "", password =  "", email = ""):
        self.username = username
        self.password = password
        self.email = email

    def __str__(self):
        return f"[{self.username}] - [pwd:{self.password} eml:{self.email}]"
