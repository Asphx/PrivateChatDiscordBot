import mysql.connector as mariadb
import asyncio
from discord.ext import commands
import discord

class Gorgee(commands.Cog):

    def __init__(self):
        pass


def setup(bot):
    bot.add_cog(Gorgee())
