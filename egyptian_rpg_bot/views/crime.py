# -*- coding: utf-8 -*-
"""crime.py — نظام سرقة RPG خيالي — dev by 7amo"""
from __future__ import annotations
import random,discord
from discord.ui import View,Button,Select
from config import COLOR_GREEN,COLOR_RED
from data.quests import STEAL_TARGETS
from services.economy import clamp,money_fmt,add_xp_and_level,fmt_seconds
from services.cooldowns import ensure_player,check_energy,check_jail_guard,safe_callback
from services.canvas import generate_result_image
from views.helpers import make_embed

DIFF_KEYS={"سهل 🟢":"easy","متوسط 🟡":"medium","صعب 🔴":"hard"}

class StealView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌",ephemeral=True); return False
        return True
    @discord.ui.select(placeholder="🔫 مستوى الصعوبة",options=[discord.SelectOption(label=k,value=k) for k in STEAL_TARGETS.keys()])
    async def sel(self,i,s):
        d=s.values[0]
        await i.response.send_message(f"🔫 اختار هدف ({d}):",view=StealTargetsView(self.uid,self.db,d),ephemeral=True)

class StealTargetsView(View):
    def __init__(self,uid,db,diff):
        super().__init__(timeout=180); self.uid=uid; self.db=db; self.diff=diff
        for t,d in STEAL_TARGETS[diff].items():
            bt=Button(label=f"{t} ({d['min_loot']}-{d['max_loot']}ج)",style=discord.ButtonStyle.danger)
            bt.callback=self._cb(t); self.add_item(bt)
    def _cb(self,target):
        @safe_callback
        async def cb(i):
            if i.user.id!=self.uid: return
            p=await ensure_player(self.db,i);
            if not p: return
            if await check_jail_guard(self.db,i): return
            act=f"steal_{DIFF_KEYS.get(self.diff,'easy')}"
            rem=await self.db.cooldown_remaining(self.uid,act)
            if rem: await i.response.send_message(f"⏰ باقي: **{fmt_seconds(rem)}**",ephemeral=True); return
            d=STEAL_TARGETS[self.diff][target]
            if await check_energy(self.db,i,p,d["energy"]): return
            if p["stealth_skill"]<d["req_stealth"]: await i.response.send_message(f"❌ محتاج تخفي **{d['req_stealth']}**.",ephemeral=True); return
            sc=clamp(100-d["risk"]+p["stealth_skill"]//2+p["fighting_skill"]//5,5,95)
            ok=random.randint(1,100)<=sc; ne=clamp(p["energy"]-d["energy"])
            cd_h={"سهل 🟢":2,"متوسط 🟡":3,"صعب 🔴":4}.get(self.diff,3)
            await self.db.set_cooldown(self.uid,act,hours=cd_h)
            if ok:
                loot=random.randint(d["min_loot"],d["max_loot"])
                await self.db.update_player(self.uid,money=p["money"]+loot,energy=ne,stealth_skill=clamp(p["stealth_skill"]+2),reputation=p["reputation"]+5,total_earnings=p["total_earnings"]+loot)
                ms=await add_xp_and_level(self.db,self.uid,d["xp"]); ms.extend(await self.db.progress_quest(self.uid,"steal_1"))
                if "بنك" in target or "خزنة" in target: ms.extend(await self.db.progress_quest(self.uid,"bank_rob_1"))
                lines=[f"🎯 {target}",f"📊 {self.diff} | نجاح {sc}%",f"💰 الغنيمة: {money_fmt(loot)}","🥷 تخفي +2"]+ms
                img=await generate_result_image("✅ سرقة ناجحة!",lines,"#2ecc71"); co=COLOR_GREEN
            else:
                fine=d["max_loot"]//3
                from datetime import datetime,timedelta
                jt=d["risk"]//8; ju=(datetime.now()+timedelta(minutes=jt)).isoformat(timespec="seconds") if jt>5 else None
                u={"money":max(0,p["money"]-fine),"energy":ne,"health":clamp(p["health"]-15),"wanted_level":clamp(p["wanted_level"]+1,0,10),"happiness":clamp(p["happiness"]-10)}
                if ju: u["jail_until"]=ju
                await self.db.update_player(self.uid,**u)
                lines=[f"🎯 {target}",f"نجاح {sc}%","🚨 اتمسكت!",f"💸 غرامة: {money_fmt(fine)}","🚔 مطلوبية +1"]
                if ju: lines.append(f"🔒 سجن {jt} دقيقة")
                img=await generate_result_image("❌ فشلت!",lines,"#e74c3c"); co=COLOR_RED
            f=discord.File(img,filename="st.png"); e=make_embed("🔫 النتيجة","\n".join(lines),co); e.set_image(url="attachment://st.png")
            from views.main_menu import MainMenuView
            await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db))
        return cb
