import discord
from discord.ext import commands
from main import get_bank_data, save_member_data, open_account
import io
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import os
import time
import random
from command.cache.var import character, list_color, weapon

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
            
            #function
            
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
            
            #edit image
            def run():
                out = Image.open(os.path.dirname(__file__) + "/cache/khung2.png")
                #tag
                cha_user_paste = Image.open(cha_user_path)
                cha_tag_paste = Image.open(cha_tag_path)
                Image.Image.paste(out, cha_tag_paste, (25, 38))
                d1 = ImageDraw.Draw(out)
                tag = drawProgressBar(d1, 30, 10, 69, 8, tag_hp/100)
                d1.text((30, 1), f"{cha_tag}", fill=(255, 255, 255))
                #user
                Image.Image.paste(out, cha_user_paste, (165,38))
                drawProgressBar(d1, 140, 10, 69,8,user_hp/100)
                d1.text((140, 1), f"{cha_user}", fill=(255, 255, 255))
                file = discord.File(fp=bytesarr(out), filename="pvp.png")
                return file
                
            #first hit
            user = data[str(ctx.author.id)]
            tag = data[str(mention.id)]
            
            user_at_def = user["attack"]
            tag_at_def = tag["attack"]
            
            if turn == "tag":
                first_hit = f"<@{mention.id}>"
            else:
                first_hit = f"<@{ctx.author.id}>"
                
            damage_chance = random.choice(["Y"]*20+["N"]*80)
            msg = f"Ván đấu sẽ bắt đầu sau 5s,{first_hit} được ra đòn trước"
            
            #check skill, equip pvp
            #user
            if user["skill"] == 8:
                user_at_def += 3
            if user["skill"] == 9:
                tag_at_def -= 3
             
            #tag
            if tag["skill"] == 8:
                tag_at_def += 3
            if tag["skill"] == 9:
                user_at_def -= 3
            
            if user["pvp_equip"] == 5 and damage_chance == "Y":
                user_at_def = user_at_def*1.1
                msg += f"\n{ctx.author.name} Đã được tăng thêm 10% sát thương cho mỗi đòn đánh nhờ trang bị"
            if tag["pvp_equip"] == 5 and damage_chance == "Y":
                tag_at_def = tag_at_def *1.1
                msg += f"\n{mention.name} Đã được tăng thêm 10% sát thương cho mỗi đòn đánh nhờ trang bị"
            file = run()
            
            msg = await ctx.send(msg, file=file)
            equip_pvp_user = weapon["0" + str(user["pvp_equip"])]["icon"]
            equip_pvp_tag = weapon["0" + str(tag["pvp_equip"])]["icon"]
            user_skill = weapon["0" + str(user["skill"])]["icon"]
            tag_skill = weapon["0" + str(tag["skill"])]["icon"]
            draw_turn = 0
            time.sleep(5)
            while True:
                tag_at = tag_at_def
                user_at = user_at_def
                
                content =  f"**{ctx.author.name}:**\n<:attack:1119538348051152916>: {user_at}\nTrang bị pvp: {equip_pvp_user}\nskill: {user_skill}\n**{mention.name}:**\n<:attack:1119538348051152916>: {tag_at}\nTrang bị pvp: {equip_pvp_tag}\nskill: {tag_skill}"
                
                #chance
                #crit
                if user["pvp_equip"] == 7 or tag["pvp_equip"]:
                    crit_chance = random.choice(["Y"]*18+["N"]*77+["0"]*5)
                    
                else:
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
                        
               #attack
                else:
                    pass
                if turn == "tag":
                    if tag["pvp_equip"] == 6:
                        hp_chance = random.choice(["Y"]*16+["N"]*84)
                        if hp_chance == "Y" and tag_hp <=90:
                            tag_hp += 10
                            content += f"\n{mention.name} Đã được cộng thêm 10HP nhò trang bị"
                    chance = random.choice(["Y"]*10 + ["N"]*90)
                    if user["skill"] == 10 and chance == "Y":
                        content += f"\n**{ctx.author.name} Đã sử dụng skill nên được miễn thương đòn đánh**"
                        tag_at = 0
                    user_hp -= tag_at
                    turn = "user"
                else:
                    if user["pvp_equip"] == 6:
                        hp_chance = random.choice(["Y"]*16+["N"]*84)
                        if hp_chance == "Y" and user_hp <=90:
                            user_hp += 10
                            content += f"\n{ctx.author.name} Đã được cộng thêm 10HP nhò trang bị"
                    chance = random.choice(["Y"]*10 + ["N"]*90)
                    if tag["skill"] == 10 and chance == "Y":
                        content += f"\n**{mention.name} Đã sử dụng skill nên được miễn thương đòn đánh**"
                        user_at = 0
                    tag_hp -= user_at
                    turn = "tag"
                if user_hp <= 0:
                    user_hp = 0
                elif tag_hp <= 0:
                    tag_hp = 0
                draw_turn += 1
                if draw_turn == 2:
                    draw_turn = 0
                    file = run()
                    
                    await msg.edit(content =content,attachments=[file])
                    time.sleep(3)
                    if user_hp == 0:
                        await ctx.send(f"<@{mention.id}> đã thắng trận đấu pvp")
                        break
                    elif tag_hp == 0:
                        await ctx.send(f"<@{ctx.author.id}> đã thắng trận đấu pvp")
                        break
                        
                    #user
                    elif user_hp < 0:
                        user_hp = 0
                        file = run()
                        await msg.edit(content =content,attachments=[file])
                        await ctx.send(f"<@{mention.id}> đã thắng trận đấu pvp")
                        break
                        
                    #tag
                    elif tag_hp < 0:
                        tag_hp = 0
                        file = run()
                        await msg.edit(content =content,attachments=[file])
                        await ctx.send(f"<@{ctx.author.id}> đã thắng trận đấu pvp")
                        break
        except Exception as e:
            print(e)
            await ctx.send(f"error: {e}")
async def setup(bot):
    await bot.add_cog(Pvp(bot))