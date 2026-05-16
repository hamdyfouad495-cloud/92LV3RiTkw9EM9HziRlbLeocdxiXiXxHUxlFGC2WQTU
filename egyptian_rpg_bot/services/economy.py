# -*- coding: utf-8 -*-
"""economy.py — XP · money · stats · helpers — 𝐝𝐞𝐯 𝐛𝐲 𝟕𝐚𝐦𝐨"""
from __future__ import annotations
import random, sqlite3
from typing import Optional
import discord
from config import STAT_FIELDS, SKILL_FIELDS, AMTHAL, OWNER_BRAND

def clamp(v, lo=0, hi=100): return max(lo, min(hi, int(v)))
def money_fmt(n): return f"{int(n):,} ج.م"
def progress_bar(v, mx=100, ln=12):
    v=clamp(v,0,mx); f=int((v/mx)*ln); return "█"*f+"░"*(ln-f)
def fmt_seconds(s):
    if s<=0: return "دلوقتي ✅"
    h,r=divmod(s,3600); m,s2=divmod(r,60)
    if h: return f"{h}س {m}د"
    if m: return f"{m}د {s2}ث"
    return f"{s2}ث"

def xp_to_level(xp):
    level,needed,total=1,500,0
    while total+needed<=xp: total+=needed; level+=1; needed=int(needed*1.12)
    return level
def xp_for_next(xp):
    level,needed,total=1,500,0
    while total+needed<=xp: total+=needed; level+=1; needed=int(needed*1.12)
    return needed,xp-total

def random_mathal():
    return random.choice(AMTHAL)

async def add_xp_and_level(db, uid, xp_gain):
    p=await db.get_player(uid)
    if not p: return []
    new_xp=p["xp"]+xp_gain; new_lvl=xp_to_level(new_xp); msgs=[]
    await db.update_player(uid, xp=new_xp, level=max(p["level"],new_lvl))
    if new_lvl>p["level"]:
        bonus=new_lvl*55
        await db.update_player(uid, money=p["money"]+bonus)
        msgs.append(f"🆙 **لفل أب! بقيت لفل {new_lvl}** 🎉 | بونص {money_fmt(bonus)}")
    msgs.extend(await db.progress_quest(uid,"level_10",new_lvl,absolute=True))
    msgs.extend(await db.progress_quest(uid,"level_25",new_lvl,absolute=True))
    return msgs

async def apply_changes(db, uid, changes):
    p=await db.get_player(uid)
    if not p: return
    u={}
    for k,d in changes.items():
        if k in STAT_FIELDS: u[k]=clamp(p[k]+d)
        elif k in SKILL_FIELDS: u[k]=clamp(p[k]+d)
        elif k in {"money","bank","crypto","reputation","wanted_level","xp","total_earnings","total_spent","daily_streak","job_xp"}:
            mn=-999999 if k=="reputation" else 0; u[k]=max(mn,p[k]+d)
    if u: await db.update_player(uid,**u)

async def maybe_random_event(db, user):
    from data.quests import RANDOM_EVENTS
    if random.random()>0.22: return None
    ev=random.choice(RANDOM_EVENTS)
    ch={k:v for k,v in ev.items() if isinstance(v,int)}
    await apply_changes(db, user.id, ch)
    txt=f"🎲 **{ev['name']}**\n> {ev['desc']}"
    try:
        await user.send(embed=discord.Embed(title=f"🎲 {ev['name']}",description=ev['desc'],color=0xF39C12).set_footer(text=OWNER_BRAND))
    except: pass
    return txt

async def check_jail(db, uid):
    from datetime import datetime
    p=await db.get_player(uid)
    if not p or not p["jail_until"]: return None
    ju=datetime.fromisoformat(p["jail_until"])
    if datetime.now()>=ju:
        await db.update_player(uid, jail_until=None, wanted_level=max(0,p["wanted_level"]-1))
        return None
    return f"🔒 أنت في السجن يا معلم! باقي: **{fmt_seconds(int((ju-datetime.now()).total_seconds()))}**"

def player_stats_text(p):
    ge="🧑" if p["gender"]=="ولد" else "👩"
    mr="متزوج/ة 💍" if p["married_to"] else "أعزب/ة 💔"
    ga=f"{p['gang']} ({p['gang_rank']})" if p["gang"] else "لا"
    wl=f"🚨 مستوى {p['wanted_level']}" if p["wanted_level"]>0 else "✅ نظيف"
    tot=p["money"]+p["bank"]
    return f"""```ansi
{ge} {p['display_name']} | {p['char_class']} | {p['gender']}
📅 {p['age_group']} ({p['age']} سنة) | ⭐ لفل {p['level']} | XP {p['xp']:,}

💼 {p['job']} {f"| 📊 {p['job_rank']}" if p['job_rank'] else ""}
💰 كاش: {money_fmt(p['money'])} | 🏦 بنك: {money_fmt(p['bank'])}
💵 إجمالي: {money_fmt(tot)}

🏠 {p['house']} | 🚗 {p['car']}
💍 {mr} | 👥 {ga}
🚔 {wl} | 🔥 سمعة: {p['reputation']}

❤️ صحة    {progress_bar(p['health'])} {p['health']}%
🍗 جوع    {progress_bar(p['hunger'])} {p['hunger']}%
💧 عطش    {progress_bar(p['thirst'])} {p['thirst']}%
⚡ طاقة   {progress_bar(p['energy'])} {p['energy']}%
😊 سعادة  {progress_bar(p['happiness'])} {p['happiness']}%
🧼 نظافة  {progress_bar(p['hygiene'])} {p['hygiene']}%
🎮 مرح    {progress_bar(p['fun'])} {p['fun']}%
🏋️ لياقة  {progress_bar(p['fitness'])} {p['fitness']}%

💻 برمجة {p['programming_skill']} | 🎨 تصميم {p['design_skill']} | 🛡️ أمن {p['hacking_skill']}
⚔️ قتال {p['fighting_skill']} | 🥷 تخفي {p['stealth_skill']} | 🍳 طبخ {p['cooking_skill']}
📈 تجارة {p['trading_skill']} | ⚽ كورة {p['football_skill']} | 🎥 ستريم {p['streaming_skill']}
😎 كاريزما {p['charisma']} | 🚗 قيادة {p['driving_skill']}
```"""
