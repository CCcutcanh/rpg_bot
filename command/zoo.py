import discord
from discord.ext import commands
from main import get_bank_data, open_account

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
            equipment = {
                "2": "<:kiemC1:1118523931406631023>",
                "3": "<:kiemC2:1118524150756163686>",
                "4": "<:kiemC3:1118524395766415370>",
                "0": "Không có vật phẩm nào cả"
            }
            def get_sub(x):
                normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
                sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
                res = x.maketrans(''.join(normal), ''.join(sub_s))
                return x.translate(res)
            msg = "🐢Đây là tất cả các quái bạn đã bắt được🐢:\n"
            common = "<:C_:1118555871958552688> | "
            uncommon = "\n<:U_:1118555223800152065> | "
            rare = "\n<:R_:1118555228481015858> | "
            ultra_rare = "\n<:UR:1118555221862383777> | "
            legendary = "\n <:L_:1118556123067322418> | "
            await open_account(ctx.author.id)
            data = (await get_bank_data())[f"{ctx.author.id}"]["zoo"]
            thuk1 = ["<a:thuK1gif:1115322059841613874>", "<a:thuK1gif:1116033962595328001>","<a:thuK1gif:1116034229587955723>"]
            thuk2 = ["<a:thuK1gif:1116034300576542751>","<a:thuK1gif:1116034392310161462>", "<a:thuK2gif:1116034488837881856>" ]
            thuk3 = ["<a:thuK2gif:1116034548443127894>", "<a:thuK2gif:1116034663568384021>", "<a:thuK2gif:1116034816111034479>"]
            thuk4 = ["<:philong:1115318989137133719>","<a:thuK3gif:1116035130004361357>", "<a:thuK3gif:1116035190075183175>"]
            thuk5 = ["<a:thuK3gif:1116035320601923664>","<a:thuK3gif:1116035401702973462>", "<a:thuK3gif:1116035547614425098>"]
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
            trang_bi = equipment[str(str((await get_bank_data())[str(ctx.author.id)]["equip"]))]
            msg +=f"\nTổng số vàng hiện có: {coin}<:vang:1116221866273681510>\nChỉ số HP: {hp}\nVật phẩm đang sử dụng: {trang_bi}"
            await ctx.send(msg)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Zoo(bot))