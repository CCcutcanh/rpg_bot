import discord
from discord.ext import commands

class Allquai(commands.Cog):
    config = {
        "name": "allquai",
        "desc": "show tat ca cac quai",
        "use": "allquai",
        "author": "anh duc"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def allquai(self, ctx):
        thuk1 = ["<a:thuK1gif:1115322059841613874>", "<a:thuK1gif:1116033962595328001>","<a:thuK1gif:1116034229587955723>"]
        thuk2 = ["<a:thuK1gif:1116034300576542751>","<a:thuK1gif:1116034392310161462>", "<a:thuK2gif:1116034488837881856>" ]
        thuk3 = ["<a:thuK2gif:1116034548443127894>", "<a:thuK2gif:1116034663568384021>", "<a:thuK2gif:1116034816111034479>"]
        thuk4 = ["<:philong:1115318989137133719>","<a:thuK3gif:1116035130004361357>", "<a:thuK3gif:1116035190075183175>"]
        thuk5 = ["<a:thuK3gif:1116035320601923664>","<a:thuK3gif:1116035401702973462>", "<a:thuK3gif:1116035547614425098>"]
        await ctx.send(thuk1+thuk2+thuk3+thuk4+thuk5)
        quaisau = ['<a:thuK:1116038561951662121>', '<a:thuK1gif:1115322059841613874>', ' <a:thuK1gif:1116033962595328001>', ' <a:thuK1gif:1116034229587955723>', ' <a:thuK1gif:1116034300576542751>', '<a:thuK1gif:1116034392310161462>', ' <a:thuK2gif:1116034488837881856>', ' <a:thuK2gif:1116034548443127894>', ' <a:thuK2gif:1116034663568384021>', ' <a:thuK2gif:1116034816111034479>', ' <a:thuK2gif:1116035009090953247>', '<a:thuK3gif:1116035130004361357>', '<a:thuK3gif:1116035190075183175> ', '<a:thuK3gif:1116035320601923664>', '<a:thuK3gif:1116035401702973462>', '<a:thuK3gif:1116035547614425098> ', '<a:thuK4gif:1116035614593253387> ', '<a:thuK4gif:1116035682285133854>', '<a:thuK4gif:1116038448965501058>', '<a:thuK4gif:1116038514044317776>']
        await ctx.send("quai sau thay doi" + "\\" + quaisau[0] + "\\" + quaisau[16] + "\\" + quaisau[17] + "\\" + quaisau[18] + "\\" + quaisau[19])
        
async def setup(bot):
    await bot.add_cog(Allquai(bot))