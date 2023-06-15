import discord
from discord.ext import commands
from command.cache.var import weapon

class Wp(commands.Cog):
    config = {
        "name": "wp",
        'desc': "xem thong tin vu khi",
        "use": "wp <weapon_id>",
        "author": "Anh Duc"
    }
    def __init__(self,bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1,4,commands.BucketType.user)
    async def wp(self, ctx,weapon_id:str=None):
        try:
            if weapon_id == None:
                return await ctx.send("Bạn cần nhập id của trang bị để xem thông tin về trang bị đo")
            data = weapon[weapon_id]
            msg = f'📑Thông tin về vật phẩm {data["icon"]}:\n- ID trang bị: {data["id"]}\n- Mô tả: {data["desc"]}\n- Giá: {data["price"]}<:vang:1116221866273681510>'
            await ctx.send(msg)
        except:
            await ctx.send("ID không tồn tại")
async def setup(bot):
    await bot.add_cog(Wp(bot))