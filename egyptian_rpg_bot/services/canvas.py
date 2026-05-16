# -*- coding: utf-8 -*-
"""canvas.py — صور Canvas احترافية — dev by 7amo"""
from __future__ import annotations
import io, sqlite3, textwrap
from PIL import Image, ImageDraw, ImageFont
from config import OWNER_BRAND
from services.economy import progress_bar, money_fmt

def load_font(size=24, bold=False):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "arial.ttf"]:
        try: return ImageFont.truetype(p, size=size)
        except: continue
    return ImageFont.load_default()

def _gradient(draw, w, h, c1=(12,18,32), c2=(28,38,62)):
    for y in range(h):
        r=y/h
        draw.line([(0,y),(w,y)], fill=(int(c1[0]+(c2[0]-c1[0])*r), int(c1[1]+(c2[1]-c1[1])*r), int(c1[2]+(c2[2]-c1[2])*r)))

async def generate_result_image(title, lines, accent="#e94560", width=920, height=0):
    lh=54; h=height or max(200, 155+len(lines)*lh+55)
    img=Image.new("RGB",(width,h)); draw=ImageDraw.Draw(img); _gradient(draw,width,h)
    ft=load_font(36,True); fl=load_font(22); fs=load_font(16)
    draw.rounded_rectangle((22,18,width-22,95),radius=16,fill="#0f172a",outline=accent,width=3)
    draw.text((width//2,56),title,fill=accent,anchor="mm",font=ft)
    # dev by 7amo watermark
    draw.text((width-30,56),"7amo",fill="#ffffff40",anchor="rm",font=fs)
    y=118
    for i,line in enumerate(lines[:11]):
        bg="#1e293b" if i%2==0 else "#1a2332"
        draw.rounded_rectangle((40,y-5,width-40,y+38),radius=9,fill=bg,outline="#334155",width=1)
        draw.text((width-60,y+16),str(line),fill="#f1f5f9",anchor="rm",font=fl)
        y+=lh
    draw.text((width//2,h-25),f"⚡ {OWNER_BRAND}",fill="#64748b",anchor="mm",font=fs)
    buf=io.BytesIO(); img.save(buf,format="PNG",optimize=True); buf.seek(0); return buf

async def generate_profile_image(p):
    ge="🧑" if p["gender"]=="ولد" else "👩"
    tot=p["money"]+p["bank"]
    lines=[
        f"{ge} {p['char_class']} | {p['age_group']} ({p['age']})",
        f"💼 {p['job']} | ⭐ لفل {p['level']} | XP {p['xp']:,}",
        f"💰 كاش: {money_fmt(p['money'])} | 🏦 بنك: {money_fmt(p['bank'])}",
        f"💵 إجمالي: {money_fmt(tot)}",
        f"🏠 {p['house']} | 🚗 {p['car']}",
        f"❤️{p['health']}% 🍗{p['hunger']}% 💧{p['thirst']}% ⚡{p['energy']}%",
        f"😊{p['happiness']}% 🧼{p['hygiene']}% 🎮{p['fun']}% 🏋️{p['fitness']}%",
        f"💻{p['programming_skill']} 🎨{p['design_skill']} 🛡️{p['hacking_skill']} ⚔️{p['fighting_skill']}",
        f"⚽{p['football_skill']} 🎥{p['streaming_skill']} 😎{p['charisma']} 🔥سمعة {p['reputation']}",
    ]
    accent="#f1c40f" if p["gender"]=="ولد" else "#e91e63"
    return await generate_result_image(f"🎭 {p['display_name']}",lines,accent=accent,height=680)

async def generate_gamble_image(game,result,bet,payout,won):
    accent="#2ecc71" if won else "#e74c3c"
    lines=[f"🎮 {game}",f"💰 الرهان: {money_fmt(bet)}",f"🎯 {result}",
           f"{'💵 كسبت' if won else '💸 خسرت'}: {money_fmt(payout)}"]
    return await generate_result_image("🎰 كسبت!" if won else "😢 خسارة",lines,accent)

async def generate_business_image(biz_name,sign,income):
    lines=[f"🏪 {biz_name}",f"📋 {sign}",f"💰 الدخل: {money_fmt(income)}/6 ساعات"]
    return await generate_result_image("🏪 البزنس بتاعك",lines,"#f1c40f")
