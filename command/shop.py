import discord
from discord.ext import commands
from main import get_bank_data, open_account, save_member_data
class Shop(commands.Cog):
    config = {
        "name": "shop",
        "desc": "shop mua vat pham",
        "use": "shop",
        "author": "Anh Duc"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1,4,commands.BucketType.user)
    async def shop(self, ctx):
        try:
            data = await get_bank_data()
            coin = data[str(ctx.author.id)]["point"]
            send = await ctx.send(f"**Đây là các vật phẩm hiện có trong Shop:**\n\n*==Vật phẩm hồi HP==*\n<:binhHP:1118551444497375292> | id: 01 | 25<:vang:1116221866273681510>\n\n*==Vật phẩm tăng số quái có thể săn==*\n <:kiemC1:1118523931406631023> | id: 02 | 80<:vang:1116221866273681510>\n<:kiemC2:1118524150756163686> | id: 03 | 110<:vang:1116221866273681510>\n<:kiemC3:1118524395766415370> | id: 04 | 150<:vang:1116221866273681510>\n\nReply tin nhắn này với id vật phẩm bạn muốn mua để mua vật phẩm\n**Sử dụng lệnh wp <weapon_id> để xem thông tin chi tiết về vật phẩm\n*Vật phẩm bạn mua sẽ thay thế vật phẩm hiện tại bạn đang sử dụng ngoại trừ vật phẩm hồi HP*\nTổng số vàng hiện có: {coin}<:vang:1116221866273681510>")
            def check(m):
                return m.author.id == ctx.author.id and m.channel == ctx.channel and m.reference is not None and m.reference.message_id == send.id
            choose = await self.bot.wait_for("message", check=check)
            if choose.content == "01":
                if data[str(ctx.author.id)]["point"] < 25:
                    return await ctx.send("Bạn không đủ vàng để mua vật phẩm này")
                elif data[str(ctx.author.id)]["hp"] > 60:
                    return await ctx.send("Số HP của bạn lớn hơn 60, không thể mua bình HP")
                data[str(ctx.author.id)]["point"] -= 25
                data[str(ctx.author.id)]["hp"] += 40
                save_member_data(data)
                return await ctx.send(f'Chỉ số HP của bạn đã tăng lên {data[str(ctx.author.id)]["hp"]}HP')
            elif choose.content == "02":
                if data[str(ctx.author.id)]["point"] < 80:
                    return await ctx.send("Bạn không đủ vàng để mua vật phẩm này")
                data[str(ctx.author.id)]["point"] -= 80
                data[str(ctx.author.id)]["equip"] = 2
                save_member_data(data)
                return await ctx.send("Bạn đã mua vật phẩm <:kiemC1:1118523931406631023>, vật phẩm sẽ được áp dụng từ bây giờ")
            elif choose.content == "03":
                if data[str(ctx.author.id)]["point"] < 110:
                    return await ctx.send("Bạn không đủ vàng để mua vật phẩm này")
                data[str(ctx.author.id)]["point"] -= 110
                data[str(ctx.author.id)]["equip"] = 3
                save_member_data(data)
                return await ctx.send("Bạn đã mua vật phẩm <:kiemC2:1118524150756163686>, vật phẩm sẽ được áp dụng từ bây giờ")
            elif choose.content == "04":
                if data[str(ctx.author.id)]["point"] < 150:
                    return await ctx.send("Bạn không đủ vàng để mua vật phẩm này")
                data[str(ctx.author.id)]["point"] -= 150
                data[str(ctx.author.id)]["equip"] = 4
                save_member_data(data)
                await ctx.send("Bạn đã mua vật phẩm <:kiemC3:1118524395766415370>, vật phẩm sẽ được áp dụng từ bây giờ")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Shop(bot))