# -*- coding: utf-8 -*-
"""شخصيات البداية + المراحل العمرية + النوع — 𝐝𝐞𝐯 𝐛𝐲 𝟕𝐚𝐦𝐨"""
from __future__ import annotations
from typing import Any

STARTER_CLASSES: dict[str, dict[str, Any]] = {
    "موظف حكومة": {
        "emoji": "👔", "desc": "بداية متوازنة. راتب ثابت وتأمين وبدلة.",
        "job": "موظف كول سنتر", "money": 800,
        "programming_skill": 5, "charisma": 6, "reputation": 5,
        "items": [("بدلة رسمية",1,"لبس"),("موبايل سامسونج",1,"أداة"),("كارنيه شغل",1,"مستند")],
    },
    "بلطجي الحتة": {
        "emoji": "💪", "desc": "ملك الحارة. القوة بتاعتك في عضلاتك.",
        "job": "عاطل", "money": 400,
        "fighting_skill": 20, "stealth_skill": 10, "charisma": 3,
        "reputation": 30, "wanted_level": 1,
        "items": [("مطواة قرن غزال",1,"سلاح"),("جاكيت جلد أسود",1,"لبس"),("سيجارة كليوباترا",5,"استهلاكي")],
    },
    "عريس الجنة": {
        "emoji": "😎", "desc": "الجدعنة والكاريزما سلاحك. كله بيحبك.",
        "job": "عاطل", "money": 900,
        "design_skill": 5, "charisma": 22, "fighting_skill": 3,
        "reputation": 18, "happiness": 110,
        "items": [("بدلة فرح إيطالي",1,"لبس"),("عطر فاخر",1,"لبس"),("جنزير ذهب (تقليد)",1,"إكسسوار"),("بوكيه ورد",1,"هدية")],
    },
    "فلاح ابن أصول": {
        "emoji": "🌾", "desc": "صحتك حديد من أكل البلد. شغّيل وجدع.",
        "job": "عامل يومية", "money": 550,
        "fighting_skill": 10, "cooking_skill": 8, "fitness": 15,
        "reputation": 8, "health": 115, "energy": 112,
        "items": [("جلباب صعيدي",1,"لبس"),("فاس",1,"أداة"),("جبنة قريش",3,"أكل"),("عيش بلدي",5,"أكل")],
    },
    "طالب جامعي": {
        "emoji": "📚", "desc": "بتذاكر وبتشتغل. المستقبل في إيدك.",
        "job": "طالب", "money": 450,
        "programming_skill": 14, "design_skill": 10, "hacking_skill": 5, "charisma": 6,
        "reputation": 3,
        "items": [("لاب توب مستعمل",1,"أداة"),("كتاب C++",1,"كتاب"),("نضارة",1,"لبس")],
    },
    "مبرمج فريلانسر": {
        "emoji": "💻", "desc": "شغلك من البيت على أبوورك. مرتاح ومرتبك دولارات.",
        "job": "فريلانسر مبتدئ", "money": 1500,
        "programming_skill": 22, "design_skill": 8, "hacking_skill": 7, "charisma": 4,
        "reputation": 6,
        "items": [("لاب توب ماك",1,"أداة"),("سماعة AirPods",1,"أداة"),("قهوة تركي",3,"مشروب")],
    },
    "لاعب كورة": {
        "emoji": "⚽", "desc": "حلمك الاحتراف والمنتخب. يا أهلي يا زمالك.",
        "job": "لاعب ناشئ", "money": 350,
        "fighting_skill": 8, "football_skill": 18, "fitness": 20, "charisma": 10,
        "reputation": 15, "health": 112, "energy": 108,
        "items": [("جزمة كورة نايكي",1,"لبس"),("كورة",1,"أداة"),("فانلة المنتخب",1,"لبس")],
    },
    "يوتيوبر/ستريمر": {
        "emoji": "🎥", "desc": "بتصور محتوى وعندك جمهور. إنفلونسر الحارة.",
        "job": "ستريمر مبتدئ", "money": 300,
        "design_skill": 12, "streaming_skill": 18, "charisma": 16,
        "reputation": 10,
        "items": [("كاميرا ويب",1,"أداة"),("مايك USB",1,"أداة"),("رينج لايت",1,"أداة")],
    },
    "شحات محترف": {
        "emoji": "🥺", "desc": "بتعرف تمثّل وتجيب فلوس من الهوا. بداية من الصفر.",
        "job": "شحات", "money": 30,
        "stealth_skill": 14, "charisma": 18, "acting_skill": 10,
        "reputation": -5,
        "items": [("شبشب مقطوع",1,"لبس"),("كوباية صاج",1,"أداة"),("جلباب ممزق",1,"لبس")],
    },
    "عاطل على القهوة": {
        "emoji": "😴", "desc": "مفيش حاجة معاك بس الأمل موجود. يلا بينا.",
        "job": "عاطل", "money": 200,
        "charisma": 2, "reputation": 0,
        "items": [("شبشب",1,"لبس"),("باكيت شيبسي",1,"أكل")],
    },
}

AGE_GROUPS: dict[str, dict[str, Any]] = {
    "طفل (12 سنة)":   {"age":12,"emoji":"👶","desc":"ممنوع من الجواز وبعض الشغل.","energy":10,"happiness":15,"work_multiplier":0.65,"xp_multiplier":1.25,"can_marry":False},
    "مراهق (16 سنة)": {"age":16,"emoji":"🧑","desc":"بتتعلم أسرع. أيام الثانوي.","energy":8,"xp_multiplier":1.15,"work_multiplier":0.80,"can_marry":False},
    "شب (23 سنة)":    {"age":23,"emoji":"🧔","desc":"أحسن توازن. لسه الدنيا قدامك.","energy":5,"xp_multiplier":1.05,"work_multiplier":1.00,"can_marry":True},
    "راجل (35 سنة)":  {"age":35,"emoji":"👨‍💼","desc":"خبرة ودخل أعلى.","reputation":12,"work_multiplier":1.12,"can_marry":True},
    "كبير (55 سنة)":  {"age":55,"emoji":"👴","desc":"الحاج وصل. سمعة كبيرة بس الطاقة أقل.","energy":-12,"reputation":30,"work_multiplier":1.22,"can_marry":True},
}

GENDERS = {
    "ولد 🧑": {"value":"ولد","emoji":"🧑","desc":"ذكر"},
    "بنت 👩": {"value":"بنت","emoji":"👩","desc":"أنثى"},
}
