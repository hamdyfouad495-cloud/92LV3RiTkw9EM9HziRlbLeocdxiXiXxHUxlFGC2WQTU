# -*- coding: utf-8 -*-
"""sports.py — كورة · جيم · ستريم — dev by 7amo"""
from __future__ import annotations
import random,discord
from discord.ui import View,Button
from config import COLOR_GREEN,COLOR_RED
from services.economy import clamp,money_fmt,add_xp_and_level,fmt_seconds
from services.cooldowns import ensure_player,check_energy,check_cooldown,safe_callback
from services.canvas import generate_result_image
from views.helpers import make_embed

class SportsView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌",ephemeral=True); return False
        return True
    @discord.ui.button(label="⚽ ماتش كورة",style=discord.ButtonStyle.success,row=0)
    async def fb(self,i,b):
        p=await ensure_player(self.db,i);
        if not p: return
        if await check_cooldown(self.db,i,"football","بدري"): return
        if await check_energy(self.db,i,p,25): return
        sk=p.get("football_skill",0); wc=clamp(40+sk,15,85); won=random.randint(1,100)<=wc
        gf=random.randint(0,3+sk//20); ga=random.randint(0,3)
        if won and gf<=ga: gf=ga+1
        opp=random.choice(["الأهلي","الزمالك","الإسماعيلي","بيراميدز","فريق الحارة","المقاولون"])
        await self.db.set_cooldown(self.uid,"football",hours=3)
        if won:
            pr=random.randint(200,800+sk*10)
            await self.db.update_player(self.uid,energy=clamp(p["energy"]-25),happiness=clamp(p["happiness"]+15),money=p["money"]+pr,football_skill=clamp(p.get("football_skill",0)+2),reputation=p["reputation"]+3,fitness=clamp(p.get("fitness",30)+2))
            ms=await add_xp_and_level(self.db,self.uid,80); ms.extend(await self.db.progress_quest(self.uid,"football_1"))
            lines=[f"⚽ ضد: {opp}",f"📊 {gf}-{ga} كسبت! 🎉",f"💰 {money_fmt(pr)}","⚽ +2 | 🔥 +3"]+ms; co=COLOR_GREEN
        else:
            await self.db.update_player(self.uid,energy=clamp(p["energy"]-25),happiness=clamp(p["happiness"]-5),football_skill=clamp(p.get("football_skill",0)+1),fitness=clamp(p.get("fitness",30)+1))
            ms=await add_xp_and_level(self.db,self.uid,30)
            lines=[f"⚽ ضد: {opp}",f"📊 {gf}-{ga} خسرت 😢","⚽ +1"]+ms; co=COLOR_RED
        img=await generate_result_image("⚽ الماتش",lines,"#2ecc71" if won else "#e74c3c"); f=discord.File(img,filename="fb.png")
        e=make_embed("⚽ ماتش","\n".join(lines),co); e.set_image(url="attachment://fb.png")
        from views.main_menu import MainMenuView
        await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db))
    @discord.ui.button(label="💪 جيم",style=discord.ButtonStyle.primary,row=0)
    async def gym(self,i,b):
        p=await ensure_player(self.db,i);
        if not p: return
        if await check_cooldown(self.db,i,"gym","عضلاتك تعبانة"): return
        if await check_energy(self.db,i,p,20): return
        await self.db.update_player(self.uid,energy=clamp(p["energy"]-20),health=clamp(p["health"]+8),happiness=clamp(p["happiness"]+5),fighting_skill=clamp(p["fighting_skill"]+1),fitness=clamp(p.get("fitness",30)+3),hunger=clamp(p["hunger"]-12))
        await self.db.set_cooldown(self.uid,"gym",hours=4)
        await i.response.send_message(embed=make_embed("💪 جيم","اتمرنت! ❤️+8 💪+1 🏋️+3\n\n💡 *NO PAIN NO GAIN*",COLOR_GREEN),ephemeral=True)
    @discord.ui.button(label="🎥 لايف ستريم",style=discord.ButtonStyle.secondary,row=1)
    async def stream(self,i,b):
        p=await ensure_player(self.db,i);
        if not p: return
        if await check_cooldown(self.db,i,"stream","لسه عملت لايف"): return
        if await check_energy(self.db,i,p,15): return
        sk=p.get("streaming_skill",0); viewers=random.randint(10+sk*5,100+sk*20); don=random.randint(0,viewers*3)
        topics=["فيفا لايف","unboxing","طبخ لايف","GTA مصري","لعب مع المتابعين","حكايات مصرية"]
        await self.db.update_player(self.uid,energy=clamp(p["energy"]-15),money=p["money"]+don,streaming_skill=clamp(sk+2),charisma=clamp(p.get("charisma",5)+1),reputation=p["reputation"]+viewers//40,total_earnings=p["total_earnings"]+don)
        await self.db.set_cooldown(self.uid,"stream",hours=4)
        ms=await add_xp_and_level(self.db,self.uid,50); ms.extend(await self.db.progress_quest(self.uid,"stream_1"))
        lines=[f"🎥 {random.choice(topics)}",f"👥 مشاهدين: {viewers:,}",f"💰 دونيشنز: {money_fmt(don)}","🎥 +2 | 😎 +1"]+ms
        img=await generate_result_image("🎥 لايف",lines,"#9b59b6"); f=discord.File(img,filename="str.png")
        e=make_embed("🎥 خلصت لايف!","\n".join(lines),0x9B59B6); e.set_image(url="attachment://str.png")
        from views.main_menu import MainMenuView
        await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db))
