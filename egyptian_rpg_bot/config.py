# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════╗
║  ⚙️  config.py — إعدادات البوت الرئيسية                      ║
║  𝐝𝐞𝐯 𝐛𝐲 𝟕𝐚𝐦𝐨 © 2026                                        ║
╚═══════════════════════════════════════════════════════════════╝
"""
from __future__ import annotations
import os

BOT_TOKEN     = os.getenv("DISCORD_TOKEN", "YOUR_BOT_TOKEN_HERE")
PREFIX        = os.getenv("BOT_PREFIX", "!")
DB_FILE       = os.getenv("RPG_DB_FILE", "roleplay7amo.db")
OWNER_BRAND   = "𝐝𝐞𝐯 𝐛𝐲 𝟕𝐚𝐦𝐨 © 2026"
BRAND_SHORT   = "7amo RPG"

COLOR_GOLD    = 0xF1C40F
COLOR_RED     = 0xE74C3C
COLOR_GREEN   = 0x2ECC71
COLOR_BLUE    = 0x3498DB
COLOR_PURPLE  = 0x9B59B6
COLOR_ORANGE  = 0xE67E22
COLOR_PINK    = 0xE91E63
COLOR_DARK    = 0x2C3E50
COLOR_CYAN    = 0x1ABC9C

STAT_FIELDS = {
    "health", "hunger", "thirst", "energy", "happiness",
    "hygiene", "fun", "fitness",
}
SKILL_FIELDS = {
    "programming_skill", "design_skill", "hacking_skill",
    "fighting_skill", "stealth_skill", "cooking_skill",
    "trading_skill", "football_skill", "streaming_skill",
    "music_skill", "acting_skill", "driving_skill", "charisma",
}
PLAYER_UPDATE_FIELDS = {
    "username","display_name","char_class","gender","age_group","age",
    "job","job_xp","job_rank","money","bank","crypto",
    "health","hunger","thirst","energy","happiness","hygiene","fun","fitness",
    "xp","level","house","car","neighborhood",
    "married_to","gang","gang_rank",
    *SKILL_FIELDS,
    "reputation","wanted_level","jail_until",
    "daily_streak","total_earnings","total_spent",
    "updated_at",
}

# ── أمثال شعبية تظهر عشوائي ──
AMTHAL = [
    "اللي يحسب الحسابات في الهنا يبات 🧠",
    "القرش الأبيض ينفع في اليوم الأسود 💰",
    "اللي ماياخدش من قلة أدبه ياخد من كتر ضربه 💪",
    "ابن الوز عوّام 🦆",
    "الحي أبقى من الميت 😅",
    "اصرف ما في الجيب يأتيك ما في الغيب 🤲",
    "الصنعة في الإيد أمان 🔧",
    "يا بخت من وفّق بين القلب والعقل ❤️",
    "العين ما تعلاش على الحاجب 👁️",
    "اللي يعيش ياما يشوف 👀",
    "جبر الخواطر على الله 🤝",
    "ربنا مع الصابرين 🙏",
    "الجار قبل الدار 🏠",
    "الأقارب عقارب 🦂",
    "على قد لحافك مد رجليك 🛏️",
    "امشي في جنازة ولا تمشي في جوازة 💀",
    "الحلو مايكملش 😔",
    "اللي بيته من إزاز مايحدفش الناس بالطوب 🏠",
    "اللي يطلع من داره يتقل مقداره 🚶",
    "الغالي تمنه فيه 💎",
]

# ── رسائل ترحيب ──
WELCOME_MSGS = [
    "يا هلا يا هلا! أهلاً بيك في مصر يا معلم! 🇪🇬",
    "نوّرت يا باشا! يلا نبدأ الرحلة! 🎮",
    "اتفضل يا كبير! مصر أم الدنيا مستنياك! 🏛️",
]
