import mysql.connector as mariadb
import asyncio
from discord.ext import commands
import discord

class Scores(commands.Cog):

    def __init__(self):
        pass

    ### DATABASE SCORE ### 


    # @commands.command(name="createUsr", description="Créer un score pour un utilisateur", pass_context=True)
    # async def create_user(self, ctx, username):
    #     try:
    #         for user in ctx.guild.members:
    #             if user.name == username:
    #                 req = self.create_user_database(user.name, user.id)
    #                 print(req)
    #                 continue
    #     except Exception as e:
    #         await ctx.message.channel.send('Erreur : {}'.format(e))

    def score_user(self, discord_tag):
        mariadb_connection = mariadb.connect(user='asphyx', password='', database='discord_private_chat')
        cursor = mariadb_connection.cursor()

        cursor.execute('SELECT `score` FROM `users` WHERE `discord_tag` = "{}"'.format(discord_tag))
        res = cursor.fetchone()[0]
        mariadb_connection.close()
        return res

    def add_score(self, discord_tag, value):
        mariadb_connection = mariadb.connect(user='asphyx', password='', database='discord_private_chat')
        cursor = mariadb_connection.cursor()
        current = self.score_user(discord_tag)

        value = str(int(value) + int(current))
        cursor.execute('UPDATE users SET score = {} WHERE discord_tag = "{}"'.format(value, str(discord_tag)))
        mariadb_connection.commit()
        mariadb_connection.close()

    def create_user_database(self, username, userid):
        try:
            mariadb_connection = mariadb.connect(user='asphyx', password='', database='discord_private_chat')
            cursor = mariadb_connection.cursor()
            cursor.execute('INSERT INTO users(`username`, `score`, `discord_tag`) VALUES ({}, 0, {});'.format(username, userid))
            mariadb_connection.commit()
            mariadb_connection.close()
        except Exception as e:
            print(e)

    ### FIN DATABASE SCORE ###

    
    ### DISCORD COMMANDS SCORE ###
    async def get_score(self, ctx, user):
        try:
            score = "User not found"
            for all_user in ctx.guild.members:
                if (all_user.name == user.name and all_user.id == user.id):
                    score = self.score_user(user.id)
                    continue
        except Exception as e:
            score = "Une erreur s'est produite {}".format(e)
            # user_name = user.name
        await ctx.message.channel.send('Le score de {} est de : {}'.format(user.name, score))
        # await ctx.message.channel.send('Le score de {} est de : {}'.format(user_name, score))

    async def add_to_score(self, ctx, user, add_score_point):
        try:
            self.add_score(user.id, add_score_point)
            # user_name = user.name
            # await ctx.message.channel.send("Le score de {} est maintenant de {}".format(user_name, self.score_user(user.id)))
            await ctx.message.channel.send("Le score de {} est maintenant de {}".format(user.name, self.score_user(user.id)))
        except Exception as e:
            await ctx.message.channel.send('Une erreur s\'est produite => {}'.format(e))

    async def all_score(self, ctx): 
        try:
            for user in ctx.guild.members:
                try:
                    score = self.score_user(str(user.id))
                except:
                    score = "Impossible de récupérer le score."
                    continue
                await ctx.message.channel.send("Le score de {} est de : {}".format(user.name, score))
        except Exception as e:
            await ctx.message.channel.send('Une erreur est survenu : {}'.format(e))

    
    @commands.command(name="score", description="gère le score", pass_context=True)
    async def score(self, ctx, user: discord.Member = '', add_score_point=0):
        if user == '':
            await self.all_score(ctx)
            return True
        else:
            if type(user) == discord.Member:
                if isinstance(add_score_point, int) and add_score_point != 0:
                    await self.add_to_score(ctx, user, add_score_point)
                else:
                    await self.get_score(ctx, user)
            

    ### FIN SCORE ###

def setup(bot):
    bot.add_cog(Scores())
