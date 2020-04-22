import mysql.connector as mariadb

class DB:
    def __init__(self):
        self.mariadb_connection = mariadb.connect(user='asphyx', password='', database='discord_private_chat')
        self.cursor = self.mariadb_connection.cursor()

    def score_user(self, discord_tag):
        self.cursor.execute('SELECT `score` FROM `users` WHERE `discord_tag` = {}'.format(discord_tag))
        return cursor['score']

    def add_score(self, discord_tag, value):
        current = self.score_user(discord_tag)
        value = value + current
        self.cursor.execute('UPDATE users SET score = {} WHERE discord_tag = {}'.format(value, discord_tag))
