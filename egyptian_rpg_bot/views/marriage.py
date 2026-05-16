# -*- coding: utf-8 -*-
"""marriage.py — جواز وطلاق — dev by 7amo"""
from __future__ import annotations
import discord
from discord.ui import View,Button
from config import COLOR_PURPLE
from services.economy import clamp
from views.helpers import make_embed

class MarriageOfferView(View):
    def __init__(self,pid,tid,db): super().__init__(timeout=120); self.pid=pid; self.tid=tid; self.db=db
    @discord.ui.button(label="✅ موافق/ة 💍",style=discord.ButtonStyle.success)
    async def yes(self,i,b):
        if i.user.id!=self.tid: await i.response.send_message("❌",ephemeral=True); return
        p1=await self.db.get_player(self.pid); p2=await self.db.get_player(self.tid)
        if not p1 or not p2: await i.response.send_message("❌ لازم الطرفين مسجلين.",ephemeral=True); return
        if p1["married_to"] or p2["married_to"]: await i.response.send_message("❌ حد متزوج.",ephemeral=True); return
        await self.db.update_player(self.pid,married_to=self.tid,happiness=clamp(p1["happiness"]+25),reputation=p1["reputation"]+15)
        await self.db.update_player(self.tid,married_to=self.pid,happiness=clamp(p2["happiness"]+25),reputation=p2["reputation"]+15)
        ms=await self.db.progress_quest(self.pid,"marry_1"); ms.extend(await self.db.progress_quest(self.tid,"marry_1"))
        await i.response.send_message(embed=make_embed("💍 ألف مبروك!",f"**{p1['display_name']}** 💞 **{p2['display_name']}**\n😊 +25 | 🔥 +15\n💡 *ربنا يهنيكم*\n"+"\n".join(ms),COLOR_PURPLE)); self.stop()
    @discord.ui.button(label="❌ رفض 💔",style=discord.ButtonStyle.danger)
    async def no(self,i,b):
        if i.user.id!=self.tid: return
        await i.response.send_message("💔 تم الرفض. معلش!\n💡 *الحلو مايكملش*"); self.stop()
