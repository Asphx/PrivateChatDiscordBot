import mysql.connector as mariadb
import asyncio
from discord.ext import commands
import discord

class Sel(commands.Cog):

    def __init__(self):
        pass

    ### DATABASE SEL ###
    def sel_user(self, discord_tag):
        mariadb_connection = mariadb.connect(user='asphyx', password='', database='discord_private_chat')
        cursor = mariadb_connection.cursor()

        cursor.execute('SELECT `score` FROM `sel` WHERE `discord_tag` = "{}"'.format(discord_tag))
        res = cursor.fetchone()[0]
        mariadb_connection.close()
        return res

    def add_sel(self, discord_tag, value):
        mariadb_connection = mariadb.connect(user='asphyx', password='', database='discord_private_chat')
        cursor = mariadb_connection.cursor()
        current = self.sel_user(discord_tag)

        value = str(int(value) + int(current))
        cursor.execute('UPDATE sel SET score = {} WHERE discord_tag = "{}"'.format(value, str(discord_tag)))
        mariadb_connection.commit()
        mariadb_connection.close()

    def create_user_sel_database(self, username, userid):
        try:
            mariadb_connection = mariadb.connect(user='asphyx', password='', database='discord_private_chat')
            cursor = mariadb_connection.cursor()
            cursor.execute('INSERT INTO sel(`username`, `score`, `discord_tag`) VALUES ({}, 0, {});'.format(username, userid))
            mariadb_connection.commit()
            mariadb_connection.close()
        except Exception as e:
            print(e)

    ### FIN DATABASE SEL ###

    ### DISCORD COMMANDS SEL ###
    async def get_score_sel(self, ctx, username):
        try:
            score = "User not found"
            for all_user in ctx.guild.members:
                if all_user.name == username.name and all_user.id == username.id:
                    score = self.sel_user(username.id)
                    continue
        except Exception as e:
            print(e)
            score = "Erreur lors de la requete {}".format(e)
        await ctx.message.channel.send('Le sel de {} est de : {} '.format(username.name, score))

    async def add_to_sel(self, ctx, username, add_score_point):
        try:
            self.add_sel(username.id, add_score_point)
            await ctx.message.channel.send("Le sel de {} est maintenant de {}".format(username.name, self.sel_user(username.id)))
        except Exception as e:
            await ctx.message.channel.send('Une erreur s\'est produite {}'.format(e))

    async def all_sel(self, ctx): 
        try:
            for user in ctx.guild.members:
                try:
                    score = self.sel_user(str(user.id))
                except:
                    score = "Impossible de récupérer le score."
                    continue
                await ctx.message.channel.send("Le sel de {} est de : {}".format(user.name, score))
        except Exception as e:
            await ctx.message.channel.send('Une erreur est survenu : {}'.format(e))

    @commands.command(name="sel", description = "Sel", pass_context=True)
    async def sel(self, ctx, username: discord.Member = "", add_score_point=0):
        if username == '' :
            await self.all_sel(ctx)
            return True
        else:
            if type(username) == discord.Member:
                if isinstance(add_score_point, int) and add_score_point != 0:
                    await self.add_to_sel(ctx, username, add_score_point)
                else:
                    await self.get_score_sel(ctx, username)

    ### FIN DISCORD COMMANDS SEL ###

def setup(bot):
    bot.add_cog(Sel())
