# -*- coding: utf-8 -*-
"""assets.py — عقارات · سيارات · بزنس — dev by 7amo"""
from __future__ import annotations
from datetime import datetime,timedelta
import discord
from discord.ui import View,Button
from config import COLOR_GOLD,COLOR_GREEN
from data.shop import HOUSES,CARS,BUSINESSES
from services.economy import clamp,money_fmt,fmt_seconds
from services.cooldowns import ensure_player,check_money,safe_callback
from services.canvas import generate_result_image,generate_business_image
from views.helpers import make_embed

class AssetsView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌",ephemeral=True); return False
        return True
    @discord.ui.button(label="🏠 بيوت",style=discord.ButtonStyle.secondary)
    async def h(self,i,b): await i.response.send_message("🏠:",view=BuyView(self.uid,self.db,"house"),ephemeral=True)
    @discord.ui.button(label="🚗 سيارات",style=discord.ButtonStyle.secondary)
    async def c(self,i,b): await i.response.send_message("🚗:",view=BuyView(self.uid,self.db,"car"),ephemeral=True)
    @discord.ui.button(label="🏪 بزنس",style=discord.ButtonStyle.success)
    async def bz(self,i,b): await i.response.send_message("🏪:",view=BuyView(self.uid,self.db,"business"),ephemeral=True)
    @discord.ui.button(label="💵 تحصيل دخل",style=discord.ButtonStyle.primary)
    async def col(self,i,b):
        rows=await self.db.fetchall("SELECT * FROM assets WHERE user_id=? AND asset_type='business'",(self.uid,))
        if not rows: await i.response.send_message("❌ مفيش بزنس.",ephemeral=True); return
        total=0; det=[]
        now=datetime.now()
        for r in rows:
            last=datetime.fromisoformat(r["last_collect"]) if r["last_collect"] else None
            if last and now<last+timedelta(hours=6):
                det.append(f"⏰ {r['name']}: {fmt_seconds(int(((last+timedelta(hours=6))-now).total_seconds()))}"); continue
            total+=r["income"]; det.append(f"✅ {r['name']}: +{money_fmt(r['income'])}")
            await self.db.execute("UPDATE assets SET last_collect=? WHERE id=?",(now.isoformat(timespec="seconds"),r["id"]))
        p=await self.db.get_player(self.uid)
        if total and p: await self.db.update_player(self.uid,money=p["money"]+total,total_earnings=p["total_earnings"]+total)
        await i.response.send_message(embed=make_embed("💵 البزنس","\n".join(det)+f"\n\n**إجمالي: {money_fmt(total)}**",COLOR_GREEN),ephemeral=True)

class BuyView(View):
    def __init__(self,uid,db,kind):
        super().__init__(timeout=180); self.uid=uid; self.db=db; self.kind=kind
        src={"house":HOUSES,"car":CARS,"business":BUSINESSES}[kind]
        for n,d in list(src.items())[:20]:
            if d["price"]==0: continue
            bt=Button(label=f"{d.get('emoji','')} {n} {money_fmt(d['price'])}",style=discord.ButtonStyle.secondary)
            bt.callback=self._cb(n); self.add_item(bt)
    def _cb(self,name):
        @safe_callback
        async def cb(i):
            if i.user.id!=self.uid: return
            p=await ensure_player(self.db,i);
            if not p: return
            src={"house":HOUSES,"car":CARS,"business":BUSINESSES}[self.kind]; d=src[name]
            if await check_money(self.db,i,p,d["price"]): return
            qm=[]
            if self.kind=="house":
                await self.db.update_player(self.uid,money=p["money"]-d["price"],house=name,happiness=clamp(p["happiness"]+max(0,d["happiness_bonus"]//2)),total_spent=p["total_spent"]+d["price"])
                qm=await self.db.progress_quest(self.uid,"house_1"); t=f"🏠 اشتريت {name}!"
            elif self.kind=="car":
                await self.db.update_player(self.uid,money=p["money"]-d["price"],car=name,happiness=clamp(p["happiness"]+d["happiness"]//2),total_spent=p["total_spent"]+d["price"])
                qm=await self.db.progress_quest(self.uid,"car_1"); t=f"🚗 اشتريت {name}!"
            else:
                await self.db.update_player(self.uid,money=p["money"]-d["price"],total_spent=p["total_spent"]+d["price"])
                sign=d.get("sign","")
                await self.db.execute("INSERT OR IGNORE INTO assets(user_id,asset_type,name,income,sign) VALUES(?,'business',?,?,?)",(self.uid,name,d["income"],sign))
                qm=await self.db.progress_quest(self.uid,"business_1"); t=f"🏪 فتحت {name}!"
                img=await generate_business_image(name,sign,d["income"])
                f=discord.File(img,filename="biz.png")
                e=make_embed(t,f"{d.get('emoji','')} {name}\n📋 لافتة: *{sign}*\n💰 دخل: {money_fmt(d['income'])}/6 ساعات\n{d['desc']}\n"+"\n".join(qm),COLOR_GOLD)
                e.set_image(url="attachment://biz.png")
                from views.main_menu import MainMenuView
                await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db)); return
            lines=[f"{d.get('emoji','')} {name}",f"💰 {money_fmt(d['price'])}",d.get("desc","")]+qm
            img=await generate_result_image(t,lines,"#f1c40f"); f=discord.File(img,filename="a.png")
            e=make_embed(t,"\n".join(lines),COLOR_GOLD); e.set_image(url="attachment://a.png")
            from views.main_menu import MainMenuView
            await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db))
        return cb
