import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=('.'))
bot.load_extension('classes.PrivateChat')


async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))


async def on_message(self, message):
    # print('Message from {0.author}: {0.content}'.format(message))
    # print('------------')
    pass

bot.run('NjM2NTcxOTQzMzczNTA0NTM0.XoIfng.gSIcXIgYuMrduPgr-vmVMVFmC6Y')
