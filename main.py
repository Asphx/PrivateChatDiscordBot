import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=('.'))
bot.load_extension('classes.PrivateChat')
bot.load_extension('classes.Bet')
bot.load_extension('classes.Scores')
bot.load_extension('classes.Sel')


async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))


async def on_message(self, message):
    # print('Message from {0.author}: {0.content}'.format(message))
    # print('------------')
    pass

with open('key') as f:
        cle = f.readline().strip()

bot.run(cle)