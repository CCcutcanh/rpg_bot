import discord
from discord.ext import commands
from main import get_bank_data, save_member_data
import random

class Clear(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.hybrid_command()
    async def clear(self, ctx, user):
        if not ctx.author.id in [716146182849560598,977482577168457748]:
            return
        users = (await get_bank_data())
        users[str(user)] = {}
        users[str(user)]["point"] = 25
        users[str(user)]["zoo"] = []
        users[str(user)]["hp"] = 5
        users[str(user)]["attack"] = 0
        users[str(user)]["equip"] = 0
        users[str(user)]["exp"] = 0
        users[str(user)]["lv"] = 1
        users[str(user)]["zp"] = 0
        users[str(user)]["character"] = random.choice(["santa", "vegeta", "android20"])
        save_member_data(users)
        await ctx.send("clear!")
async def setup(bot):
    await bot.add_cog(Clear(bot))