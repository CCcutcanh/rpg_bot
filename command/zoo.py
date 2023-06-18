import discord
from discord.ext import commands
from main import get_bank_data, open_account
from command.cache.var import thuk1,thuk2,thuk3,thuk4,thuk5, weapon
class Zoo(commands.Cog):
    config = {
        "name": "zoo",
        "desc": "xem nhung quai da bat duoc",
        "use": "zoo",
        "author": "Anh Duc"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1,4,commands.BucketType.user)
    async def zoo(self, ctx):
        try:
            
            def get_sub(x):
                normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
                sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
                res = x.maketrans(''.join(normal), ''.join(sub_s))
                return x.translate(res)
            msg = f"🐢Đây là tất cả các quái **{ctx.author.name}** đã bắt được🐢:\n"
            common = "<:C_:1118555871958552688> | "
            uncommon = "\n<:U_:1118555223800152065> | "
            rare = "\n<:R_:1118555228481015858> | "
            ultra_rare = "\n<:UR:1118555221862383777> | "
            legendary = "\n <:L_:1118556123067322418>| "
            await open_account(ctx.author.id)
            data = (await get_bank_data())[f"{ctx.author.id}"]["zoo"]
            if True:
                for quai in data[:]:
                    count = str(data.count(quai))
                    if int(count) == 0:
                        pass
                    else:
                        for i in range(int(count)):
                            data.remove(quai)
                        if quai in thuk1:
                            common += quai + get_sub(count)
                        elif quai in thuk2:
                            uncommon += quai + get_sub(count)
                        elif quai in thuk3:
                            rare += quai + get_sub(count)
                        elif quai in thuk4:
                            ultra_rare += quai + get_sub(count)
                        else:
                            legendary += quai + get_sub(count)
            msg += common + uncommon + rare + ultra_rare + legendary
            coin = (await get_bank_data())[f"{ctx.author.id}"]["point"]
            hp = (await get_bank_data())[str(ctx.author.id)]["hp"]
            trang_bi = weapon["0" + str(str((await get_bank_data())[str(ctx.author.id)]["equip"]))]["icon"]
            equip_pvp = weapon["0"+str((await get_bank_data())[str(ctx.author.id)]["pvp_equip"])]["icon"]
            data = await get_bank_data()
            lv = data[str(ctx.author.id)]["lv"]
            exp = data[str(ctx.author.id)]["exp"]
            zp = data[str(ctx.author.id)]["zp"]
            cha = data[str(ctx.author.id)]["character"]
            msg +=f"\nTổng số vàng hiện có: {coin}<:vang:1116221866273681510>\nChỉ số HP: {hp}\n<:level:1119126214670561382>: {lv}\nexp: {exp}\nVật phẩm đang sử dụng: {trang_bi}\nTrang bị pvp: {equip_pvp}\nzoo point: {zp}\nNhân vật của bạn: {cha}"
            await ctx.send(msg)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Zoo(bot))