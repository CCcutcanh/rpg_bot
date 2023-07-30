import discord
from discord.ext import commands
import main
import random
from command.cache.var import thuk1,thuk2,thuk3,thuk4,thuk5, weapon
from captcha.image import ImageCaptcha
import string

class Hunt(commands.Cog):
    config = {
        "name": "hunt",
        "desc": "san thu",
        "use": "hunt",
        "author": "Anh Duc"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 9, commands.BucketType.user)
    async def hunt(self, ctx):
        try:
            await main.open_account(ctx.author.id)
            data = await main.get_bank_data()
            if data[str(ctx.author.id)]["captcha"] == 0:
                image = ImageCaptcha(width = 300, height = 100)
                password = list(string.ascii_lowercase + "0123456789" + "!#$%&*+<=>?@^{}")
                result = ""
                for i in range(6):
                    result += random.choice(password)
                image.generate(result)
                image.write(result, ("captcha") + ".png")
                file = discord.File("captcha.png")
                send = await ctx.send(file = file)
                def check(m):
                    return m.author.id == ctx.author.id and m.channel == ctx.channel and m.reference is not None and m.reference.message_id == send.id
                captcha = await self.bot.wait_for("message", check=check)
                if captcha.content != result:
                    await ctx.send("Sai captcha!")
                    return
                data[str(ctx.author.id)]["captcha"] = 30
                main.save_member_data(data)
                await ctx.send("Cảm ơn bạn đã giải captcha")
            if data[f"{ctx.author.id}"]["hp"] <= 24:
                return await ctx.send(f'ban con {data[f"{ctx.author.id}"]["hp"]}HP khong du de di san')
            
            quaix2 = False
            def hunt():
                user = data[f"{ctx.author.id}"]
                equip = user["equip"]
                rank = data[str(ctx.author.id)]["lv"]
                if rank <= 5:
                    chance = random.choice(["K1"]*65+["K2"]*35)
                elif 5 < rank < 10:
                    chance = random.choice(["K1"]*50+["K2"]*40+["K3"]*3+["K0"]*7)
                else:
                    chance = random.choice(["K1"] * 520 + ["K2"]*360 + ["K3"] * 35 + ["K4"] * 3 + ["K5"]*2 + ["K0"]*80)
                place = random.choice(["Thung lũng namec","Thung Lũng Tre","Vách Núi Đen","Doanh trại độc nhãn","Đảo Kame"])
                if chance == "K0":
                    hunt = "🚫"
                    hp = 0
                    vang = 0
                    zp = 0
                elif chance == "K1":
                    hunt = random.choice(thuk1)
                    hp = 2
                    vang = 3
                    zp = 2
                elif chance == "K2":
                    hunt = random.choice(thuk2)
                    hp = 3
                    vang = 5
                    zp = 3
                elif chance == "K3":
                    hunt = random.choice(thuk3)
                    hp = 7
                    vang = 8
                    zp = 4
                elif chance == "K4":
                    hunt = random.choice(thuk4)
                    hp = 8
                    vang = 10
                    zp = 5
                else:
                    hunt = random.choice(thuk5)
                    hp = 12
                    vang = 15
                    zp = 6
                exp = random.randint(1,4)
                return {"k": chance, "hunt": hunt, "vang": vang, "hp": hp, "place": place, "exp": exp,"zp": zp}
            if data[str(ctx.author.id)]['equip'] == 2:
                chance = random.choice(["Y"] * 40 + ["N"]*60)
                if chance == "Y":
                    quaix2 = True
            elif data[str(ctx.author.id)]["equip"] == 3:
                chance = random.choice(["Y"]*60 + ["N"]*40)
                if chance == "Y":
                    quaix2 = True
            elif data[str(ctx.author.id)]["equip"] == 4:
                quaix2 = True
            if quaix2:
                hunt1 = hunt()
                hunt2 = hunt()
                quai = hunt1["hunt"] + hunt2['hunt']
                if hunt1["place"] == hunt2["place"]:
                    place = hunt1["place"]
                else:
                    place = hunt1["place"] + " và " + hunt2["place"]
                hp = hunt1["hp"] + hunt2["hp"]
                coin = hunt1["vang"] + hunt2["vang"]
                exp = hunt1["exp"] + hunt2["exp"]
                zp = hunt1["zp"] + hunt2["zp"]
                if hunt1["hunt"] == "🚫":
                    pass
                else:
                    data[f"{ctx.author.id}"]["zoo"].append(hunt1["hunt"])
                if hunt2["hunt"] == "🚫":
                    pass
                else:
                    data[f"{ctx.author.id}"]["zoo"].append(hunt2["hunt"])
                main.save_member_data(data)
            else:
                hunt = hunt()
                place = hunt["place"]
                quai = hunt["hunt"]
                hp = hunt["hp"]
                coin = hunt["vang"]
                exp = hunt["exp"]
                zp = hunt["zp"]
                if hunt["hunt"] == "🚫":
                    pass
                else:
                    data[f"{ctx.author.id}"]["zoo"].append(hunt["hunt"])
                main.save_member_data(data)
            data[f"{ctx.author.id}"]["point"] += coin
            data[f"{ctx.author.id}"]["hp"] -= hp
            data[str(ctx.author.id)]["zp"] += zp
            data[str(ctx.author.id)]["captcha"] -= 1
            if data[str(ctx.author.id)]["zp"] >= 100:
                await ctx.send(f"**Điểm zoo point của {ctx.author.name} đã đủ 100,  bạn sẽ được tăng 0,2 attack, số point hiện tại sẽ về 0**", delete_after=5)
                data[str(ctx.author.id)]["attack"] += 0.2
                data[str(ctx.author.id)]["zp"] = 0
            data[str(ctx.author.id)]["exp"] += exp
            if data[str(ctx.author.id)]["exp"] >= 100:
                data[str(ctx.author.id)]["exp"] = 0
                data[str(ctx.author.id)]["lv"] += 1
                lv = data[str(ctx.author.id)]["lv"]
                await ctx.reply(f"**{ctx.author.name} đã tăng cấp lên <:level:1119126214670561382>{lv}**", delete_after=5)
            lv = data[str(ctx.author.id)]["lv"]
            main.save_member_data(data)
            trang_bi = weapon["0"+str(str((await main.get_bank_data())[str(ctx.author.id)]["equip"]))]["icon"]
            await ctx.send(f"<:meo:1119142394668011651>  | **{ctx.author.name}** đã đi săn ở **{place}**:\n    | Bạn bắt được: {quai}\n    | +{coin}<:vang:1116221866273681510>\n    | -{hp}HP\n    | +{exp}exp\n    | <:level:1119126214670561382>: {lv}\n    | + {zp} zoo point\n    | Vật phẩm đang sử dụng: {trang_bi}")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Hunt(bot))