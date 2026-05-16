# -*- coding: utf-8 -*-
"""jobs.py — الشغل والترقيات — dev by 7amo"""
from __future__ import annotations
import random,discord
from discord.ui import View,Button,Select
from config import COLOR_GREEN,COLOR_RED,COLOR_BLUE
from data.jobs import JOBS,WORK_EVENTS
from data.classes import AGE_GROUPS
from services.economy import clamp,money_fmt,add_xp_and_level,maybe_random_event,fmt_seconds
from services.cooldowns import ensure_player,check_cooldown,check_energy,check_jail_guard,safe_callback
from services.canvas import generate_result_image
from views.helpers import make_embed

class JobsView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌",ephemeral=True); return False
        return True
    @discord.ui.select(placeholder="💼 اختار وظيفة",options=[discord.SelectOption(label=f"{d.get('emoji','')} {n}",value=n,description=f"راتب {d['salary']}ج | لفل {d['req_level']}") for n,d in list(JOBS.items())[:25]],row=0)
    async def sel(self,i,s):
        p=await ensure_player(self.db,i);
        if not p: return
        j=s.values[0]; d=JOBS[j]
        if p["level"]<d["req_level"]: await i.response.send_message(f"❌ محتاج لفل **{d['req_level']}**.",ephemeral=True); return
        await self.db.update_player(self.uid,job=j,job_xp=0,job_rank="")
        rnks=" → ".join([r["name"] for r in d.get("ranks",[])]) if d.get("ranks") else ""
        from views.main_menu import MainMenuView
        await i.response.send_message(embed=make_embed("✅ تم التعيين!",f"{d.get('emoji','')} بقيت **{j}**\n💰 الراتب: {money_fmt(d['salary'])}\n📝 {d['desc']}\n{'📈 '+rnks if rnks else ''}",COLOR_GREEN),view=MainMenuView(self.uid,self.db))
    @discord.ui.button(label="💼 اشتغل دلوقتي!",style=discord.ButtonStyle.success,row=1,emoji="⚡")
    async def work(self,i,b):
        p=await ensure_player(self.db,i);
        if not p: return
        if p["job"]=="عاطل": await i.response.send_message("❌ أنت عاطل! اختار وظيفة.",ephemeral=True); return
        if await check_jail_guard(self.db,i): return
        if await check_cooldown(self.db,i,"work","لسه بدري"): return
        d=JOBS[p["job"]]
        if await check_energy(self.db,i,p,d["energy_cost"]): return
        am=AGE_GROUPS[p["age_group"]].get("work_multiplier",1.0); rb=0; cr=""; jxg=random.randint(25,60)
        if d.get("ranks"):
            njx=p["job_xp"]+jxg
            for rk in reversed(d["ranks"]):
                if njx>=rk["job_xp"]: rb=rk["salary_bonus"]; cr=rk["name"]; break
        sal=int(max(0,(d["salary"]+random.randint(-20,60)+rb)*am))
        # work event
        wem=""; xm=0; mm=0
        for ev in WORK_EVENTS:
            if random.random()<ev["chance"]: wem=f"\n🎲 {ev['msg']}"; xm=ev.get("xp_bonus",0); mm=ev.get("money_bonus",0); break
        ups={"money":p["money"]+sal+mm,"energy":clamp(p["energy"]-d["energy_cost"]),"hunger":clamp(p["hunger"]-random.randint(8,14)),"thirst":clamp(p["thirst"]-random.randint(10,16)),"job_xp":p["job_xp"]+jxg,"total_earnings":p["total_earnings"]+sal}
        if cr: ups["job_rank"]=cr
        await self.db.update_player(self.uid,**ups); await self.db.set_cooldown(self.uid,"work",hours=3)
        msgs=await add_xp_and_level(self.db,self.uid,55+xm)
        for q in ["work_1","work_10","work_50"]: msgs.extend(await self.db.progress_quest(self.uid,q))
        msgs.extend(await self.db.progress_quest(self.uid,"rich_100k",ups["money"]+p["bank"],absolute=True))
        ev=await maybe_random_event(self.db,i.user)
        if ev: msgs.append(ev)
        lines=[f"{d.get('emoji','')} اشتغلت كـ {p['job']}",f"{'📊 '+cr if cr else ''}",f"💰 قبضت: {money_fmt(sal)}{f' (+{mm})' if mm else ''}",f"⚡ طاقة: -{d['energy_cost']}",f"⭐ +{55+xm} XP"]+[l for l in lines if l]+msgs
        lines=[l for l in lines if l]
        if wem: lines.append(wem)
        img=await generate_result_image("💼 يوم شغل",lines[:10],"#2ecc71"); f=discord.File(img,filename="w.png")
        e=make_embed("💼 خلصت شغل!","\n".join(lines),COLOR_GREEN); e.set_image(url="attachment://w.png")
        from views.main_menu import MainMenuView
        await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db))
    @discord.ui.button(label="📊 مسار الترقية",style=discord.ButtonStyle.secondary,row=1)
    async def career(self,i,b):
        p=await ensure_player(self.db,i);
        if not p: return
        d=JOBS.get(p["job"],{}); rnks=d.get("ranks",[])
        if not rnks: await i.response.send_message("❌ مفيش ترقيات.",ephemeral=True); return
        desc=f"**{d.get('emoji','')} {p['job']}** — Job XP: **{p['job_xp']:,}**\n\n"
        for r in rnks:
            c="◀️ " if p["job_rank"]==r["name"] else ""; s="✅" if p["job_xp"]>=r["job_xp"] else "🔒"
            desc+=f"{s} {c}**{r['name']}** — XP: {r['job_xp']:,} | +{money_fmt(r['salary_bonus'])}\n"
        await i.response.send_message(embed=make_embed("📊 الترقيات",desc,COLOR_BLUE),ephemeral=True)
