# -*- coding: utf-8 -*-
"""main_menu.py — المنيو الرئيسية — dev by 7amo"""
from __future__ import annotations
import discord
from discord.ui import View,Button
from config import *
from services.canvas import generate_profile_image
from services.economy import player_stats_text,money_fmt,clamp,fmt_seconds,random_mathal
from services.cooldowns import ensure_player
from views.helpers import make_embed
from data.shop import HOUSES

class MainMenuView(View):
    def __init__(self,uid,db): super().__init__(timeout=360); self.uid=uid; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌ مش بتاعتك.",ephemeral=True); return False
        return True

    @discord.ui.button(label="📊 بروفايل",style=discord.ButtonStyle.primary,row=0)
    async def profile(self,i,b):
        p=await ensure_player(self.db,i)
        if not p: return
        e=make_embed(f"🎭 {p['display_name']}",player_stats_text(p),COLOR_GOLD)
        img=await generate_profile_image(p); f=discord.File(img,filename="p.png"); e.set_image(url="attachment://p.png")
        await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db))

    @discord.ui.button(label="💼 شغل",style=discord.ButtonStyle.success,row=0)
    async def jobs(self,i,b):
        from views.jobs import JobsView
        p=await ensure_player(self.db,i);
        if not p: return
        await i.response.send_message(embed=make_embed("💼 الشغل",f"وظيفتك: **{p['job']}** | رتبة: **{p['job_rank'] or 'مبتدئ'}** | Job XP: **{p['job_xp']:,}**\n\n💡 *{random_mathal()}*",COLOR_GREEN),view=JobsView(self.uid,self.db),ephemeral=True)

    @discord.ui.button(label="🛒 متجر",style=discord.ButtonStyle.secondary,row=0)
    async def shop(self,i,b):
        from views.shop import MarketView
        await i.response.send_message(embed=make_embed("🛒 السوق المصري","اختار القسم 👇\n\n💡 *الغالي تمنه فيه*",COLOR_BLUE),view=MarketView(self.uid,self.db),ephemeral=True)

    @discord.ui.button(label="😴 نوم",style=discord.ButtonStyle.primary,row=0)
    async def sleep(self,i,b):
        p=await ensure_player(self.db,i);
        if not p: return
        rem=await self.db.cooldown_remaining(self.uid,"sleep")
        if rem: await i.response.send_message(f"⏰ لسه بدري! باقي: **{fmt_seconds(rem)}**",ephemeral=True); return
        hd=HOUSES[p["house"]]; eg=clamp(p["energy"]+45+hd["energy_bonus"]//3); hh=clamp(p["health"]+12); hp=clamp(p["happiness"]+max(0,hd["happiness_bonus"]//2))
        await self.db.update_player(self.uid,energy=eg,health=hh,happiness=hp,hygiene=clamp(p["hygiene"]-5))
        await self.db.set_cooldown(self.uid,"sleep",hours=4)
        from services.canvas import generate_result_image
        lines=[f"🏠 نمت في: {p['house']}",f"⚡ طاقة: {p['energy']}→{eg}%",f"❤️ صحة: {hh}%",f"😊 سعادة: {hp}%"]
        img=await generate_result_image("😴 نومة هنية يا معلم",lines,"#3498db"); f=discord.File(img,filename="s.png")
        e=make_embed("😴 نمت كويس!","\n".join(lines),COLOR_BLUE); e.set_image(url="attachment://s.png")
        await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db))

    @discord.ui.button(label="🍗 أكل/شرب",style=discord.ButtonStyle.success,row=0)
    async def eat(self,i,b):
        from views.shop import QuickFoodView
        await i.response.send_message(embed=make_embed("🍗 أكل وشرب","اختار حاجة يا معلم!\n💡 *الأكل في الشبعان لذة*",COLOR_ORANGE),view=QuickFoodView(self.uid,self.db),ephemeral=True)

    @discord.ui.button(label="🔫 سرقة RPG",style=discord.ButtonStyle.danger,row=1)
    async def steal(self,i,b):
        from views.crime import StealView
        await i.response.send_message(embed=make_embed("🔫 سرقة خيالية","⚠️ نظام خيالي للعبة فقط.",COLOR_RED),view=StealView(self.uid,self.db),ephemeral=True)

    @discord.ui.button(label="💻 شغل حر",style=discord.ButtonStyle.primary,row=1)
    async def freelance(self,i,b):
        from views.freelance import FreelanceView
        await i.response.send_message(embed=make_embed("💻 شغل حر","برمجة · تصميم · أمن · كورسات",COLOR_BLUE),view=FreelanceView(self.uid,self.db),ephemeral=True)

    @discord.ui.button(label="🏦 بنك",style=discord.ButtonStyle.secondary,row=1)
    async def bank(self,i,b):
        from views.bank import BankView
        p=await ensure_player(self.db,i);
        if not p: return
        await i.response.send_message(embed=make_embed("🏦 بنك مصر",f"💰 كاش: **{money_fmt(p['money'])}**\n🏦 بنك: **{money_fmt(p['bank'])}**\n\n💡 *القرش الأبيض ينفع في اليوم الأسود*",COLOR_BLUE),view=BankView(self.uid,self.db),ephemeral=True)

    @discord.ui.button(label="🏠 عقارات",style=discord.ButtonStyle.secondary,row=1)
    async def assets(self,i,b):
        from views.assets import AssetsView
        await i.response.send_message(embed=make_embed("🏠🚗🏪 الأصول","بيوت · سيارات · بزنس",COLOR_GOLD),view=AssetsView(self.uid,self.db),ephemeral=True)

    @discord.ui.button(label="🎰 مراهنات",style=discord.ButtonStyle.danger,row=2)
    async def gamble(self,i,b):
        from views.gambling import GamblingView
        await i.response.send_message(embed=make_embed("🎰 كازينو مصر","العب واكسب! ⚠️ القمار بيخسّر.\n💡 *اللي يلعب بالنار يتحرق*",COLOR_RED),view=GamblingView(self.uid,self.db),ephemeral=True)

    @discord.ui.button(label="⚽ رياضة/ستريم",style=discord.ButtonStyle.success,row=2)
    async def sports(self,i,b):
        from views.sports import SportsView
        await i.response.send_message(embed=make_embed("⚽ رياضة وستريم","كورة · جيم · لايف",COLOR_GREEN),view=SportsView(self.uid,self.db),ephemeral=True)

    @discord.ui.button(label="👥 عصابات",style=discord.ButtonStyle.danger,row=2)
    async def gang(self,i,b):
        from views.gang import GangView
        await i.response.send_message(embed=make_embed("👥 العصابات","انضم لعصابة!",COLOR_RED),view=GangView(self.uid,self.db),ephemeral=True)

    @discord.ui.button(label="🎒 شنطة",style=discord.ButtonStyle.secondary,row=2)
    async def inv(self,i,b):
        items=await self.db.get_inventory(self.uid)
        if not items: d="🎒 فاضية. روح المتجر!"
        else:
            gr={}
            for r in items:
                t=r["item_type"]
                if t not in gr: gr[t]=[]
                gr[t].append(f"• **{r['item']}** x{r['quantity']}")
            d="".join(f"\n**━ {t} ━**\n"+"\n".join(il)+"\n" for t,il in gr.items())
        await i.response.send_message(embed=make_embed("🎒 الشنطة",d[:3900],COLOR_PURPLE),ephemeral=True)

    @discord.ui.button(label="🎭 ترفيه",style=discord.ButtonStyle.success,row=2)
    async def fun(self,i,b):
        from views.entertainment import EntertainmentView
        await i.response.send_message(embed=make_embed("🎭 ترفيه","قهوة · سينما · ملاهي · شيشة · نيل\n💡 *الضحك بلا سبب من قلة الأدب* 😂",COLOR_PURPLE),view=EntertainmentView(self.uid,self.db),ephemeral=True)

    @discord.ui.button(label="📋 مهام",style=discord.ButtonStyle.success,row=3)
    async def quests(self,i,b):
        rows=await self.db.fetchall("SELECT * FROM quests WHERE user_id=? ORDER BY completed,id",(self.uid,))
        d="\n".join([f"{'✅' if r['completed'] else '⬜'} **{r['quest_name']}** ({r['progress']}/{r['target']}) — 💰{r['reward_money']:,} ⭐{r['reward_xp']:,}" for r in rows]) or "مفيش مهام."
        await i.response.send_message(embed=make_embed("📋 المهام",d[:3900],COLOR_GREEN),ephemeral=True)

    @discord.ui.button(label="🏆 توب",style=discord.ButtonStyle.secondary,row=3)
    async def top(self,i,b):
        rows=await self.db.leaderboard()
        md=["🥇","🥈","🥉"]+["🏅"]*12
        d="\n".join([f"{md[x]} **{r['display_name']}** ({r['char_class']}) — Score {r['score']:,} | 💰{r['money']+r['bank']:,} | ⭐{r['level']}" for x,r in enumerate(rows)]) or "مفيش لاعبين."
        await i.response.send_message(embed=make_embed("🏆 التوب",d[:3900],COLOR_GOLD),ephemeral=True)

    @discord.ui.button(label="💍 جواز",style=discord.ButtonStyle.primary,row=3)
    async def marry(self,i,b):
        await i.response.send_message(embed=make_embed("💍 الجواز","`!جواز @الشخص` أو `/marry`\n`!طلاق` أو `/divorce`\n\n⚠️ لازم تكون بالغ\n💡 *امشي في جنازة ولا تمشي في جوازة* 😂",COLOR_PURPLE),ephemeral=True)

    @discord.ui.button(label="🧼 نظافة",style=discord.ButtonStyle.secondary,row=3)
    async def hygiene(self,i,b):
        from views.shop import HygieneView
        await i.response.send_message(embed=make_embed("🧼 النظافة","نضّف نفسك يا معلم!",COLOR_BLUE),view=HygieneView(self.uid,self.db),ephemeral=True)

    @discord.ui.button(label="📚 مكتبة",style=discord.ButtonStyle.primary,row=3)
    async def books(self,i,b):
        from views.shop import BooksView
        await i.response.send_message(embed=make_embed("📚 المكتبة","اقرا وطوّر نفسك!\n💡 *العلم نور*",COLOR_PURPLE),view=BooksView(self.uid,self.db),ephemeral=True)
