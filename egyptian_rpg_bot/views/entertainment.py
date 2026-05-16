# -*- coding: utf-8 -*-
"""entertainment.py — ترفيه — dev by 7amo"""
from __future__ import annotations
import discord
from discord.ui import View,Select
from config import COLOR_GREEN,COLOR_PURPLE,STAT_FIELDS,SKILL_FIELDS
from data.shop import ENTERTAINMENT
from services.economy import clamp,money_fmt
from services.cooldowns import ensure_player,check_money
from views.helpers import make_embed

class EntertainmentView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌",ephemeral=True); return False
        return True
    @discord.ui.select(placeholder="🎭 نشاط",options=[discord.SelectOption(label=f"{d.get('emoji','')} {n} — {d['price']}ج",value=n,description=d["desc"][:50]) for n,d in ENTERTAINMENT.items()])
    async def sel(self,i,s):
        p=await ensure_player(self.db,i);
        if not p: return
        n=s.values[0]; d=ENTERTAINMENT[n]
        if await check_money(self.db,i,p,d["price"]): return
        u={"money":p["money"]-d["price"],"total_spent":p["total_spent"]+d["price"]}
        for k in list(STAT_FIELDS)+list(SKILL_FIELDS)+["charisma"]:
            if k in d: u[k]=clamp(p.get(k,0)+d[k])
        await self.db.update_player(self.uid,**u)
        await i.response.send_message(embed=make_embed(f"{d.get('emoji','')} {n}",f"{d['desc']}\n💰 {money_fmt(d['price'])}",COLOR_PURPLE),ephemeral=True)
