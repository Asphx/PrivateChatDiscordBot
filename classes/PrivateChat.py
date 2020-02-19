import asyncio
from discord.ext import commands


class PrivateChat(commands.Cog):

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

    @commands.command(name="score", description="Score blague de merde", pass_context=True)
    async def score(ctx): 
        pass

    @commands.command(name='getScore', description:"Score du joueur", pass_context=True)
    async def get_score(ctx):
        pass
    
                
def setup(bot):
    bot.add_cog(PrivateChat())
