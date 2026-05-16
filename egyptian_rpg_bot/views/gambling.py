# -*- coding: utf-8 -*-
"""gambling.py — مراهنات مصرية (متوازنة) — dev by 7amo"""
from __future__ import annotations
import random,discord
from discord.ui import View,Select,Modal,TextInput
from config import COLOR_GREEN,COLOR_RED
from data.quests import GAMBLING_GAMES
from services.economy import money_fmt,clamp
from services.cooldowns import ensure_player,check_jail_guard
from services.canvas import generate_gamble_image
from views.helpers import make_embed

def _play(game,bet):
    if game=="صقعة (كوتشينة)":
        ph=random.randint(2,21); dh=random.randint(2,21)
        if ph>21: return False,0,f"إيدك: {ph} (باست!) | ديلر: {dh}"
        if dh>21 or ph>dh: return True,int(bet*1.5),f"إيدك: {ph} | ديلر: {dh} 🎉"
        return False,0,f"إيدك: {ph} | ديلر: {dh} 😢"
    elif game=="طاولة (نرد)":
        d1,d2=random.randint(1,6),random.randint(1,6); t=d1+d2
        if t in(7,11): return True,int(bet*1.7),f"🎲 {d1}+{d2}={t} كسبت!"
        if t in(2,3,12): return False,0,f"🎲 {d1}+{d2}={t} خسرت!"
        return (True,int(bet*1.3),f"🎲 {d1}+{d2}={t} Point!") if random.random()<0.40 else (False,0,f"🎲 {d1}+{d2}={t} 7-out!")
    elif game=="كوتشينة عالي/واطي":
        f1,f2=random.randint(2,14),random.randint(2,14); g=random.choice(["عالي","واطي"])
        ok=(g=="عالي" and f2>f1)or(g=="واطي" and f2<f1)
        return (True,int(bet*1.8),f"🂡 {f1}→{f2} {g} ✅") if ok else (False,0,f"🂡 {f1}→{f2} {g} ❌")
    elif game=="سلوتس مصري":
        sym=["🍉","🍋","🍇","💎","7️⃣","🔔","⭐","🍀"]; r=[random.choice(sym) for _ in range(3)]; rs=" | ".join(r)
        if r[0]==r[1]==r[2]: return True,bet*(8 if r[0]=="💎" else 5 if r[0]=="7️⃣" else 3),f"🎰 {rs} جاكبوت!"
        if r[0]==r[1] or r[1]==r[2]: return True,int(bet*1.3),f"🎰 {rs} اتنين!"
        return False,0,f"🎰 {rs} 😢"
    elif game=="لعبة الكوبايات":
        c=random.randint(1,3); g=random.randint(1,3)
        return (True,int(bet*2.2),f"كوباية {c} ✅") if g==c else (False,0,f"كوباية {c} مش {g} ❌")
    return False,0,"?"

class BetModal(Modal):
    def __init__(self,uid,db,game):
        super().__init__(title=f"🎰 {game}",timeout=120); self.uid=uid; self.db=db; self.game=game
        gd=GAMBLING_GAMES[game]; self.amt=TextInput(label=f"المبلغ ({gd['min_bet']}-{gd['max_bet']})",placeholder=str(gd['min_bet']*2),min_length=1,max_length=10); self.add_item(self.amt)
    async def on_submit(self,i):
        p=await self.db.get_player(self.uid)
        if not p: return
        gd=GAMBLING_GAMES[self.game]
        try: bet=int(str(self.amt.value).strip().replace(",",""))
        except: await i.response.send_message("❌ رقم!",ephemeral=True); return
        if bet<gd["min_bet"] or bet>gd["max_bet"]: await i.response.send_message("❌ خارج النطاق.",ephemeral=True); return
        if p["money"]<bet: await i.response.send_message("❌ مش كفاية.",ephemeral=True); return
        won,payout,rt=_play(self.game,bet)
        if won:
            await self.db.update_player(self.uid,money=p["money"]+payout,happiness=clamp(p["happiness"]+6),total_earnings=p["total_earnings"]+payout)
            await self.db.progress_quest(self.uid,"gamble_win_5")
        else:
            await self.db.update_player(self.uid,money=p["money"]-bet,happiness=clamp(p["happiness"]-4),total_spent=p["total_spent"]+bet)
            payout=bet
        await self.db.log_gamble(self.uid,self.game,bet,won,payout)
        img=await generate_gamble_image(self.game,rt,bet,payout,won); f=discord.File(img,filename="g.png")
        e=make_embed("🎉 كسبت!" if won else "😢 خسرت!",f"🎮 {self.game}\n💰 رهان: {money_fmt(bet)}\n🎯 {rt}\n{'💵 كسبت' if won else '💸 خسرت'}: **{money_fmt(payout)}**",COLOR_GREEN if won else COLOR_RED)
        e.set_image(url="attachment://g.png")
        from views.main_menu import MainMenuView
        await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db))

class GamblingView(View):
    def __init__(self,uid,db): super().__init__(timeout=180); self.uid=uid; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌",ephemeral=True); return False
        return True
    @discord.ui.select(placeholder="🎰 اختار لعبة",options=[discord.SelectOption(label=f"{d['emoji']} {n}",value=n,description=f"{d['min_bet']}-{d['max_bet']}ج") for n,d in GAMBLING_GAMES.items()])
    async def sel(self,i,s):
        if await check_jail_guard(self.db,i): return
        await i.response.send_modal(BetModal(self.uid,self.db,s.values[0]))
