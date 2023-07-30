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
            await open_account(ctx.author.id)
            data = await get_bank_data()
            coin = data[str(ctx.author.id)]["point"]
            msg_send = f"**Đây là các vật phẩm, kĩ năng, bạn có thể mua và học trong shop**:\n"
            keys = weapon.keys()
            hp = "==Vật phẩm hồi HP=="
            hunt = "\n==Vật phẩm hỗ trợ đi săn=="
            pvp = "\n==Vật phẩm hỗ trợ PVP=="
            skill = "\n===SKILL==="
            for i in keys:
                if i == "00":
                    pass
                else:
                    info = weapon[i]
                    icon = info["icon"]
                    id = i
                    price = str(info["price"])
                    category = info["category"]
                    content = "\n" + icon + " | " + id + " | " + price + "<:vang:1116221866273681510>"
                    if category == "HP":
                        hp += content
                    elif category == "hunt":
                        hunt += content
                    elif category == "pvp":
                        pvp += content
                    elif category == 'skill':
                        skill += content
            msg_send += hp + hunt + pvp + skill
            msg_send +=f"\n\n_Reply tin nhắn này với id vật phẩm bạn muốn mua để mua vật phẩm_\n**Sử dụng lệnh wp <weapon_id> để xem thông tin chi tiết về vật phẩm**\n*Vật phẩm bạn mua sẽ thay thế vật phẩm hiện tại bạn đang sử dụng ngoại trừ vật phẩm hồi HP*\nTổng số vàng hiện có: {coin}<:vang:1116221866273681510>"
            send = await ctx.send(msg_send)
            def check(m):
                return m.author.id == ctx.author.id and m.channel == ctx.channel and m.reference is not None and m.reference.message_id == send.id
            choose = await self.bot.wait_for("message", check=check)
            coin = data[str(ctx.author.id)]["point"]
            list_equip = []
            list_equip_pvp = []
            skill = []
            all_equip = weapon.keys()
            for i in all_equip:
                if i == "00":
                    pass
                k = weapon[i]["category"]
                if k == 'pvp':
                    list_equip_pvp.append(i)
                elif k == "hunt":
                    list_equip.append(i)
                elif k == "skill":
                    skill.append(i)
            if not choose.content in all_equip:
                return await ctx.send("Id không hợp lệ")
            wp_choose = weapon[choose.content]
            if choose.content == "01":
                if coin < wp_choose["price"]:
                    return await ctx.send("**Bạn không đủ <:vang:1116221866273681510> để mua vật phẩm này**")
                if data[str(ctx.author.id)]["hp"] > 60:
                    return await ctx.send("**HP quả bạn đã quá 60 không thể sử dụng bình HP**")
                data[str(ctx.author.id)]["hp"] += 40
                data[str(ctx.author.id)]["point"] -= wp_choose["price"]
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
            elif choose.content in skill:
                data[f"{ctx.author.id}"]["skill"] = int(choose.content)
            icon = wp_choose["icon"]
            save_member_data(data)
            await ctx.send(f"Bạn đã mua vật phẩm {icon}, vật phẩm sẽ được áp dụng từ bây giờ")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Shop(bot))
