import discord
from discord.ext import commands
from main import get_bank_data, save_member_data, open_account
import io
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import os
import time
import random
from command.cache.var import character, list_color

class Pvp(commands.Cog):
    config = {
        "name": "pvp",
        "desc": "pvp voi nguoi khac",
        "use": "pvp <@tag>",
        "author": 'Anh Duc'
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def pvp(self, ctx, mention: discord.Member = None):
        try:
            if mention == None:
                return await ctx.send("ban chua tag nguoi ban muon pvp cung")
            em = discord.Embed(title= f"**{ctx.author.name} Đã gửi lời đề nghị thách đấu tới {mention.name}, bạn có đồng ý hay không?**", color = random.choice(list_color))
            send = await ctx.send(embed=em)
            await send.add_reaction("❎")
            await send.add_reaction("✅")
            
            def check(reaction, mem):
                if mem.id == mention.id and str(reaction.emoji) == '✅':
                    return True
                elif mem.id != mention.id or str(reaction.emoji) == "✅":
                    return False
            react = await self.bot.wait_for("reaction_add", check = check)
            if not react:
                return await ctx.send(f"**{mention.name} Đã từ chối lời đề nghị của bạn**")
            def drawProgressBar(d, x, y, w, h, progress, bg="white", fg="red"):
                if progress== 0:
                    d.rectangle((x+w, y, x+h+w, y+h), fill=bg)
                    d.rectangle((x, y, x+h, y+h), fill=bg)
                    d.rectangle((x+(h/2), y, x+w+(h/2), y+h), fill=bg)
                
                    # draw progress bar
                    w *= progress
                    d.rectangle((x+w, y, x+h+w, y+h),fill=bg)
                    d.rectangle((x, y, x+h, y+h),fill=bg)
                    d.rectangle((x+(h/2), y, x+w+(h/2), y+h),fill=bg)
                    return d
                #if progress > 0
                d.rectangle((x+w, y, x+h+w, y+h), fill=bg)
                d.rectangle((x, y, x+h, y+h), fill=bg)
                d.rectangle((x+(h/2), y, x+w+(h/2), y+h), fill=bg)
            
                # draw progress bar
                w *= progress
                d.rectangle((x+w, y, x+h+w, y+h),fill=fg)
                d.rectangle((x, y, x+h, y+h),fill=fg)
                d.rectangle((x+(h/2), y, x+w+(h/2), y+h),fill=fg)
            
                return d
            def bytesarr(image: Image) -> bytes:
                imgByteArr = io.BytesIO()
                image.save(imgByteArr, format=image.format)
                imgByteArr = imgByteArr.getvalue()
                return io.BytesIO(imgByteArr)
            
            await open_account(ctx.author.id)
            await open_account(mention.id)
            tag_hp = 100
            user_hp = 100
            data = await get_bank_data()
            turn = random.choice(["tag","user"])
            cha_user = data[str(ctx.author.id)]["character"]
            cha_tag = data[str(mention.id)]["character"]
            cha_user_path = character[data[str(ctx.author.id)]["character"]]["path"]
            cha_tag_path = character[data[str(mention.id)]["character"]]["path"]
            def run():
                out = Image.open(os.path.dirname(__file__) + "/cache/khung2.png")
                #tag
                cha_user_paste = Image.open(cha_user_path)
                cha_tag_paste = Image.open(cha_tag_path)
                Image.Image.paste(out, cha_tag_paste, (25, 40))
                d1 = ImageDraw.Draw(out)
                tag = drawProgressBar(d1, 30, 10, 69, 8, tag_hp/100)
                d1.text((30, 1), f"{cha_tag}", fill=(255, 255, 255))
                #user
                Image.Image.paste(out, cha_user_paste, (165,40))
                user = drawProgressBar(d1, 140, 10, 69,8,user_hp/100)
                d1.text((140, 1), f"{cha_user}", fill=(255, 255, 255))
                file = discord.File(fp=bytesarr(out), filename="pvp.png")
                return file
            file = run()
            if turn == "tag":
                first_hit = f"<@{mention.id}>"
            else:
                first_hit = f"<@{ctx.author.id}>"
            msg = await ctx.send(f"Ván đấu sẽ bắt đầu sau 5s,{first_hit} được ra đòn trước", file=file)
            time.sleep(5)
            while True:
                tag_at = data[str(mention.id)]["attack"]
                user_at = data[str(ctx.author.id)]["attack"]
                content =  f"**{ctx.author.name}:**\nattack: {user_at}\n**{mention.name}:**\nattack: {tag_at}"
                crit_chance = random.choice(["Y"]*15+["N"]*80+["0"]*5)
                
                if crit_chance == "Y":
                    if turn == "tag":
                        tag_at += 5
                        content += f"\n**{mention.name} đã thực hiện một đòn đánh chí mạng gây ra {tag_at} sát thương**"
                    elif turn == "user":
                        user_at += 5
                        content += f"\n**{ctx.author.name} đã thực hiện một đòn đánh chí mạng gây ra {user_at} sát thương**"
                elif crit_chance == "0":
                    if turn == "tag":
                        tag_at = 0
                        content += f"\n**{mention.name}** đã đánh trượt nên không gây ra sát thương"
                    else:
                        user_at = 0
                        content += f"\n**{ctx.author.name}** đã đánh trượt nên không gây ra sát thương"
                else:
                    pass
                if turn == "tag":
                    user_hp -= tag_at
                    turn = "user"
                else:
                    tag_hp -= user_at
                    turn = "tag"
                    
                
                file = run()
                
                await msg.edit(content =content,attachments=[file])
                time.sleep(2.5)
                if user_hp == 0:
                    await ctx.send(f"<@{mention.id}> won!")
                    break
                elif tag_hp == 0:
                    await ctx.send(f"<@{ctx.author.id}> won!")
                    break
                #user
                elif user_hp < 0:
                    user_hp = 0
                    file = run()
                    await msg.edit(content =content,attachments=[file])
                    await ctx.send(f"<@{mention.id}> won!")
                    break
                #tag
                elif tag_hp < 0:
                    tag_hp = 0
                    file = run()
                    await msg.edit(content =content,attachments=[file])
                    await ctx.send(f"<@{ctx.author.id}> won!")
                    break
        except Exception as e:
            print(e)
            await ctx.send(f"error: {e}")
async def setup(bot):
    await bot.add_cog(Pvp(bot))