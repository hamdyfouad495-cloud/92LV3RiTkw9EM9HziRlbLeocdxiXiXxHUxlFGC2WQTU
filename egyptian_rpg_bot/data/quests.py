# -*- coding: utf-8 -*-
"""المهام · الأحداث · المراهنات · السرقة · الفريلانس · الكورسات — 𝐝𝐞𝐯 𝐛𝐲 𝟕𝐚𝐦𝐨"""
from __future__ import annotations
from typing import Any

DEFAULT_QUESTS: list[dict[str,Any]] = [
    {"code":"work_1","name":"🔨 اشتغل أول يوم","target":1,"money":150,"xp":80},
    {"code":"work_10","name":"💼 اشتغل 10 مرات","target":10,"money":1200,"xp":500},
    {"code":"work_50","name":"🏆 اشتغل 50 مرة","target":50,"money":8000,"xp":3000},
    {"code":"marry_1","name":"💍 اتجوز","target":1,"money":700,"xp":250},
    {"code":"house_1","name":"🏠 اشتري بيت","target":1,"money":1500,"xp":450},
    {"code":"steal_1","name":"🔫 نفذ مهمة RPG","target":1,"money":400,"xp":150},
    {"code":"program_1","name":"💻 برمج مشروع","target":1,"money":900,"xp":300},
    {"code":"design_1","name":"🎨 صمم شغل","target":1,"money":650,"xp":220},
    {"code":"gang_1","name":"👥 انضم لعصابة","target":1,"money":850,"xp":350},
    {"code":"level_10","name":"⭐ وصل لفل 10","target":10,"money":5000,"xp":2000},
    {"code":"level_25","name":"🌟 وصل لفل 25","target":25,"money":25000,"xp":10000},
    {"code":"car_1","name":"🚗 اشتري عربية","target":1,"money":2200,"xp":800},
    {"code":"bank_rob_1","name":"🏦 سرقة بنك RPG","target":1,"money":10000,"xp":5000},
    {"code":"course_3","name":"📚 3 كورسات","target":3,"money":1800,"xp":700},
    {"code":"business_1","name":"🏪 افتح بزنس","target":1,"money":3000,"xp":1200},
    {"code":"eat_20","name":"🍗 كل 20 مرة","target":20,"money":500,"xp":200},
    {"code":"gamble_win_5","name":"🎰 اكسب 5 مراهنات","target":5,"money":3000,"xp":1000},
    {"code":"football_1","name":"⚽ العب ماتش","target":1,"money":600,"xp":200},
    {"code":"stream_1","name":"🎥 أول لايف","target":1,"money":500,"xp":180},
    {"code":"rich_100k","name":"💰 اجمع 100k","target":100000,"money":15000,"xp":6000},
    {"code":"reputation_100","name":"🔥 سمعة 100","target":100,"money":5000,"xp":2500},
    {"code":"daily_7","name":"📅 7 أيام متتالية","target":7,"money":2000,"xp":800},
    {"code":"book_5","name":"📖 اقرا 5 كتب","target":5,"money":1000,"xp":400},
    {"code":"pvp_win_3","name":"⚔️ اكسب 3 معارك","target":3,"money":2500,"xp":900},
    {"code":"transfer_1","name":"💸 حوّل فلوس","target":1,"money":300,"xp":100},
    {"code":"pet_1","name":"🐾 اشتري حيوان أليف","target":1,"money":500,"xp":200},
    {"code":"travel_1","name":"✈️ سافر مدينة","target":1,"money":800,"xp":300},
]

RANDOM_EVENTS: list[dict[str,Any]] = [
    {"name":"فرح في الحارة 🎉","desc":"اتعزمت على فرح. «الفرح فرحنا والعريس أبو أحمد»","happiness":14,"hunger":10},
    {"name":"مواصلات زحمة 🚌","desc":"وقفت في الزحمة ساعة ونص. «مصر ما فيهاش مواصلات»","energy":-12,"happiness":-6},
    {"name":"بقشيش كريم 💵","desc":"عميل ادالك بقشيش محترم. «ربنا يبارك فيك»","money":250,"reputation":3},
    {"name":"دور برد 🤧","desc":"خدت برد من التكييف. «اللي يلعب بالنار يتحرق»","health":-10,"energy":-7},
    {"name":"ترند سوشيال 📱","desc":"بوست ليك ضرب ترند! «إنت فين يا عم من زمان؟»","reputation":15,"happiness":10},
    {"name":"مخالفة مرور 🚔","desc":"اتسحبت منك فلوس. «اللي بيسوق في مصر بيصبر»","money":-180,"happiness":-5},
    {"name":"فلوس في البنطلون 💰","desc":"لقيت 300ج في جيب البنطلون القديم!","money":300,"happiness":6},
    {"name":"نشّال المترو 😡","desc":"حد نشلك في المترو. «خلّي بالك من جيبك»","money":-120,"happiness":-10},
    {"name":"أكل ست الكل 🍲","desc":"أمك عملت محشي وملوخية. «ست الكل»","hunger":35,"happiness":25,"health":6},
    {"name":"الموبايل وقع 📱💥","desc":"وقع على السلم وشرخ. «يا خسارة»","money":-350,"happiness":-12},
    {"name":"قابلت حد مهم 🤝","desc":"اتعرفت على رجل أعمال في مناسبة.","reputation":10,"charisma":1},
    {"name":"فاتورة كهربا 💡","desc":"فاتورة كهربا فلكية. «كهربا مصر غالية»","money":-250,"happiness":-4},
    {"name":"شغلانة جانبية 🔧","desc":"حد طلب منك شغلانة صغيرة. «الرزق على الله»","money":350,"xp":25},
    {"name":"عزومة بيتزا 🍕","desc":"صاحبك عزمك. «الصحاب يوم الضيق»","hunger":28,"happiness":12},
    {"name":"ضربة شمس ☀️","desc":"قعدت في الشمس كتير. «حر مصر»","health":-6,"energy":-10},
    {"name":"يوم محظوظ 🍀","desc":"يومك زي الفل! «الدنيا بخير»","happiness":18,"energy":10,"money":120},
    {"name":"خناقة ركنة 👊","desc":"اتخانقت مع حد على ركنة. «ده مكاني أنا»","health":-5,"happiness":-6,"fighting_skill":1},
    {"name":"كوبون خصم 🏷️","desc":"لقيت كوبون 50%. «الفرصة مبتتكررش»","money":60,"happiness":5},
    {"name":"قطة اتبنتها 🐱","desc":"قطة صغيرة لقيتها في الشارع. «الرحمة»","happiness":15},
    {"name":"فوز المنتخب ⚽","desc":"مصر كسبت! الشارع كله بيزمّر!","happiness":25,"fun":20},
]

EGYPTIAN_JOKES = [
    "ليه الفول بيروح الجامعة؟ عشان يبقى فول مدمّس! 😂",
    "واحد راح يشتري ملوخية، البياع قاله: مفروم ولا ورق؟ قاله: لا كاش! 💰😂",
    "واحد قال لصاحبه: أنا بحلم إني مدير. صاحبه: وأنا بحلم إني موظف! 😂",
    "ليه المصري ميخلصش أكله؟ عشان في حد جاي ورا! 🍽😂",
    "واحد سأل صاحبه: إنت فين؟ قاله: قاعد ع القهوة. قاله: وأنا معاك! ☕😂",
    "مصري في السوبر ماركت: عندكم جبنة مستوردة؟ البياع: لا بس عندنا جبنة مسافرة! ✈️😂",
    "واحد قال لأبوه: عايز أبقى مبرمج. أبوه: ذاكر! هو: لا عايز أبقى مبرمج وبس! 💻😂",
    "دكتور قال للمريض: عندك ضغط عالي. المريض: أكيد! ده أنا في مصر! 🏥😂",
    "واحد اتصل بصاحبه: أنت فين؟ قاله: أنا في التحرير! قاله: تحرير إيه ده؟ قاله: تحرير محضر! 👮😂",
]

GAMBLING_GAMES = {
    "صقعة (كوتشينة)":   {"emoji":"🃏","min_bet":50,"max_bet":50000,"desc":"العب صقعة مع الديلر."},
    "طاولة (نرد)":       {"emoji":"🎲","min_bet":50,"max_bet":30000,"desc":"ارمي النرد. 7 أو 11."},
    "كوتشينة عالي/واطي": {"emoji":"🂡","min_bet":25,"max_bet":20000,"desc":"احزر الكارت."},
    "سلوتس مصري":        {"emoji":"🎰","min_bet":10,"max_bet":100000,"desc":"ماكينة الحظ."},
    "لعبة الكوبايات":    {"emoji":"🥤","min_bet":50,"max_bet":10000,"desc":"فين الكورة؟"},
}

STEAL_TARGETS: dict[str,dict[str,dict[str,Any]]] = {
    "سهل 🟢": {
        "عربية فول":     {"min_loot":25,"max_loot":100,"risk":10,"xp":18,"req_stealth":0,"energy":10},
        "كشك سجاير":    {"min_loot":40,"max_loot":180,"risk":14,"xp":28,"req_stealth":0,"energy":12},
        "عجلة مربوطة":  {"min_loot":80,"max_loot":350,"risk":18,"xp":38,"req_stealth":3,"energy":14},
        "محل بقالة":    {"min_loot":60,"max_loot":250,"risk":16,"xp":32,"req_stealth":0,"energy":16},
        "دراجة":        {"min_loot":120,"max_loot":480,"risk":22,"xp":42,"req_stealth":5,"energy":18},
        "محل ملابس":    {"min_loot":200,"max_loot":800,"risk":28,"xp":55,"req_stealth":10,"energy":22},
    },
    "متوسط 🟡": {
        "سوبر ماركت":   {"min_loot":500,"max_loot":2000,"risk":40,"xp":110,"req_stealth":18,"energy":30},
        "صيدلية":       {"min_loot":350,"max_loot":1400,"risk":36,"xp":85,"req_stealth":14,"energy":28},
        "محل ذهب":      {"min_loot":1200,"max_loot":5000,"risk":52,"xp":170,"req_stealth":28,"energy":38},
        "فيلا":         {"min_loot":2000,"max_loot":10000,"risk":56,"xp":210,"req_stealth":38,"energy":42},
        "محل موبايلات": {"min_loot":1600,"max_loot":7000,"risk":48,"xp":150,"req_stealth":22,"energy":34},
    },
    "صعب 🔴": {
        "بنك صغير":     {"min_loot":6000,"max_loot":25000,"risk":70,"xp":550,"req_stealth":48,"energy":52},
        "شركة كبيرة":   {"min_loot":10000,"max_loot":50000,"risk":74,"xp":800,"req_stealth":58,"energy":58},
        "بنك أهلي":     {"min_loot":50000,"max_loot":200000,"risk":86,"xp":1600,"req_stealth":78,"energy":72},
        "مستودع أموال":  {"min_loot":100000,"max_loot":450000,"risk":90,"xp":3000,"req_stealth":88,"energy":80},
        "خزنة القصر":   {"min_loot":400000,"max_loot":1500000,"risk":96,"xp":7000,"req_stealth":96,"energy":92},
    },
}

PROGRAMMING_PROJECTS = {
    "سهل":{"موقع بسيط":{"time":2,"earnings":550,"xp":55,"req_skill":0,"complexity":1},"بوت تليجرام":{"time":3,"earnings":1200,"xp":100,"req_skill":12,"complexity":2},"سكريبت أتمتة":{"time":2,"earnings":700,"xp":70,"req_skill":5,"complexity":1}},
    "متوسط":{"متجر إلكتروني":{"time":6,"earnings":3200,"xp":220,"req_skill":28,"complexity":5},"تطبيق موبايل":{"time":8,"earnings":5500,"xp":320,"req_skill":40,"complexity":7},"بوت ديسكورد":{"time":5,"earnings":4000,"xp":260,"req_skill":32,"complexity":5}},
    "صعب":{"نظام AI":{"time":14,"earnings":22000,"xp":850,"req_skill":68,"complexity":10},"بلوكتشين":{"time":18,"earnings":50000,"xp":1500,"req_skill":80,"complexity":10},"نظام أمني":{"time":22,"earnings":100000,"xp":2000,"req_skill":88,"complexity":10}},
}
DESIGN_PROJECTS = {
    "سهل":{"شعار بسيط":{"time":1,"earnings":300,"xp":30,"req_skill":0,"quality":1},"بوستر":{"time":2,"earnings":550,"xp":55,"req_skill":8,"quality":2},"ستوري إنستا":{"time":1,"earnings":250,"xp":25,"req_skill":0,"quality":1}},
    "متوسط":{"هوية بصرية":{"time":5,"earnings":2600,"xp":160,"req_skill":28,"quality":5},"تصميم موقع":{"time":6,"earnings":4000,"xp":220,"req_skill":38,"quality":6},"موشن جرافيك":{"time":7,"earnings":6500,"xp":310,"req_skill":48,"quality":7}},
    "صعب":{"تصميم لعبة":{"time":14,"earnings":15000,"xp":650,"req_skill":68,"quality":9},"3D Rendering":{"time":18,"earnings":30000,"xp":1050,"req_skill":78,"quality":10},"فيلم أنيميشن":{"time":22,"earnings":50000,"xp":1600,"req_skill":88,"quality":10}},
}
HACKING_TARGETS = {
    "سهل":{"CTF Challenge":{"time":2,"earnings":800,"xp":80,"risk":6,"req_skill":5},"تأمين شبكة محل":{"time":2,"earnings":1100,"xp":100,"risk":8,"req_skill":10}},
    "متوسط":{"تدقيق أمني شركة":{"time":6,"earnings":6000,"xp":340,"risk":20,"req_skill":38},"Bug Bounty":{"time":7,"earnings":11000,"xp":440,"risk":18,"req_skill":45}},
    "صعب":{"تأمين بنية تحتية":{"time":14,"earnings":88000,"xp":1800,"risk":42,"req_skill":78},"مسابقة أمن عالمية":{"time":22,"earnings":450000,"xp":7500,"risk":32,"req_skill":95}},
}

COURSES = {
    "برمجة مبتدئ 💻":    {"skill":"programming_skill","gain":7,"price":700,"xp":75,"hours":2},
    "برمجة متقدم 🖥️":   {"skill":"programming_skill","gain":14,"price":5500,"xp":210,"hours":5},
    "تصميم مبتدئ 🎨":    {"skill":"design_skill","gain":7,"price":600,"xp":65,"hours":2},
    "تصميم متقدم 🖌️":   {"skill":"design_skill","gain":14,"price":5000,"xp":190,"hours":5},
    "أمن سيبراني 🛡️":    {"skill":"hacking_skill","gain":8,"price":2200,"xp":130,"hours":3},
    "قتال ودفاع 🥊":     {"skill":"fighting_skill","gain":8,"price":1000,"xp":85,"hours":2},
    "تخفي وتمثيل 🥷":    {"skill":"stealth_skill","gain":8,"price":1300,"xp":95,"hours":2},
    "طبخ مصري 🍳":       {"skill":"cooking_skill","gain":8,"price":500,"xp":60,"hours":2},
    "تجارة وبزنس 📈":    {"skill":"trading_skill","gain":8,"price":2800,"xp":115,"hours":3},
    "كورة قدم ⚽":       {"skill":"football_skill","gain":8,"price":900,"xp":75,"hours":2},
    "ستريمنج 🎥":        {"skill":"streaming_skill","gain":8,"price":1300,"xp":85,"hours":2},
    "قيادة سيارات 🚗":   {"skill":"driving_skill","gain":10,"price":1800,"xp":95,"hours":3},
    "كاريزما وتواصل 😎": {"skill":"charisma","gain":5,"price":1600,"xp":85,"hours":2},
}

GANGS = {
    "الأنوف السودا":  {"territory":"بولاق","req_reputation":0,"emoji":"👃"},
    "عيال المعادي":   {"territory":"المعادي","req_reputation":50,"emoji":"🔥"},
    "العيال الصعايدة": {"territory":"السيدة زينب","req_reputation":100,"emoji":"⚡"},
    "أسود شبرا":      {"territory":"شبرا","req_reputation":200,"emoji":"🦁"},
    "الزمالكاوية":    {"territory":"الزمالك","req_reputation":300,"emoji":"⚪"},
    "تيجان التجمع":   {"territory":"التجمع الخامس","req_reputation":500,"emoji":"👑"},
    "ذئاب مدينة نصر": {"territory":"مدينة نصر","req_reputation":800,"emoji":"🐺"},
    "القاهرة الفاطمية":{"territory":"الحسين","req_reputation":1000,"emoji":"🏛️"},
}

PETS = {
    "قطة مصري 🐱":     {"price":400,"happiness_daily":4,"desc":"ميو ميو. بتاخد أكل ورعاية."},
    "كلب بلدي 🐕":     {"price":600,"happiness_daily":5,"security":8,"desc":"حارس أمين."},
    "عصفور كناري 🐦":  {"price":250,"happiness_daily":3,"desc":"بيغنّي الصبح."},
    "سمك زينة 🐟":     {"price":150,"happiness_daily":2,"desc":"مريح للأعصاب."},
    "حصان عربي 🐴":    {"price":12000,"happiness_daily":8,"speed":15,"reputation":12,"desc":"للفرسان."},
    "جمل 🐫":          {"price":5000,"happiness_daily":5,"reputation":8,"desc":"سفينة الصحراء."},
}

TRAVEL_CITIES = {
    "القاهرة 🏙️":     {"price":0,"desc":"العاصمة. كل حاجة هنا.","bonus":"xp_multiplier:1.0"},
    "إسكندرية 🌊":    {"price":200,"desc":"عروس البحر. «إسكندرية يا بهية»","bonus":"happiness:10"},
    "الأقصر 🏛️":      {"price":350,"desc":"أرض المعابد. «الحضارة الفرعونية»","bonus":"reputation:5"},
    "أسوان ☀️":       {"price":400,"desc":"النيل والنوبة. «بلاد الذهب»","bonus":"energy:15"},
    "شرم الشيخ 🏖️":  {"price":600,"desc":"مدينة السلام. سياحة وغوص.","bonus":"fun:20"},
    "الغردقة 🐠":     {"price":500,"desc":"البحر الأحمر. شواطئ ومنتجعات.","bonus":"happiness:15"},
}
