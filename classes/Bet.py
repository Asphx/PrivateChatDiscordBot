import mysql.connector as mariadb
import asyncio
from discord.ext import commands
import discord

class Bet(commands.Cog):

    def __init__(self):
        pass
    
    @commands.command(name="test", description="Doing some shitty test", pass_context=True)
    async def testing(self, ctx, usertagged: discord.Member):
        print(usertagged)
        print(type(usertagged))
        
        await ctx.message.channel.send('user : '.format(usertagged))

        await ctx.message.channel.send(
            '"name" => {} '.format(usertagged.name)
            )

        await ctx.message.channel.send(
            '"id" => {} '.format(usertagged.id)
        )
        await ctx.message.channel.send(
            '"discriminator" => {} '.format(usertagged.discriminator)
        )
        return True

def setup(bot):
    bot.add_cog(Bet())
