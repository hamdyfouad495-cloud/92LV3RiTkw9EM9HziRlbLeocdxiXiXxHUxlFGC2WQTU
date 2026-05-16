# -*- coding: utf-8 -*-
"""bank.py — البنك + تحويل فلوس — dev by 7amo"""
from __future__ import annotations
import discord
from discord.ui import View,Button,Modal,TextInput
from config import COLOR_BLUE,COLOR_GREEN
from services.economy import money_fmt
from services.cooldowns import ensure_player
from views.helpers import make_embed

class AmountModal(Modal):
    def __init__(self,title,uid,mode,db):
        super().__init__(title=title,timeout=120); self.uid=uid; self.mode=mode; self.db=db
        self.amt=TextInput(label="المبلغ",placeholder="500 أو all",min_length=1,max_length=12); self.add_item(self.amt)
    async def on_submit(self,i):
        p=await self.db.get_player(self.uid)
        if not p: await i.response.send_message("❌",ephemeral=True); return
        raw=str(self.amt.value).strip().lower()
        if raw in ("all","كل","الكل"): a=p["money"] if self.mode=="dep" else p["bank"]
        else:
            try: a=int(raw.replace(",",""))
            except: await i.response.send_message("❌ رقم صحيح!",ephemeral=True); return
        if a<=0: await i.response.send_message("❌ أكبر من صفر!",ephemeral=True); return
        if self.mode=="dep":
            if p["money"]<a: await i.response.send_message("❌ مش كفاية.",ephemeral=True); return
            await self.db.update_player(self.uid,money=p["money"]-a,bank=p["bank"]+a)
            msg=f"✅ أودعت **{money_fmt(a)}**\n💰 كاش: **{money_fmt(p['money']-a)}**\n🏦 بنك: **{money_fmt(p['bank']+a)}**"
        else:
            if p["bank"]<a: await i.response.send_message("❌ مش كفاية.",ephemeral=True); return
            await self.db.update_player(self.uid,money=p["money"]+a,bank=p["bank"]-a)
            msg=f"✅ سحبت **{money_fmt(a)}**\n💰 كاش: **{money_fmt(p['money']+a)}**\n🏦 بنك: **{money_fmt(p['bank']-a)}**"
        await self.db.log(self.uid,self.mode,a)
        await i.response.send_message(embed=make_embed("🏦",msg,COLOR_GREEN),ephemeral=True)

class TransferModal(Modal):
    def __init__(self,uid,db):
        super().__init__(title="💸 تحويل فلوس",timeout=120); self.uid=uid; self.db=db
        self.target_id=TextInput(label="ID اللاعب",placeholder="رقم الـ ID",min_length=1); self.add_item(self.target_id)
        self.amt=TextInput(label="المبلغ",placeholder="500",min_length=1); self.add_item(self.amt)
    async def on_submit(self,i):
        p=await self.db.get_player(self.uid)
        if not p: return
        try: tid=int(self.target_id.value); a=int(self.amt.value.replace(",",""))
        except: await i.response.send_message("❌ أرقام صحيحة!",ephemeral=True); return
        if a<=0 or tid==self.uid: await i.response.send_message("❌",ephemeral=True); return
        if p["money"]<a: await i.response.send_message("❌ مش كفاية.",ephemeral=True); return
        t=await self.db.get_player(tid)
        if not t: await i.response.send_message("❌ اللاعب مش مسجل.",ephemeral=True); return
        await self.db.update_player(self.uid,money=p["money"]-a)
        await self.db.update_player(tid,money=t["money"]+a)
        await self.db.log(self.uid,"transfer",a,f"to {tid}")
        await self.db.progress_quest(self.uid,"transfer_1")
        await i.response.send_message(embed=make_embed("💸 تحويل",f"حوّلت **{money_fmt(a)}** لـ **{t['display_name']}**\n💡 *الجود من الموجود*",COLOR_GREEN),ephemeral=True)

class BankView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌",ephemeral=True); return False
        return True
    @discord.ui.button(label="📥 إيداع",style=discord.ButtonStyle.success)
    async def dep(self,i,b): await i.response.send_modal(AmountModal("إيداع",self.uid,"dep",self.db))
    @discord.ui.button(label="📤 سحب",style=discord.ButtonStyle.primary)
    async def wit(self,i,b): await i.response.send_modal(AmountModal("سحب",self.uid,"wit",self.db))
    @discord.ui.button(label="💳 كشف حساب",style=discord.ButtonStyle.secondary)
    async def bal(self,i,b):
        p=await ensure_player(self.db,i);
        if not p: return
        await i.response.send_message(embed=make_embed("🏦",f"💰 كاش: **{money_fmt(p['money'])}**\n🏦 بنك: **{money_fmt(p['bank'])}**\n💵 إجمالي: **{money_fmt(p['money']+p['bank'])}**\n📊 مكسب: {money_fmt(p['total_earnings'])} | مصروف: {money_fmt(p['total_spent'])}",COLOR_BLUE),ephemeral=True)
    @discord.ui.button(label="💸 تحويل",style=discord.ButtonStyle.primary)
    async def transfer(self,i,b): await i.response.send_modal(TransferModal(self.uid,self.db))
