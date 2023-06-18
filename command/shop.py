import discord
from discord.ext import commands
from main import get_bank_data, open_account, save_member_data
from command.cache.var import weapon

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
            send = await ctx.send(f"**Đây là các vật phẩm hiện có trong Shop:**\n\n*==Vật phẩm hồi HP==*\n<:binhHP:1118551444497375292> | id: 01 | 25<:vang:1116221866273681510>\n\n*==Vật phẩm tăng số quái có thể săn==*\n <:kiemC1:1118523931406631023> | id: 02 | 80<:vang:1116221866273681510>\n<:kiemC2:1118524150756163686> | id: 03 | 110<:vang:1116221866273681510>\n<:kiemC3:1118524395766415370> | id: 04 | 150<:vang:1116221866273681510>\n==*Vật phẩm hỗ trợ pvp*==\n <:pvpkiem3:1119872683367202846> | id: 05 | 140<:vang:1116221866273681510>\n<:pvpkiem2:1119872536616898560> | id: 06 | 150<:vang:1116221866273681510>\n<:pvpkiem1:1119872240478068826> | id: 07 | 110<:vang:1116221866273681510>\n\nReply tin nhắn này với id vật phẩm bạn muốn mua để mua vật phẩm\n**Sử dụng lệnh wp <weapon_id> để xem thông tin chi tiết về vật phẩm\n*Vật phẩm bạn mua sẽ thay thế vật phẩm hiện tại bạn đang sử dụng ngoại trừ vật phẩm hồi HP*\nTổng số vàng hiện có: {coin}<:vang:1116221866273681510>")
            def check(m):
                return m.author.id == ctx.author.id and m.channel == ctx.channel and m.reference is not None and m.reference.message_id == send.id
            choose = await self.bot.wait_for("message", check=check)
            coin = data[str(ctx.author.id)]["point"]
            list_equip = ["01","02","03","04"]
            list_equip_pvp = ["05","06","07"]
            all_equip = list_equip + list_equip_pvp
            if not choose.content in all_equip:
                return await ctx.send("Id không hợp lệ")
            wp_choose = weapon[choose.content]
            if choose.content == "01":
                if coin < wp_choose["price"]:
                    return await ctx.send("**Bạn không đủ :vang: để mua vật phẩm này**")
                if data[str(ctx.author.id)]["hp"] > 60:
                    return await ctx.send("**HP quả bạn đã quá 60 không thể sử dụng bình HP**")
                data[str(ctx.author.id)]["hp"] += 40
                save_member_data(data)
                hp = data[str(ctx.author.id)]["hp"]
                return await ctx.send(f"Chỉ số hp của bạn đã tăng lên {hp}")
            
            if coin < wp_choose["price"]:
                return await ctx.send("**Bạn không đủ <:vang:1116221866273681510> để mua vật phẩm này**")
            data[str(ctx.author.id)]["point"] -= wp_choose["price"]
            if choose.content in list_equip:
                data[str(ctx.author.id)]["equip"] = int(choose.content)
            elif choose.content in list_equip_pvp:
                data[str(ctx.author.id)]["pvp_equip"] = int(choose.content)
            icon = wp_choose["icon"]
            save_member_data(data)
            await ctx.send(f"Bạn đã mua vật phẩm {icon}, vật phẩm sẽ được áp dụng từ bây giờ")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Shop(bot))