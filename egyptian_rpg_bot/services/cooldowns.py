# -*- coding: utf-8 -*-
"""cooldowns.py — Cooldown + interaction safety — dev by 7amo"""
from __future__ import annotations
import sqlite3, logging
from typing import Optional
import discord
from services.economy import fmt_seconds, money_fmt

log = logging.getLogger("7amo_rpg")

async def ensure_player(db, inter):
    p=await db.get_player(inter.user.id)
    if not p:
        await inter.response.send_message("❌ مش مسجل! اكتب `!ابدأ` أو `/start`.",ephemeral=True)
        return None
    return p

async def check_cooldown(db, inter, action, label=""):
    rem=await db.cooldown_remaining(inter.user.id, action)
    if rem>0:
        await inter.response.send_message(f"⏰ {label or 'لسه بدري'}! باقي: **{fmt_seconds(rem)}**",ephemeral=True)
        return True
    return False

async def check_energy(db, inter, p, needed):
    if p["energy"]<needed:
        await inter.response.send_message(f"⚡ طاقتك قليلة! محتاج **{needed}** وعندك **{p['energy']}**.\n💡 نام أو اشرب قهوة.",ephemeral=True)
        return True
    return False

async def check_money(db, inter, p, needed):
    if p["money"]<needed:
        await inter.response.send_message(f"💸 فلوسك مش كفاية! محتاج **{money_fmt(needed)}** وعندك **{money_fmt(p['money'])}**.",ephemeral=True)
        return True
    return False

async def check_jail_guard(db, inter):
    from services.economy import check_jail
    msg=await check_jail(db, inter.user.id)
    if msg:
        await inter.response.send_message(msg,ephemeral=True)
        return True
    return False

def safe_callback(func):
    """Decorator to catch errors in dynamic callbacks."""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            log.error(f"Callback error: {e}", exc_info=True)
            # Try to respond
            for a in args:
                if isinstance(a, discord.Interaction):
                    try: await a.response.send_message("⚠️ حصل خطأ! جرب تاني.",ephemeral=True)
                    except: 
                        try: await a.followup.send("⚠️ حصل خطأ!",ephemeral=True)
                        except: pass
                    break
    return wrapper
