# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════╗
║  🎮  EGYPTIAN RPG BOT — PROFESSIONAL MAX EDITION                  ║
║  𝐝𝐞𝐯 𝐛𝐲 𝟕𝐚𝐦𝐨 © 2026 — جميع الحقوق محفوظة                      ║
║  Install: pip install -U discord.py Pillow aiohttp                ║
║  Run:     DISCORD_TOKEN="..." python bot.py                       ║
╚════════════════════════════════════════════════════════════════════╝
"""
from __future__ import annotations
import os,sys,random,logging
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands,tasks

sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))

from config import *
from database import ProDatabase
from data.classes import AGE_GROUPS
from services.economy import player_stats_text,money_fmt,clamp,random_mathal,fmt_seconds
from services.canvas import generate_profile_image
from views.helpers import make_embed
from views.start import StartView
from views.main_menu import MainMenuView
from views.marriage import MarriageOfferView
from data.quests import EGYPTIAN_JOKES

logging.basicConfig(level=logging.INFO,format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.FileHandler('bot.log',encoding='utf-8'),logging.StreamHandler()])
log=logging.getLogger("7amo_rpg")

intents=discord.Intents.default(); intents.message_content=True; intents.members=True
bot=commands.Bot(command_prefix=PREFIX,intents=intents,help_command=None)
db=ProDatabase(DB_FILE)

# ═══════════════════════════════════════════════════════════════════
# SHARED
# ═══════════════════════════════════════════════════════════════════
async def send_start(dest):
    user=dest.author if isinstance(dest,commands.Context) else dest.user
    p=await db.get_player(user.id)
    if p:
        e=make_embed("✅ مسجل بالفعل!",f"أهلاً **{p['display_name']}**!\nاستخدم `!منيو` أو `/menu`.\n\n💡 *{random_mathal()}*",COLOR_BLUE)
        v=MainMenuView(user.id,db)
        if isinstance(dest,commands.Context): await dest.reply(embed=e,view=v,mention_author=False)
        else: await dest.response.send_message(embed=e,view=v,ephemeral=True)
        return
    desc=("🇪🇬 **أهلاً بيك في مصر RPG!** 🎮\n\n"
          "اختار شخصيتك ونوعك وعمرك وابدأ!\n\n"
          "**الشخصيات:**\n"
          "👔 موظف | 💪 بلطجي | 😎 عريس الجنة | 🌾 فلاح\n"
          "📚 طالب | 💻 مبرمج | ⚽ لاعب كورة | 🎥 ستريمر\n"
          "🥺 شحات | 😴 عاطل\n\n"
          f"💡 *{random.choice(WELCOME_MSGS)}*")
    e=make_embed("🎮 ابدأ رحلتك!",desc,COLOR_GOLD)
    v=StartView(user,db)
    if isinstance(dest,commands.Context): await dest.reply(embed=e,view=v,mention_author=False)
    else: await dest.response.send_message(embed=e,view=v,ephemeral=True)

async def marry_common(ch,proposer,target):
    if proposer.id==target.id: await ch.send("❌ مش هتتجوز نفسك! 😂 *الحلو مايكملش*"); return
    if target.bot: await ch.send("❌ البوتات مش بتتجوز 🤖"); return
    p1=await db.get_player(proposer.id); p2=await db.get_player(target.id)
    if not p1 or not p2: await ch.send("❌ لازم الطرفين مسجلين."); return
    if not AGE_GROUPS[p1["age_group"]].get("can_marry",True) or not AGE_GROUPS[p2["age_group"]].get("can_marry",True):
        await ch.send("❌ الجواز للبالغين فقط."); return
    if p1["married_to"] or p2["married_to"]: await ch.send("❌ حد متزوج بالفعل."); return
    await ch.send(embed=make_embed("💍 عرض جواز!",f"{target.mention}، **{proposer.display_name}** طلب يتجوزك! 💞\n\n💡 *امشي في جنازة ولا تمشي في جوازة* 😂",COLOR_PURPLE),view=MarriageOfferView(proposer.id,target.id,db))

async def divorce_common(user,dest):
    p=await db.get_player(user.id)
    if not p or not p["married_to"]: msg="❌ مش متزوج/ة."
    else:
        oid=p["married_to"]
        await db.update_player(user.id,married_to=None,happiness=clamp(p["happiness"]-20))
        o=await db.get_player(oid)
        if o: await db.update_player(oid,married_to=None,happiness=clamp(o["happiness"]-20))
        msg="💔 تم الطلاق. سعادة -20.\n💡 *ربنا يعوّض على الجميع*"
    e=make_embed("💔 طلاق",msg,COLOR_RED)
    if isinstance(dest,commands.Context): await dest.reply(embed=e,mention_author=False)
    else: await dest.followup.send(embed=e,ephemeral=True)

def help_embed():
    return make_embed("📖 مساعدة مصر RPG",f"""
**🎮 بداية:**
`!ابدأ` `/start` — تسجيل | `!منيو` `/menu` — المنيو

**📊 معلومات:**
`!بروفايل` `/profile` — بروفايلك | `!توب` `/top` — الترتيب

**💰 اقتصاد:**
`!يومي` `/daily` — مكافأة يومية

**💍 اجتماعي:**
`!جواز @user` `/marry` — جواز | `!طلاق` `/divorce` — طلاق

**😂 ترفيه:**
`!نكتة` — نكتة مصرية | `!مثل` — مثل شعبي

**🔧 إدارة:**
`!حذف` — حذف الحساب

**🎮 المنيو فيها:**
📊 بروفايل | 💼 شغل+ترقيات | 🛒 متجر (8 أقسام)
😴 نوم | 🍗 أكل | 🔫 سرقة | 💻 فريلانس | 🏦 بنك+تحويل
🏠 عقارات | 🚗 سيارات | 🏪 بزنس | 🎰 مراهنات (5 ألعاب)
⚽ كورة | 💪 جيم | 🎥 ستريم | 👥 عصابات | 🎭 ترفيه
🧼 نظافة | 📚 مكتبة | 📋 مهام | 🏆 توب | 💍 جواز

⚠️ أنظمة السرقة/الأمن خيالية للعبة فقط.
{OWNER_BRAND}""",COLOR_BLUE)

# ═══════════════════════════════════════════════════════════════════
# PREFIX COMMANDS
# ═══════════════════════════════════════════════════════════════════
@bot.command(name="ابدأ",aliases=["start","بداية","سجل"])
async def cmd_start(ctx): await send_start(ctx)

@bot.command(name="منيو",aliases=["menu","قائمة","لعب"])
async def cmd_menu(ctx):
    p=await db.get_player(ctx.author.id)
    if not p: await ctx.reply("❌ اكتب `!ابدأ`.",mention_author=False); return
    await ctx.reply(embed=make_embed(f"🎮 أهلاً يا {p['display_name']}!",f"اختار من الأزرار 👇\n💡 *{random_mathal()}*",COLOR_BLUE),view=MainMenuView(ctx.author.id,db),mention_author=False)

@bot.command(name="بروفايل",aliases=["profile","انا","ب"])
async def cmd_profile(ctx,member:Optional[discord.Member]=None):
    member=member or ctx.author; p=await db.get_player(member.id)
    if not p: await ctx.reply("❌ مش مسجل.",mention_author=False); return
    e=make_embed(f"🎭 {p['display_name']}",player_stats_text(p),COLOR_GOLD)
    img=await generate_profile_image(p); f=discord.File(img,filename="p.png"); e.set_image(url="attachment://p.png")
    await ctx.reply(embed=e,file=f,mention_author=False)

@bot.command(name="توب",aliases=["top","leaderboard"])
async def cmd_top(ctx):
    rows=await db.leaderboard()
    md=["🥇","🥈","🥉"]+["🏅"]*12
    d="\n".join([f"{md[x]} **{r['display_name']}** ({r['char_class']}) — {r['score']:,} | 💰{r['money']+r['bank']:,} | ⭐{r['level']}" for x,r in enumerate(rows)]) or "مفيش لاعبين."
    await ctx.reply(embed=make_embed("🏆 التوب",d[:3900],COLOR_GOLD),mention_author=False)

@bot.command(name="جواز",aliases=["marry"])
async def cmd_marry(ctx,target:discord.Member): await marry_common(ctx.channel,ctx.author,target)

@bot.command(name="طلاق",aliases=["divorce"])
async def cmd_divorce(ctx): await divorce_common(ctx.author,ctx)

@bot.command(name="نكتة",aliases=["joke"])
async def cmd_joke(ctx): await ctx.reply(embed=make_embed("😂 نكتة مصري",random.choice(EGYPTIAN_JOKES),COLOR_GOLD),mention_author=False)

@bot.command(name="مثل",aliases=["mathal"])
async def cmd_mathal(ctx): await ctx.reply(embed=make_embed("📜 مثل شعبي",random_mathal(),COLOR_GOLD),mention_author=False)

@bot.command(name="يومي",aliases=["daily"])
async def cmd_daily(ctx):
    p=await db.get_player(ctx.author.id)
    if not p: await ctx.reply("❌ اكتب `!ابدأ`.",mention_author=False); return
    rem=await db.cooldown_remaining(ctx.author.id,"daily")
    if rem: await ctx.reply(f"⏰ باقي: **{fmt_seconds(rem)}**",mention_author=False); return
    streak=p["daily_streak"]+1; reward=200+(streak*50)
    bonus=""
    if streak>=7: reward+=500; bonus="\n🎁 **بونص أسبوع! +500**"
    await db.update_player(ctx.author.id,money=p["money"]+reward,daily_streak=streak,happiness=clamp(p["happiness"]+5))
    await db.set_cooldown(ctx.author.id,"daily",hours=20)
    await db.progress_quest(ctx.author.id,"daily_7",streak,absolute=True)
    await ctx.reply(embed=make_embed("🎁 يومي!",f"💰 **{money_fmt(reward)}**\n🔥 سلسلة: **{streak}** يوم\n😊 +5{bonus}\n💡 *{random_mathal()}*",COLOR_GREEN),mention_author=False)

@bot.command(name="حذف",aliases=["delete","reset"])
async def cmd_delete(ctx):
    p=await db.get_player(ctx.author.id)
    if not p: await ctx.reply("❌ مش مسجل.",mention_author=False); return
    await db.delete_player(ctx.author.id)
    await ctx.reply(embed=make_embed("🗑️ تم الحذف","حسابك اتحذف. اكتب `!ابدأ` لو عايز ترجع.\n💡 *ربنا يعوّض عليك*",COLOR_RED),mention_author=False)

@bot.command(name="مساعدة",aliases=["help","اوامر"])
async def cmd_help(ctx): await ctx.reply(embed=help_embed(),mention_author=False)

# ═══════════════════════════════════════════════════════════════════
# SLASH COMMANDS
# ═══════════════════════════════════════════════════════════════════
@bot.tree.command(name="start",description="ابدأ مصر RPG")
async def sl_start(i): await send_start(i)

@bot.tree.command(name="menu",description="المنيو")
async def sl_menu(i):
    p=await db.get_player(i.user.id)
    if not p: await i.response.send_message("❌ `/start`",ephemeral=True); return
    await i.response.send_message(embed=make_embed(f"🎮 {p['display_name']}!",f"👇\n💡 *{random_mathal()}*",COLOR_BLUE),view=MainMenuView(i.user.id,db),ephemeral=True)

@bot.tree.command(name="profile",description="بروفايل")
@app_commands.describe(user="لاعب")
async def sl_profile(i,user:Optional[discord.Member]=None):
    u=user or i.user; p=await db.get_player(u.id)
    if not p: await i.response.send_message("❌",ephemeral=True); return
    e=make_embed(f"🎭 {p['display_name']}",player_stats_text(p),COLOR_GOLD)
    img=await generate_profile_image(p); f=discord.File(img,filename="p.png"); e.set_image(url="attachment://p.png")
    await i.response.send_message(embed=e,file=f)

@bot.tree.command(name="top",description="الترتيب")
async def sl_top(i):
    rows=await db.leaderboard()
    md=["🥇","🥈","🥉"]+["🏅"]*12
    d="\n".join([f"{md[x]} **{r['display_name']}** — {r['score']:,}" for x,r in enumerate(rows)]) or "لا."
    await i.response.send_message(embed=make_embed("🏆",d[:3900],COLOR_GOLD))

@bot.tree.command(name="marry",description="جواز")
@app_commands.describe(user="اللاعب")
async def sl_marry(i,user:discord.Member): await i.response.defer(); await marry_common(i.channel,i.user,user)

@bot.tree.command(name="divorce",description="طلاق")
async def sl_divorce(i): await i.response.defer(ephemeral=True); await divorce_common(i.user,i)

@bot.tree.command(name="help",description="مساعدة")
async def sl_help(i): await i.response.send_message(embed=help_embed(),ephemeral=True)

@bot.tree.command(name="daily",description="المكافأة اليومية")
async def sl_daily(i):
    p=await db.get_player(i.user.id)
    if not p: await i.response.send_message("❌ `/start`",ephemeral=True); return
    rem=await db.cooldown_remaining(i.user.id,"daily")
    if rem: await i.response.send_message(f"⏰ {fmt_seconds(rem)}",ephemeral=True); return
    s=p["daily_streak"]+1; r=200+(s*50)+(500 if s>=7 else 0)
    await db.update_player(i.user.id,money=p["money"]+r,daily_streak=s,happiness=clamp(p["happiness"]+5))
    await db.set_cooldown(i.user.id,"daily",hours=20)
    await i.response.send_message(embed=make_embed("🎁",f"💰 **{money_fmt(r)}** | 🔥 {s} يوم",COLOR_GREEN),ephemeral=True)

# ═══════════════════════════════════════════════════════════════════
# EVENTS & TASKS
# ═══════════════════════════════════════════════════════════════════
@bot.event
async def on_ready():
    log.info("═"*55)
    log.info(f"  🎮 Logged in as {bot.user}")
    log.info(f"  {OWNER_BRAND}")
    log.info(f"  Servers: {len(bot.guilds)}")
    log.info("═"*55)
    if not hasattr(bot,"_synced"):
        try: s=await bot.tree.sync(); log.info(f"  ✅ Synced {len(s)} slash")
        except Exception as e: log.warning(f"  ⚠️ Sync: {e}")
        bot._synced=True
    if not status_loop.is_running(): status_loop.start()
    if not stat_decay.is_running(): stat_decay.start()

@tasks.loop(minutes=5)
async def status_loop():
    ss=["🎮 مصر RPG | !ابدأ","💼 !منيو","🇪🇬 مصر أم الدنيا!","⚽ يلا كورة!","💻 شغل حر","🎰 مراهنات",OWNER_BRAND]
    await bot.change_presence(activity=discord.Game(random.choice(ss)))

@tasks.loop(hours=1)
async def stat_decay():
    """Stat decay — الجوع والعطش والنظافة بتنزل مع الوقت"""
    try:
        await db.execute("""UPDATE players SET
            hunger=MAX(0,hunger-4), thirst=MAX(0,thirst-6),
            hygiene=MAX(0,hygiene-3), energy=MIN(100,energy+2),
            updated_at=CURRENT_TIMESTAMP
            WHERE hunger>0 OR thirst>0 OR hygiene>0""")
        await db.execute("UPDATE players SET health=MAX(0,health-5) WHERE hunger<12 OR thirst<12")
        log.info("⏰ Stat decay applied")
    except Exception as e: log.error(f"Stat decay error: {e}")

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument): await ctx.reply("❌ حاجة ناقصة! `!مساعدة`",mention_author=False)
    elif isinstance(error,commands.BadArgument): await ctx.reply("❌ مش فاهم. اتأكد.",mention_author=False)
    elif isinstance(error,commands.CommandNotFound): return
    else: log.error(f"Cmd error: {error}"); await ctx.reply("⚠️ خطأ! جرب تاني.",mention_author=False)

# ═══════════════════════════════════════════════════════════════════
if __name__=="__main__":
    if not BOT_TOKEN or BOT_TOKEN=="YOUR_BOT_TOKEN_HERE":
        raise SystemExit("❌ حط التوكن في DISCORD_TOKEN\n   DISCORD_TOKEN='...' python bot.py")
    bot.run(BOT_TOKEN)
