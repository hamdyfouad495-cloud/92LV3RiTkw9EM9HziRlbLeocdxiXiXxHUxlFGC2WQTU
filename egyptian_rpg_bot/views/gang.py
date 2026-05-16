# -*- coding: utf-8 -*-
"""gang.py — عصابات — dev by 7amo"""
from __future__ import annotations
import discord
from discord.ui import View,Button,Select
from config import COLOR_RED
from data.quests import GANGS
from services.cooldowns import ensure_player
from views.helpers import make_embed

class GangView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌",ephemeral=True); return False
        return True
    @discord.ui.select(placeholder="👥 عصابة",options=[discord.SelectOption(label=f"{d.get('emoji','')} {n}",value=n,description=f"{d['territory']} | سمعة {d['req_reputation']}") for n,d in GANGS.items()])
    async def sel(self,i,s):
        p=await ensure_player(self.db,i);
        if not p: return
        g=s.values[0]; d=GANGS[g]
        if p["gang"]: await i.response.send_message(f"❌ أنت في **{p['gang']}**.",ephemeral=True); return
        if p["reputation"]<d["req_reputation"]: await i.response.send_message(f"❌ محتاج سمعة **{d['req_reputation']}**.",ephemeral=True); return
        await self.db.update_player(self.uid,gang=g,gang_rank="عضو جديد",reputation=p["reputation"]+10)
        await self.db.execute("UPDATE gangs SET members_count=members_count+1 WHERE name=?",(g,))
        qm=await self.db.progress_quest(self.uid,"gang_1")
        from views.main_menu import MainMenuView
        await i.response.send_message(embed=make_embed(f"👥 {g}!",f"انضممت لـ **{g}**\n📍 {d['territory']}\n🔥 سمعة +10\n"+"\n".join(qm),COLOR_RED),view=MainMenuView(self.uid,self.db))
    @discord.ui.button(label="🚪 خروج",style=discord.ButtonStyle.secondary)
    async def leave(self,i,b):
        p=await ensure_player(self.db,i);
        if not p: return
        if not p["gang"]: await i.response.send_message("❌ مش في عصابة.",ephemeral=True); return
        old=p["gang"]
        await self.db.update_player(self.uid,gang=None,gang_rank=None,reputation=max(0,p["reputation"]-25))
        await self.db.execute("UPDATE gangs SET members_count=MAX(0,members_count-1) WHERE name=?",(old,))
        await i.response.send_message(embed=make_embed("🚪 خرجت",f"خرجت من **{old}**. سمعة -25.\n💡 *اللي يخرج من الجماعة الجماعة تاكله*",COLOR_RED),ephemeral=True)
