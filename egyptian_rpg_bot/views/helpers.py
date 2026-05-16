# -*- coding: utf-8 -*-
"""helpers.py — embed builder — dev by 7amo"""
from datetime import datetime
import discord
from config import OWNER_BRAND, COLOR_GOLD

def make_embed(title="",desc="",color=COLOR_GOLD):
    e=discord.Embed(title=title,description=desc,color=color,timestamp=datetime.now())
    e.set_footer(text=f"⚡ {OWNER_BRAND}")
    return e
