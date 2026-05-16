# -*- coding: utf-8 -*-
"""freelance.py — شغل حر + كورسات — dev by 7amo"""
from __future__ import annotations
import random,discord
from discord.ui import View,Button,Select
from config import COLOR_GREEN,COLOR_RED,COLOR_BLUE,COLOR_PURPLE
from data.quests import PROGRAMMING_PROJECTS,DESIGN_PROJECTS,HACKING_TARGETS,COURSES
from data.jobs import CUSTOMERS_ALL
from services.economy import clamp,money_fmt,add_xp_and_level,fmt_seconds
from services.cooldowns import ensure_player,check_money,check_jail_guard,safe_callback
from services.canvas import generate_result_image
from views.helpers import make_embed

class FreelanceView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌",ephemeral=True); return False
        return True
    @discord.ui.button(label="💻 برمجة",style=discord.ButtonStyle.primary,row=0)
    async def prog(self,i,b): await i.response.send_message("💻 صعوبة:",view=DiffView(self.uid,self.db,"program"),ephemeral=True)
    @discord.ui.button(label="🎨 تصميم",style=discord.ButtonStyle.success,row=0)
    async def des(self,i,b): await i.response.send_message("🎨 صعوبة:",view=DiffView(self.uid,self.db,"design"),ephemeral=True)
    @discord.ui.button(label="🛡️ أمن",style=discord.ButtonStyle.secondary,row=0)
    async def hack(self,i,b): await i.response.send_message("🛡️ صعوبة:",view=DiffView(self.uid,self.db,"hack"),ephemeral=True)
    @discord.ui.button(label="📚 كورسات",style=discord.ButtonStyle.secondary,row=1)
    async def courses(self,i,b): await i.response.send_message("📚 كورسات:",view=CoursesView(self.uid,self.db),ephemeral=True)

class DiffView(View):
    def __init__(self,uid,db,kind): super().__init__(timeout=180); self.uid=uid; self.db=db; self.kind=kind
    @discord.ui.select(placeholder="📊 الصعوبة",options=[discord.SelectOption(label=x,value=x) for x in ["سهل","متوسط","صعب"]])
    async def sel(self,i,s):
        if i.user.id!=self.uid: return
        await i.response.send_message("اختار:",view=ProjView(self.uid,self.db,self.kind,s.values[0]),ephemeral=True)

class ProjView(View):
    def __init__(self,uid,db,kind,diff):
        super().__init__(timeout=180); self.uid=uid; self.db=db; self.kind=kind; self.diff=diff
        src={"program":PROGRAMMING_PROJECTS,"design":DESIGN_PROJECTS,"hack":HACKING_TARGETS}[kind]
        for n,d in src[diff].items():
            bt=Button(label=f"{n} ({money_fmt(d.get('earnings',0))})",style=discord.ButtonStyle.primary)
            bt.callback=self._cb(n); self.add_item(bt)
    def _cb(self,pn):
        @safe_callback
        async def cb(i):
            if i.user.id!=self.uid: return
            p=await ensure_player(self.db,i);
            if not p: return
            if await check_jail_guard(self.db,i): return
            src={"program":PROGRAMMING_PROJECTS,"design":DESIGN_PROJECTS,"hack":HACKING_TARGETS}[self.kind]
            d=src[self.diff][pn]; sf={"program":"programming_skill","design":"design_skill","hack":"hacking_skill"}[self.kind]; act=f"{self.kind}_proj"
            rem=await self.db.cooldown_remaining(self.uid,act)
            if rem: await i.response.send_message(f"⏰ باقي: **{fmt_seconds(rem)}**",ephemeral=True); return
            if p[sf]<d["req_skill"]: await i.response.send_message(f"❌ محتاج {d['req_skill']}.",ephemeral=True); return
            cost=d.get("complexity",d.get("quality",4))*5
            if p["energy"]<cost: await i.response.send_message("❌ طاقة مش كفاية.",ephemeral=True); return
            bc=70-(d.get("risk",0)//4 if self.kind=="hack" else 0)
            sc=clamp(bc+p[sf]//3,8,96); ok=random.randint(1,100)<=sc
            await self.db.set_cooldown(self.uid,act,hours=d["time"]); cl=random.choice(CUSTOMERS_ALL)
            if ok:
                earn=int(d["earnings"]+random.randint(-d["earnings"]//10,d["earnings"]//5)); gn=d.get("complexity",d.get("quality",3))
                await self.db.update_player(self.uid,money=p["money"]+earn,energy=clamp(p["energy"]-cost),total_earnings=p["total_earnings"]+earn,**{sf:clamp(p[sf]+gn)})
                ms=await add_xp_and_level(self.db,self.uid,d["xp"])
                if self.kind=="program": ms.extend(await self.db.progress_quest(self.uid,"program_1"))
                elif self.kind=="design": ms.extend(await self.db.progress_quest(self.uid,"design_1"))
                kn={"program":"💻 برمجة","design":"🎨 تصميم","hack":"🛡️ أمن"}[self.kind]
                lines=[f"{kn}: {pn}",f"👤 العميل: {cl}",f"💰 {money_fmt(earn)}",f"📈 +{gn} مهارة",f"⭐ +{d['xp']} XP"]+ms; co,ac=COLOR_GREEN,"#2ecc71"
            else:
                await self.db.update_player(self.uid,energy=clamp(p["energy"]-max(5,cost//2)))
                lines=[f"المشروع: {pn}",f"👤 {cl}","❌ فشل!","💡 طوّر مهاراتك."]; co,ac=COLOR_RED,"#e74c3c"
            img=await generate_result_image("💼 نتيجة",lines,ac); f=discord.File(img,filename="fl.png")
            e=make_embed("نتيجة المشروع","\n".join(lines),co); e.set_image(url="attachment://fl.png")
            from views.main_menu import MainMenuView
            await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db))
        return cb

class CoursesView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    @discord.ui.select(placeholder="📚 كورس",options=[discord.SelectOption(label=n,value=n,description=f"{d['price']}ج | +{d['gain']}") for n,d in COURSES.items()])
    async def sel(self,i,s):
        if i.user.id!=self.uid: return
        p=await ensure_player(self.db,i);
        if not p: return
        c=s.values[0]; d=COURSES[c]
        rem=await self.db.cooldown_remaining(self.uid,"course")
        if rem: await i.response.send_message(f"⏰ باقي: **{fmt_seconds(rem)}**",ephemeral=True); return
        if await check_money(self.db,i,p,d["price"]): return
        sk=d["skill"]
        await self.db.update_player(self.uid,money=p["money"]-d["price"],**{sk:clamp(p.get(sk,0)+d["gain"])})
        await self.db.set_cooldown(self.uid,"course",hours=d["hours"])
        ms=await add_xp_and_level(self.db,self.uid,d["xp"]); ms.extend(await self.db.progress_quest(self.uid,"course_3"))
        lines=[f"📚 {c}",f"💰 {money_fmt(d['price'])}",f"📈 +{d['gain']}",f"⭐ +{d['xp']}"]+ms
        img=await generate_result_image("📚 كورس!",lines,"#9b59b6"); f=discord.File(img,filename="co.png")
        e=make_embed("📚 خلصت كورس!","\n".join(lines),COLOR_PURPLE); e.set_image(url="attachment://co.png")
        from views.main_menu import MainMenuView
        await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db))
