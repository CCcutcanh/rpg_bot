import discord
from discord.ext import commands
from main import get_bank_data, save_member_data, open_account

class Add(commands.Cog):
    config = {
        "name": "Add",
        "desc": "",
        "use": "add <@tag>",
        "author": 'Anh Duc'
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def add(self, ctx, mention: discord.Member = None, coin: int = 0):
        if not ctx.author.id in [716146182849560598,977482577168457748]:
            return
        await open_account(mention.id)
        mem = (await get_bank_data())
        mem[str(mention.id)]["point"] = coin
        save_member_data(mem)
        await ctx.send("sucess")
async def setup(bot):
    await bot.add_cog(Add(bot))