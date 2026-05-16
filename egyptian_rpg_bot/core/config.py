# -*- coding: utf-8 -*-
"""
Core configuration file for Egyptian RPG Bot
Stores all constants, colors, classes, and game data
"""

import os
from enum import Enum

# ════════════════════════════════════════════════════════════════
# BOT CONFIGURATION
# ════════════════════════════════════════════════════════════════

BOT_TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_BOT_TOKEN_HERE")
PREFIX = os.getenv("BOT_PREFIX", "!")
DB_FILE = os.getenv("RPG_DB_FILE", "roleplay_egypt.db")
OWNER_BRAND = "𝐝𝐞𝐯 𝐛𝐲 𝟕𝐚𝐦𝐨 © 2026"
BRAND_SHORT = "7amo RPG"

# ════════════════════════════════════════════════════════════════
# COLORS (Discord Embeds)
# ════════════════════════════════════════════════════════════════

class Colors(Enum):
    GOLD = 0xF1C40F
    RED = 0xE74C3C
    GREEN = 0x2ECC71
    BLUE = 0x3498DB
    PURPLE = 0x9B59B6
    ORANGE = 0xE67E22
    PINK = 0xE91E63
    DARK = 0x2C3E50
    CYAN = 0x1ABC9C
    YELLOW = 0xF39C12
    LIME = 0x27AE60
    NAVY = 0x34495E

# Shortcuts
COLOR_GOLD = Colors.GOLD.value
COLOR_RED = Colors.RED.value
COLOR_GREEN = Colors.GREEN.value
COLOR_BLUE = Colors.BLUE.value
COLOR_PURPLE = Colors.PURPLE.value
COLOR_ORANGE = Colors.ORANGE.value

# ════════════════════════════════════════════════════════════════
# STARTER CLASSES - Initial character stats
# ════════════════════════════════════════════════════════════════

STARTER_CLASSES = {
    "موظف": {
        "emoji": "👔",
        "job": "موظف",
        "money": 1000,
        "health": 0,
        "energy": 0,
        "happiness": 5,
        "fitness": 20,
        "charisma": 8,
        "reputation": 5,
        "trading_skill": 5,
    },
    "بلطجي": {
        "emoji": "💪",
        "job": "بلطجي",
        "money": 500,
        "health": 20,
        "energy": 10,
        "happiness": 0,
        "fitness": 40,
        "fighting_skill": 20,
        "stealth_skill": 10,
        "charisma": 3,
        "reputation": 15,
    },
    "عريس الجنة": {
        "emoji": "😎",
        "job": "عاطل",
        "money": 200,
        "health": 0,
        "energy": -5,
        "happiness": 30,
        "fitness": 10,
        "charisma": 15,
        "reputation": 0,
    },
    "فلاح": {
        "emoji": "🌾",
        "job": "فلاح",
        "money": 300,
        "health": 10,
        "energy": 5,
        "fitness": 30,
        "reputation": 5,
    },
    "طالب": {
        "emoji": "📚",
        "job": "طالب",
        "money": 100,
        "health": 0,
        "energy": -10,
        "happiness": 10,
        "fitness": 15,
        "programming_skill": 5,
        "charisma": 7,
    },
    "مبرمج": {
        "emoji": "💻",
        "job": "مبرمج",
        "money": 1500,
        "health": -5,
        "energy": -15,
        "happiness": 0,
        "fitness": 10,
        "programming_skill": 25,
        "hacking_skill": 15,
        "charisma": 5,
    },
    "لاعب كورة": {
        "emoji": "⚽",
        "job": "لاعب كورة",
        "money": 800,
        "health": 15,
        "energy": 10,
        "happiness": 20,
        "fitness": 50,
        "football_skill": 30,
        "charisma": 10,
        "reputation": 10,
    },
    "ستريمر": {
        "emoji": "🎥",
        "job": "ستريمر",
        "money": 600,
        "health": -10,
        "energy": -20,
        "happiness": 25,
        "fitness": 5,
        "streaming_skill": 20,
        "charisma": 12,
        "music_skill": 10,
    },
    "شحات": {
        "emoji": "🥺",
        "job": "شحات",
        "money": 50,
        "health": -20,
        "energy": -10,
        "happiness": -20,
        "fitness": 5,
        "charisma": 3,
        "reputation": -10,
    },
    "عاطل": {
        "emoji": "😴",
        "job": "عاطل",
        "money": 200,
        "health": 0,
        "energy": 0,
        "happiness": -5,
        "fitness": 5,
        "reputation": -5,
    },
}

# ════════════════════════════════════════════════════════════════
# AGE GROUPS - Age-based bonuses
# ════════════════════════════════════════════════════════════════

AGE_GROUPS = {
    "صغير": {
        "age": 15,
        "health": -5,
        "energy": 10,
        "can_marry": False,
        "can_work": False,
        "bonus_xp": 1.1,
    },
    "شاب": {
        "age": 23,
        "health": 0,
        "energy": 5,
        "can_marry": True,
        "can_work": True,
        "bonus_xp": 1.0,
    },
    "كهل": {
        "age": 35,
        "health": 5,
        "energy": -5,
        "can_marry": True,
        "can_work": True,
        "bonus_xp": 0.9,
    },
    "عجوز": {
        "age": 55,
        "health": 10,
        "energy": -15,
        "can_marry": True,
        "can_work": True,
        "bonus_xp": 0.7,
    },
}

# ════════════════════════════════════════════════════════════════
# NEIGHBORHOODS - Cairo areas
# ════════════════════════════════════════════════════════════════

NEIGHBORHOODS = {
    "بولاق": {"emoji": "🏘️", "price_modifier": 1.0, "danger": 3, "vibes": "شعبي"},
    "جاردن سيتي": {"emoji": "🏰", "price_modifier": 1.5, "danger": 1, "vibes": "فاخر"},
    "عين شمس": {"emoji": "🏢", "price_modifier": 1.1, "danger": 4, "vibes": "سكني"},
    "الزمالك": {"emoji": "🌳", "price_modifier": 1.4, "danger": 1, "vibes": "هادئ"},
    "الجيزة": {"emoji": "🏛️", "price_modifier": 1.0, "danger": 2, "vibes": "وسط"},
    "مصر الجديدة": {"emoji": "🏙️", "price_modifier": 1.2, "danger": 2, "vibes": "عصري"},
    "عباسية": {"emoji": "🎪", "price_modifier": 1.0, "danger": 5, "vibes": "جريء"},
    "حلوان": {"emoji": "🏭", "price_modifier": 0.8, "danger": 4, "vibes": "صناعي"},
}

# ════════════════════════════════════════════════════════════════
# JOBS & CAREERS
# ════════════════════════════════════════════════════════════════

JOBS = {
    "موظف": {
        "emoji": "👔",
        "salary_min": 500,
        "salary_max": 1500,
        "energy_cost": 20,
        "required_level": 1,
        "skills": ["trading_skill"],
    },
    "بلطجي": {
        "emoji": "💪",
        "salary_min": 300,
        "salary_max": 1200,
        "energy_cost": 30,
        "required_level": 5,
        "skills": ["fighting_skill"],
        "danger": True,
    },
    "مبرمج": {
        "emoji": "💻",
        "salary_min": 800,
        "salary_max": 3000,
        "energy_cost": 25,
        "required_level": 10,
        "skills": ["programming_skill"],
    },
    "ستريمر": {
        "emoji": "🎥",
        "salary_min": 200,
        "salary_max": 2000,
        "energy_cost": 15,
        "required_level": 1,
        "skills": ["streaming_skill", "charisma"],
    },
    "فلاح": {
        "emoji": "🌾",
        "salary_min": 100,
        "salary_max": 500,
        "energy_cost": 35,
        "required_level": 1,
        "skills": [],
    },
}

# ════════════════════════════════════════════════════════════════
# DATABASE FIELDS CONFIGURATION
# ════════════════════════════════════════════════════════════════

STAT_FIELDS = {
    "health", "hunger", "thirst", "energy", 
    "happiness", "hygiene", "fun", "fitness",
}

SKILL_FIELDS = {
    "programming_skill", "design_skill", "hacking_skill",
    "fighting_skill", "stealth_skill", "cooking_skill",
    "trading_skill", "football_skill", "streaming_skill",
    "music_skill", "acting_skill", "driving_skill", "charisma",
}

PLAYER_UPDATE_FIELDS = {
    "username", "display_name", "char_class", "gender", "age_group", "age",
    "job", "job_xp", "job_rank", "job_level",
    "money", "bank", "crypto",
    "health", "hunger", "thirst", "energy", "happiness", "hygiene", "fun", "fitness",
    "xp", "level", "house", "car", "neighborhood",
    "married_to", "gang", "gang_rank",
    *SKILL_FIELDS,
    "reputation", "wanted_level", "jail_until",
    "daily_streak", "total_earnings", "total_spent",
    "updated_at", "last_daily"
}

# ════════════════════════════════════════════════════════════════
# EGYPTIAN PROVERBS & SAYINGS
# ════════════════════════════════════════════════════════════════

EGYPTIAN_PROVERBS = [
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
    "الجدعنة رزق 💸",
    "مفيش فصال 🤝",
    "الكاش يكسب 💳",
    "سيبك من المنظر 🎭",
    "خدها نصيحة 📝",
    "البيع نقدًا 💵",
    "التصوير ممنوع 📸",
    "اسأل مجرب 🧠",
    "عيش وملح 🍞",
    "الرجولة أفعال 💪",
    "لو معاك قرش تسوى قرش 💡",
    "القهوة للجدعان ☕",
    "محدش بياكلها بالساهل 🏆",
    "احنا ولاد ناس 👑",
    "ادفع الأول 💰",
    "مفيش ديون 🚫",
    "خليك جدع 🔥",
    "متجيش تعيط 👶",
    "ربح وخسارة 📊",
    "كل خير 🤐",
    "ماتقول أبدًا 🤫",
    "الحب أعمى 👁️",
    "الموت أحسن من الهوان 💀",
    "الصاحب ساحب 👥",
    "المال لا يشتري السعادة 💸",
    "الصبر مفتاح الفرج ⏰",
]

# ════════════════════════════════════════════════════════════════
# WELCOME MESSAGES
# ════════════════════════════════════════════════════════════════

WELCOME_MESSAGES = [
    "يا هلا يا هلا! أهلاً بيك في مصر يا معلم! 🇪🇬",
    "نوّرت يا باشا! يلا نبدأ الرحلة! 🎮",
    "اتفضل يا كبير! مصر أم الدنيا مستنياك! 🏛️",
    "أهلاً بيك في جنة الدنيا! 😎",
    "يلا نشتغل! في فلوس تنتظرك! 💰",
    "نوّرت يا فندم! 🎩",
    "أهلاً وسهلاً يا صديقي! 🤝",
]

# ═════════════════��══════════════════════════════════════════════
# LEVELING CONFIGURATION
# ════════════════════════════════════════════════════════════════

XP_PER_LEVEL = 1000
LEVEL_CAP = 100

def get_xp_for_level(level: int) -> int:
    """Calculate total XP needed for a level"""
    return level * XP_PER_LEVEL

# ════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════════

def clamp(value: float, minimum: float = 0, maximum: float = 100) -> int:
    """Clamp value between min and max"""
    return max(minimum, min(maximum, int(value)))

def money_format(amount: int) -> str:
    """Format money with commas"""
    return f"{amount:,}"
