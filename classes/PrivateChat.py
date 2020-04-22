import asyncio
from discord.ext import commands
import mysql.connector as mariadb
import requests
import random


class PrivateChat(commands.Cog):

    def __init__(self):
        pass
        # self.mariadb_connection = mariadb.connect(user='asphyx', password='', database='discord_private_chat')
        # self.cursor = self.mariadb_connection.cursor()

    @commands.command(name='private', description="Remove all message sent between the command and N minutes after",
                      pass_context=True)
    async def private(self, ctx, time):
        count = -1
        messageID = ctx.message.id
        print(ctx.message.id)
        time = int(time)
        for i in range(time * 60):
            await asyncio.sleep(1)
            # print(i)
            if i % 60 == 0:
                await ctx.message.channel.send(
                    'Il reste {} minute(s) avant la suppression des messages'.format(str(int(((time * 60) - i) / 60)))
                )

        async for i in ctx.message.channel.history():
            if i.id >= int(messageID):
                await i.delete()
                count += 1
            else:
                await ctx.message.channel.send(
                    'Suppression de {} message(s) avec succès'.format(count)
                )
                return

    @commands.command(name="clearID", description="Remove all messages in channel until given ID", pass_context=True)
    async def clearID(self, ctx, messageID):
        count = -1
        async for i in ctx.message.channel.history():
            if i.id >= int(messageID):
                await i.delete()
                count += 1
            else:
                await ctx.message.channel.send(
                    'Suppression de {} message(s) avec succès'.format(count)
                )
                return

    @commands.command(name="clearN", description="Remove N messages in channel", pass_context=True)
    async def clear(self, ctx, number):
        number = int(number)
        if number > 50 : 
            await ctx.message.channel.send('Trop de message à supprimer, la limite est de 50 à la fois')
            return
        count = 0
        async for i in ctx.message.channel.history():
            if number >= count:
                await i.delete()
                count += 1
            else :
                await ctx.message.channel.send(
                    'Suppression de {} message(s) avec succès'.format(count - 1)
                )
                return
            """
            if i.id >= int(messageID):
                await i.delete()
                count += 1
            else:
                await ctx.message.channel.send(
                    'Suppression de {} message(s) avec succès'.format(count)
                )
                return
                """
       
    @commands.command(name="rename", description="Rename selected user", pass_context=True)
    async def rename_user(self, ctx, user_to_rename, new_username):
        for user in ctx.guild.members:
            print(user)
            if user.name == user_to_rename:
                print('Utilisateur trouvé : {}'.format(user))
                try:
                    await user.edit(nick=new_username)
                    return
                except Exception as e:
                    print('Erreur => \n {}'.format(e))
                    return
        print('Aucun utilisateur trouvé')
        return

### SCORE ###
    # @commands.command(name="gScore", description="Score blague de merde", pass_context=True)
    async def get_score(self, ctx, username):
        try:
            score = "User not found"
            for user in ctx.guild.members:
                if user.name == username:
                    score = self.score_user(user.id)
                    continue
        except Exception as e:
            print(e)
            score = "Erreur lors de la requete {}".format(e)
        await ctx.message.channel.send('Le score de {} est de : {} '.format(username, score))

    # @commands.command(name="addScore", description="Met a jour le score blague de merde", pass_context=True)
    async def add_to_score(self, ctx, username, add_score_point):
        try:
            for user in ctx.guild.members:
                if user.name == username:
                    self.add_score(str(user.id), add_score_point)
                    await ctx.message.channel.send("Le score de {} est maintenant de {}".format(user.name, self.score_user(user.id)))
                    continue
        except Exception as e:
            print(e)
            await ctx.message.channel.send('Erreur pour mettre a jour le score de {} : {}'.format(username, e))

    # @commands.command(name="allScore", description="Affiche le score de toutes les personnes du serveur", pass_context=True)
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
    async def score(self, ctx, username = "", add_score_point=0):
        if (username.strip() != "" and int(add_score_point) != 0):
            await self.add_to_score(ctx, username, add_score_point)
        elif (username.strip() != ""):
            await self.get_score(ctx, username)
        else:
            await self.all_score(ctx)

### FIN SCORE ###

    @commands.command(name="hentai", description=":smirk:", pass_context=True)
    async def hentai_pic(self, ctx):
        await self.send_pic(ctx, 'hentai')

    @commands.command(name="nekobot", description="The type of image to get. Current types: hass, hmidriff, pgif, 4k, hentai, holo, hneko, neko, hkitsune, kemonomimi, anal, hanal, gonewild, kanna, ass, pussy, thigh, hthigh, gah, coffee, food", pass_context=True)
    async def send_pic(self, ctx, img_type):
        response = requests.get("https://nekobot.xyz/api/image?type=" + img_type)
        if (response.status_code == 200):
            await ctx.message.channel.send(response.json()['message'])

    @commands.command(name="nekos", description="femdom, tickle, classic, ngif, erofeet, meow, erok, poke, les, v3, hololewd, nekoapi_v3.1, lewdk, keta, feetg, nsfw_neko_gif, eroyuri, kiss, 8ball, kuni, tits, pussy_jpg, cum_jpg, pussy, lewdkemo, lizard, slap, lewd, cum, cuddle, spank, smallboobs, goose, Random_hentai_gif, avatar, fox_girl, nsfw_avatar, hug, gecg, boobs, pat, feet, smug, kemonomimi, solog, holo, wallpaper, bj, woof, yuri, trap, anal, baka, blowjob, holoero, feed, neko, gasm, hentai, futanari, ero, solo, waifu, pwankg, eron, erokemo", pass_context=True)
    async def nekos(self, ctx, neko_type = "", number = 1):
        if (neko_type == "") :
            await ctx.message.channel.send('femdom, tickle, classic, ngif, erofeet\n meow, erok, poke, les, v3, hololewd\n nekoapi_v3.1, lewdk, keta, feetg, nsfw_neko_gif, eroyuri\n kiss, 8ball, kuni, tits, pussy_jpg, cum_jpg\n pussy, lewdkemo, lizard, slap, lewd, cum\n cuddle, spank, smallboobs, goose, Random_hentai_gif, avatar\n fox_girl, nsfw_avatar, hug, gecg, boobs, pat\n feet, smug, kemonomimi, solog, holo, wallpaper\n bj, woof, yuri, trap, anal, baka\n blowjob, holoero, feed, neko, gasm, hentai\n futanari, ero, solo, waifu, pwankg, eron, erokemo')
            return False
        if (int(number) <= 0) :
            ctx.message.channel.send('Le 2e argument doit être un entier supérieur à 0')
            return False
        for i in range(number) :
            response = requests.get('https://nekos.life/api/v2/img/' + neko_type)
            if (response.status_code == 200):
                await ctx.message.channel.send(response.json()['url']) 
        return true

    @commands.command(name='random', description='Random WIP', pass_context=True)
    async def choix_aleatoire(self, ctx, *args) :
        if len(args) == 1 and args[0].isdigit():
            rand_num = random.randint(1, int(args[0]))
            await ctx.message.channel.send("Aléatoire de 1 à {} => {}".format(str(args[0]), rand_num))
            return True
        elif len(args) == 2 and args[0].isdigit() and args[1].isdigit():
            rand_num = random.randint(int(args[0]), int(args[1]))
            await ctx.message.channel.send(" Aléatoire entre {} et {} => {}".format(str(args[0]), str(args[1]), str(rand_num) ) )
            return True
        else : 
            await ctx.message.channel.send("{}".format(str(random.choice(args))))
            return True


### SCORE DE SEL ###


    async def get_score_sel(self, ctx, username):
        try:
            score = "User not found"
            for user in ctx.guild.members:
                if user.name == username:
                    score = self.sel_user(user.id)
                    continue
        except Exception as e:
            print(e)
            score = "Erreur lors de la requete {}".format(e)
        await ctx.message.channel.send('Le sel de {} est de : {} '.format(username, score))

    async def add_to_sel(self, ctx, username, add_score_point):
        try:
            for user in ctx.guild.members:
                if user.name == username:
                    self.add_sel(str(user.id), add_score_point)
                    await ctx.message.channel.send("Le sel de {} est maintenant de {}".format(user.name, self.sel_user(user.id)))
                    continue
        except Exception as e:
            print(e)
            await ctx.message.channel.send('Erreur pour mettre a jour le score de {} : {}'.format(username, e))

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
    async def sel(self, ctx, username = "", add_score_point=0):
        if (username.strip() != "" and int(add_score_point) != 0):
            await self.add_to_sel(ctx, username, add_score_point)
        elif (username.strip() != ""):
            await self.get_score_sel(ctx, username)
        else:
            await self.all_sel(ctx)


### FIN DU SEL ###

### SCORE DE GORGEE ###


    async def get_score_gorgee(self, ctx, username):
        try:
            score = "User not found"
            for user in ctx.guild.members:
                if user.name == username:
                    score = self.gorgee_user(user.id)
                    continue
        except Exception as e:
            print(e)
            score = "Erreur lors de la requete {}".format(e)
        await ctx.message.channel.send('Le nombre de gorgee est de {} est de : {} '.format(username, score))

    async def add_to_gorgee(self, ctx, username, add_score_point):
        try:
            for user in ctx.guild.members:
                if user.name == username:
                    self.add_gorgee(str(user.id), add_score_point)
                    await ctx.message.channel.send("Le nombre de gorgee est de {} est maintenant de {}".format(user.name, self.gorgee_user(user.id)))
                    continue
        except Exception as e:
            print(e)
            await ctx.message.channel.send('Erreur pour mettre a jour le score de {} : {}'.format(username, e))

    async def all_gorgee(self, ctx): 
        try:
            for user in ctx.guild.members:
                try:
                    score = self.gorgee_user(str(user.id))
                except:
                    score = "Impossible de récupérer le score."
                    continue
                await ctx.message.channel.send("Le nombre de gorgee est de {} est de : {}".format(user.name, score))
        except Exception as e:
            await ctx.message.channel.send('Une erreur est survenu : {}'.format(e))

    @commands.command(name="gorgee", description = "gorgee", pass_context=True)
    async def gorgee(self, ctx, username = "", add_score_point=0):
        if (username.strip() != "" and int(add_score_point) != 0):
            await self.add_to_gorgee(ctx, username, add_score_point)
        elif (username.strip() != ""):
            await self.get_score_gorgee(ctx, username)
        else:
            await self.all_gorgee(ctx)


### FIN DU GORGÉE ###



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


### SEL ###

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

### FIN SEL ###

### GORGEE ###

    def gorgee_user(self, discord_tag):
        mariadb_connection = mariadb.connect(user='asphyx', password='', database='discord_private_chat')
        cursor = mariadb_connection.cursor()

        cursor.execute('SELECT `score` FROM `gorgee` WHERE `discord_tag` = "{}"'.format(discord_tag))
        res = cursor.fetchone()[0]
        mariadb_connection.close()
        return res

    def add_gorgee(self, discord_tag, value):
        mariadb_connection = mariadb.connect(user='asphyx', password='', database='discord_private_chat')
        cursor = mariadb_connection.cursor()
        current = self.sel_user(discord_tag)

        value = str(int(value) + int(current))
        cursor.execute('UPDATE gorgee SET score = {} WHERE discord_tag = "{}"'.format(value, str(discord_tag)))
        mariadb_connection.commit()
        mariadb_connection.close()

    def create_user_gorgee_database(self, username, userid):
        try:
            mariadb_connection = mariadb.connect(user='asphyx', password='', database='discord_private_chat')
            cursor = mariadb_connection.cursor()
            cursor.execute('INSERT INTO gorgee(`username`, `score`, `discord_tag`) VALUES ({}, 0, {});'.format(username, userid))
            mariadb_connection.commit()
            mariadb_connection.close()
        except Exception as e:
            print(e)

### FIN GORGEE ###

def setup(bot):
    bot.add_cog(PrivateChat())
