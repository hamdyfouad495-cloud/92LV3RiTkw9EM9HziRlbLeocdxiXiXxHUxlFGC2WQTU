# -*- coding: utf-8 -*-
"""shop.py — المتجر — dev by 7amo"""
from __future__ import annotations
from typing import Any
import discord
from discord.ui import View,Button,Select
from config import COLOR_GREEN,COLOR_BLUE,COLOR_PURPLE,STAT_FIELDS,SKILL_FIELDS
from data.shop import MARKET_CATEGORIES,FOODS,DRINKS,HYGIENE_ITEMS,BOOKS
from services.economy import clamp,money_fmt,add_xp_and_level
from services.cooldowns import ensure_player,check_money,safe_callback
from services.canvas import generate_result_image
from views.helpers import make_embed

class MarketView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌",ephemeral=True); return False
        return True
    @discord.ui.select(placeholder="🛒 اختار قسم",options=[discord.SelectOption(label=k,value=k) for k in MARKET_CATEGORIES.keys()])
    async def sel(self,i,s):
        cat=s.values[0]; items=MARKET_CATEGORIES[cat]
        d="\n".join([f"• {da.get('emoji','')} **{n}** — {money_fmt(da['price'])} | {da.get('desc','')}" for n,da in items.items()])
        await i.response.send_message(embed=make_embed(f"🛒 {cat}",d[:3900],COLOR_BLUE),view=ItemsBuyView(self.uid,self.db,cat,items),ephemeral=True)

class ItemsBuyView(View):
    def __init__(self,uid,db,cat,items):
        super().__init__(timeout=180); self.uid=uid; self.db=db; self.cat=cat; self.items=items
        for idx,(n,d) in enumerate(list(items.items())[:20]):
            bt=Button(label=f"{n} {d['price']}ج",style=discord.ButtonStyle.secondary,row=idx//5)
            bt.callback=self._cb(n); self.add_item(bt)
    def _cb(self,name):
        @safe_callback
        async def cb(i):
            if i.user.id!=self.uid: await i.response.send_message("❌",ephemeral=True); return
            p=await ensure_player(self.db,i);
            if not p: return
            d=self.items[name]
            if await check_money(self.db,i,p,d["price"]): return
            u={"money":p["money"]-d["price"],"total_spent":p["total_spent"]+d["price"]}
            for k in list(STAT_FIELDS)+list(SKILL_FIELDS)+["reputation","charisma"]:
                if k in d and k not in u:
                    if k in STAT_FIELDS: u[k]=clamp(p[k]+d[k])
                    else: u[k]=clamp(p.get(k,0)+d[k])
            await self.db.update_player(self.uid,**u)
            if any(x in self.cat for x in ["لبس","أدوات","أسلحة"]): await self.db.add_item(self.uid,name,1,self.cat.split()[-1])
            if "أكل" in self.cat or "مشروب" in self.cat: await self.db.progress_quest(self.uid,"eat_20")
            ms=[]; xp=d.get("xp",0)
            if xp: ms=await add_xp_and_level(self.db,self.uid,xp)
            lines=[f"{d.get('emoji','')} اشتريت: {name}",f"💰 {money_fmt(d['price'])}",f"💵 المتبقي: {money_fmt(u['money'])}"]+ms
            img=await generate_result_image("🛒 شراء ناجح",lines,"#3498db"); f=discord.File(img,filename="b.png")
            e=make_embed("✅ تم!","\n".join(lines),COLOR_GREEN); e.set_image(url="attachment://b.png")
            from views.main_menu import MainMenuView
            await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db))
        return cb

class QuickFoodView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌",ephemeral=True); return False
        return True
    @discord.ui.select(placeholder="🍗 أكل",options=[discord.SelectOption(label=f"{d.get('emoji','')} {n} — {d['price']}ج",value=n,description=f"جوع +{d['hunger']}") for n,d in list(FOODS.items())[:25]],row=0)
    async def food(self,i,s): await self._buy(i,s.values[0],FOODS)
    @discord.ui.select(placeholder="🥤 مشروب",options=[discord.SelectOption(label=f"{d.get('emoji','')} {n} — {d['price']}ج",value=n,description=f"عطش +{d['thirst']}") for n,d in list(DRINKS.items())[:25]],row=1)
    async def drink(self,i,s): await self._buy(i,s.values[0],DRINKS)
    async def _buy(self,i,name,src):
        p=await ensure_player(self.db,i);
        if not p: return
        d=src[name]
        if await check_money(self.db,i,p,d["price"]): return
        u={"money":p["money"]-d["price"]}
        for k in STAT_FIELDS:
            if k in d: u[k]=clamp(p[k]+d[k])
        await self.db.update_player(self.uid,**u); await self.db.progress_quest(self.uid,"eat_20")
        await i.response.send_message(embed=make_embed(f"{d.get('emoji','')} {name}",f"**{name}**\n{d['desc']}\n💰 {money_fmt(d['price'])}",COLOR_GREEN),ephemeral=True)

class HygieneView(View):
    def __init__(self,uid,db):
        super().__init__(timeout=180); self.uid=uid; self.db=db
        for n,d in HYGIENE_ITEMS.items():
            bt=Button(label=f"{d.get('emoji','')} {n} {d['price']}ج",style=discord.ButtonStyle.secondary)
            bt.callback=self._cb(n); self.add_item(bt)
    def _cb(self,name):
        @safe_callback
        async def cb(i):
            if i.user.id!=self.uid: return
            p=await ensure_player(self.db,i);
            if not p: return
            d=HYGIENE_ITEMS[name]
            if await check_money(self.db,i,p,d["price"]): return
            u={"money":p["money"]-d["price"]}
            for k in STAT_FIELDS|SKILL_FIELDS|{"charisma"}:
                if k in d: u[k]=clamp(p.get(k,0)+d[k])
            await self.db.update_player(self.uid,**u)
            await i.response.send_message(embed=make_embed(f"{d.get('emoji','')} {name}",d["desc"],COLOR_GREEN),ephemeral=True)
        return cb

class BooksView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    @discord.ui.select(placeholder="📚 اختار كتاب",options=[discord.SelectOption(label=f"{d.get('emoji','')} {n} — {d['price']}ج",value=n,description=d["desc"][:50]) for n,d in BOOKS.items()])
    async def sel(self,i,s):
        if i.user.id!=self.uid: return
        p=await ensure_player(self.db,i);
        if not p: return
        n=s.values[0]; d=BOOKS[n]
        if await check_money(self.db,i,p,d["price"]): return
        u={"money":p["money"]-d["price"]}
        for k in STAT_FIELDS|SKILL_FIELDS|{"charisma"}:
            if k in d: u[k]=clamp(p.get(k,0)+d[k])
        await self.db.update_player(self.uid,**u)
        ms=await add_xp_and_level(self.db,self.uid,d.get("xp",0)) if d.get("xp") else []
        await self.db.progress_quest(self.uid,"book_5"); await self.db.add_item(self.uid,n,1,"كتاب")
        await i.response.send_message(embed=make_embed(f"📖 قرأت {n}",f"{d['desc']}\n"+"\n".join(ms),COLOR_PURPLE),ephemeral=True)
