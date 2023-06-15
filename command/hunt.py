import discord
from discord.ext import commands
import main
import random

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
            equipment = {
                "2": "<:kiemC1:1118523931406631023>",
                "3": "<:kiemC2:1118524150756163686>",
                "4": "<:kiemC3:1118524395766415370>",
                "0": "Không có vật phẩm nào cả"
            }
            await main.open_account(ctx.author.id)
            data = await main.get_bank_data()
            if data[f"{ctx.author.id}"]["hp"] <= 24:
                return await ctx.send(f'ban con {data[f"{ctx.author.id}"]["hp"]}HP khong du de di san')
            thuk1 = ["<a:thuK1gif:1115322059841613874>", "<a:thuK1gif:1116033962595328001>","<a:thuK1gif:1116034229587955723>", "<a:thuK4gif:1116038514044317776>"]
            thuk2 = ["<a:thuK1gif:1116034300576542751>","<a:thuK1gif:1116034392310161462>", "<a:thuK2gif:1116034488837881856>", "<a:thuK4gif:1116035682285133854>" ]
            thuk3 = ["<a:thuK2gif:1116034548443127894>", "<a:thuK2gif:1116034663568384021>", "<a:thuK2gif:1116034816111034479>", "<a:thuK4gif:1116035614593253387>"]
            thuk4 = ["<:philong:1115318989137133719>","<a:thuK3gif:1116035130004361357>", "<a:thuK3gif:1116035190075183175>", "<a:thuK:1116038561951662121>"]
            thuk5 = ["<a:thuK3gif:1116035320601923664>","<a:thuK3gif:1116035401702973462>", "<a:thuK3gif:1116035547614425098>","<a:thuK4gif:1116038448965501058>"]
            quaix2 = False
            def hunt():
                rank = data[str(ctx.author.id)]["lv"]
                if rank <= 5:
                    chance = random.choice(["K1"]*60+["K2"]*40)
                elif 5 < rank <= 10:
                    chance = random.choice(["K1"]*50+["K2"]*40+["K3"]*6+["K0"]*4)
                else:
                    chance = random.choice(["K1"] * 520 + ["K2"]*350 + ["K3"] * 55 + ["K4"] * 3 + ["K5"]*2 + ["K0"]*70)
                place = random.choice(["Thung lũng namec","Thung Lũng Tre","Vách Núi Đen","Doanh trại độc nhãn","Đảo Kame"])
                if chance == "K0":
                    hunt = "🚫"
                    hp = 0
                    vang = 0
                elif chance == "K1":
                    hunt = random.choice(thuk1)
                    hp = 2
                    vang = 3
                elif chance == "K2":
                    hunt = random.choice(thuk2)
                    hp = 3
                    vang = 5
                elif chance == "K3":
                    hunt = random.choice(thuk3)
                    hp = 7
                    vang = 8
                elif chance == "K4":
                    hunt = random.choice(thuk4)
                    hp = 8
                    vang = 10
                else:
                    hunt = random.choice(thuk5)
                    hp = 12
                    vang = 15
                exp = random.randint(1,4)
                return {"k": chance, "hunt": hunt, "vang": vang, "hp": hp, "place": place, "exp": exp}
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
                if hunt["hunt"] == "🚫":
                    pass
                else:
                    data[f"{ctx.author.id}"]["zoo"].append(hunt["hunt"])
                main.save_member_data(data)
            data[f"{ctx.author.id}"]["point"] += coin
            data[f"{ctx.author.id}"]["hp"] -= hp
            data[str(ctx.author.id)]["exp"] += exp
            if data[str(ctx.author.id)]["exp"] >= 100:
                data[str(ctx.author.id)]["exp"] = 0
                data[str(ctx.author.id)]["lv"] += 1
                lv = data[str(ctx.author.id)]["lv"]
                await ctx.reply(f"**{ctx.author.name}** đã tăng cấp lên **lv{lv}**", delete_after=2)
            lv = data[str(ctx.author.id)]["lv"]
            main.save_member_data(data)
            trang_bi = equipment[str(str((await main.get_bank_data())[str(ctx.author.id)]["equip"]))]
            await ctx.send(f"🐺  | **{ctx.author.name}** đã đi săn ở **{place}**:\n    | Bạn bắt được: {quai}\n    | +{coin}<:vang:1116221866273681510>\n    | -{hp}HP\n    | +{exp}exp\n    | level: {lv}\n    | Vật phẩm đang sử dụng: {trang_bi}")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Hunt(bot))