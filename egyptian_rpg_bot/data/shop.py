# -*- coding: utf-8 -*-
"""المتاجر والعقارات والسيارات — 𝐝𝐞𝐯 𝐛𝐲 𝟕𝐚𝐦𝐨"""
from __future__ import annotations
from typing import Any

FOODS: dict[str,dict[str,Any]] = {
    "فول مدمس":        {"price":12,"hunger":22,"health":5,"happiness":6,"emoji":"🫘","desc":"أصل الفطار. بالزيت الحار والليمونة."},
    "طعمية (فلافل)":   {"price":8, "hunger":16,"health":3,"happiness":5,"emoji":"🧆","desc":"سخنة ومقرمشة من عم حسن."},
    "سندوتش فول وطعمية":{"price":10,"hunger":20,"health":4,"happiness":8,"emoji":"🥙","desc":"سندوتش الغلابة اللذيذ."},
    "كشري":            {"price":28,"hunger":40,"health":8,"happiness":20,"emoji":"🍝","desc":"دقة وشطة ودمعة الست. «مالوش حل»"},
    "ملوخية بالأرانب":  {"price":60,"hunger":45,"health":18,"happiness":18,"emoji":"🥘","desc":"بالتقلية. «ست الكل عملتها»"},
    "كبدة إسكندراني":  {"price":55,"hunger":36,"health":8,"happiness":24,"emoji":"🥩","desc":"حارقة وعلى النار. من عم فتحي."},
    "شاورما لحمة":     {"price":70,"hunger":44,"health":4,"happiness":30,"emoji":"🌯","desc":"ثومية زيادة يا معلم."},
    "محشي ورق عنب":    {"price":85,"hunger":48,"health":16,"happiness":26,"emoji":"🫔","desc":"ورق عنب وكرنب. «أكلة ملوك»"},
    "كفتة مشوية":      {"price":115,"hunger":55,"health":22,"happiness":35,"emoji":"🍖","desc":"على الفحم مع الطحينة."},
    "فتة عيد":         {"price":95,"hunger":52,"health":14,"happiness":22,"emoji":"🍲","desc":"فتة بالخل والثوم. «يوم العيد»"},
    "حمام محشي فريك":  {"price":150,"hunger":62,"health":20,"happiness":32,"emoji":"🍗","desc":"أكل ملوك. من أحسن مطعم في البلد."},
    "بيتزا مارجريتا":  {"price":80,"hunger":42,"health":5,"happiness":22,"emoji":"🍕","desc":"من بيتزا الفرن."},
    "فراخ بانيه":      {"price":60,"hunger":40,"health":7,"happiness":20,"emoji":"🍗","desc":"مقرمشة مع الكاتشب."},
    "ترمس بالليمون":   {"price":5, "hunger":10,"health":3,"happiness":3,"emoji":"🫘","desc":"سناك الأيام. «ترمس يا ولاد»"},
    "بطاطس محمرة":     {"price":10,"hunger":14,"health":2,"happiness":6,"emoji":"🍟","desc":"محمرة في الزيت الغزير."},
    "عيش بلدي":        {"price":2, "hunger":8, "health":2,"happiness":2,"emoji":"🫓","desc":"أساس أي أكلة."},
}

DRINKS: dict[str,dict[str,Any]] = {
    "مياه معدنية":   {"price":5, "thirst":32,"health":5,"happiness":0,"energy":0,"emoji":"💧","desc":"أهم حاجة في الدنيا."},
    "شاي بالنعناع":  {"price":7, "thirst":15,"happiness":7,"energy":4,"emoji":"🫖","desc":"شاي مصري تقيل. «شاي بالنعناع يا أسطى»"},
    "شاي كشري":     {"price":4, "thirst":12,"happiness":4,"energy":3,"emoji":"☕","desc":"شاي تقيل يفوّق."},
    "قهوة تركي":    {"price":14,"thirst":18,"happiness":12,"energy":18,"emoji":"☕","desc":"مظبوط يا بيه. «القهوة لأصحاب المزاج»"},
    "نسكافيه":      {"price":10,"thirst":16,"happiness":7,"energy":14,"emoji":"☕","desc":"صحيان يا ناس."},
    "عصير قصب":     {"price":16,"thirst":34,"happiness":16,"energy":6,"emoji":"🥤","desc":"طازة من العربية. «يا قصب يا عسل»"},
    "عصير مانجو":   {"price":25,"thirst":38,"health":8,"happiness":22,"energy":8,"emoji":"🥭","desc":"كاسات الصيف."},
    "بيبسي":        {"price":12,"thirst":24,"health":-2,"happiness":10,"energy":3,"emoji":"🥤","desc":"سكر وغاز."},
    "سحلب بالمكسرات":{"price":15,"thirst":22,"happiness":14,"health":6,"energy":5,"emoji":"🥛","desc":"في ليالي الشتا."},
    "عرقسوس":       {"price":8, "thirst":28,"happiness":9,"health":4,"emoji":"🍺","desc":"عرقسووووس! «مشروب رمضان»"},
    "كركديه ساقع":  {"price":8, "thirst":26,"happiness":8,"health":7,"emoji":"🍷","desc":"ساقع في الصيف. منعش."},
    "خروب":         {"price":7, "thirst":24,"happiness":6,"health":4,"emoji":"🥤","desc":"حاجة ساقعة من الزمن الجميل."},
    "تمر هندي":     {"price":8, "thirst":26,"happiness":8,"health":3,"emoji":"🥤","desc":"الطعم الأصيل."},
}

CLOTHES: dict[str,dict[str,Any]] = {
    "شبشب":              {"price":25, "happiness":1,"reputation":0,"emoji":"🩴","desc":"الأساسي."},
    "تيشيرت سوق التوفيقية":{"price":80, "happiness":4,"reputation":1,"emoji":"👕","desc":"رخيص وشيك."},
    "جلباب بلدي":         {"price":150,"happiness":5,"reputation":3,"emoji":"👘","desc":"أصالة مصرية."},
    "بنطلون جينز":        {"price":300,"happiness":6,"reputation":3,"emoji":"👖","desc":"كاجوال."},
    "فستان كاجوال":       {"price":280,"happiness":8,"reputation":4,"emoji":"👗","desc":"للبنات. شيك."},
    "قميص رسمي":          {"price":400,"happiness":7,"reputation":5,"emoji":"👔","desc":"للشغل."},
    "جاكيت جلد":          {"price":850,"happiness":10,"reputation":8,"emoji":"🧥","desc":"هيبة. «اللي لابس جلد ده مين؟»"},
    "بدلة رسمية":         {"price":1100,"happiness":12,"reputation":10,"emoji":"🤵","desc":"للمقابلات والأفراح."},
    "فستان سواريه":       {"price":2200,"happiness":15,"reputation":12,"emoji":"👗","desc":"للمناسبات الكبيرة."},
    "ساعة كاسيو":         {"price":800,"happiness":6,"reputation":5,"emoji":"⌚","desc":"كلاسيك."},
    "ساعة فاخرة":         {"price":5500,"happiness":18,"reputation":25,"emoji":"⌚","desc":"برستيج. «الغالي تمنه فيه»"},
    "نضارة شمس ريبان":    {"price":1600,"happiness":8,"reputation":12,"charisma":3,"emoji":"🕶️","desc":"ستايل."},
    "حذاء نايكي":         {"price":2000,"happiness":10,"reputation":8,"emoji":"👟","desc":"أصلي."},
    "عطر أصلي":           {"price":2800,"happiness":12,"charisma":6,"emoji":"🧴","desc":"ريحة الأمراء."},
    "طقم ذهب 21":         {"price":18000,"happiness":28,"reputation":35,"emoji":"💍","desc":"قيراط 21. «الدهب دهب»"},
}

TOOLS: dict[str,dict[str,Any]] = {
    "موبايل صيني":        {"price":600, "emoji":"📱","desc":"بيفتح واتساب بالعافية."},
    "موبايل سامسونج":     {"price":2500,"programming_skill":1,"design_skill":1,"emoji":"📱","desc":"يشتغل كويس."},
    "آيفون":              {"price":22000,"programming_skill":3,"design_skill":3,"charisma":5,"emoji":"📱","desc":"فليكس. «باين عليك ابن ناس»"},
    "لاب توب مستعمل":     {"price":5500,"programming_skill":4,"design_skill":3,"hacking_skill":2,"emoji":"💻","desc":"بداية الفريلانس."},
    "لاب توب ماك":        {"price":32000,"programming_skill":12,"design_skill":10,"hacking_skill":6,"emoji":"💻","desc":"ماك بوك. «شغل تقيل»"},
    "كاميرا تصوير":       {"price":16000,"design_skill":12,"streaming_skill":6,"emoji":"📷","desc":"للتصوير الاحترافي."},
    "كاميرا ويب":         {"price":2500,"streaming_skill":8,"emoji":"🎥","desc":"للستريم."},
    "مايك احترافي":       {"price":4500,"streaming_skill":10,"music_skill":5,"emoji":"🎤","desc":"صوت كريستال."},
    "جزمة كورة":          {"price":3500,"football_skill":6,"emoji":"⚽","desc":"مرسيال يا كابتن."},
    "بلاي ستيشن 5":       {"price":14000,"fun":22,"happiness":16,"emoji":"🎮","desc":"فيفا طوووول الليل."},
    "عدة ميكانيكا":       {"price":7000,"fighting_skill":2,"reputation":3,"emoji":"🔧","desc":"شغل جانبي."},
}

WEAPONS: dict[str,dict[str,Any]] = {
    "شبشب الوالدة":    {"price":1,   "fighting_skill":2,"emoji":"🩴","desc":"أقوى سلاح في مصر. والله العظيم."},
    "مطواة قرن غزال":  {"price":150, "fighting_skill":4,"stealth_skill":1,"emoji":"🔪","desc":"كلاسيك."},
    "نبوت صعيدي":     {"price":700, "fighting_skill":9,"reputation":4,"emoji":"🪵","desc":"نبوت الرجالة. «اللي معاه نبوت بيحكم»"},
    "مضرب بيسبول":    {"price":1000,"fighting_skill":11,"emoji":"🏏","desc":"أمريكاني بس شغّال."},
    "سلاح رش (RPG)":  {"price":4500,"fighting_skill":20,"reputation":10,"emoji":"🔫","desc":"(خيالي — للعبة بس)"},
    "قفازات ملاكمة":   {"price":1200,"fighting_skill":8,"fitness":3,"emoji":"🥊","desc":"تايسون مصر."},
    "درع صاج":        {"price":2500,"fighting_skill":5,"health":12,"emoji":"🛡️","desc":"حماية."},
}

HYGIENE_ITEMS: dict[str,dict[str,Any]] = {
    "صابونة نابلسي":   {"price":8, "hygiene":18,"happiness":2,"emoji":"🧼","desc":"نضافة."},
    "شامبو":           {"price":20,"hygiene":22,"happiness":5,"emoji":"🧴","desc":"شعر نضيف."},
    "دش سخن":          {"price":12,"hygiene":38,"happiness":12,"energy":6,"emoji":"🚿","desc":"دش يفوّق."},
    "حمام تركي":       {"price":90,"hygiene":55,"happiness":22,"health":6,"emoji":"🏖️","desc":"ريلاكس تمام."},
    "حلاق أبو صلاح":   {"price":40,"hygiene":28,"charisma":3,"happiness":10,"emoji":"💈","desc":"حلاقة زيرو وتهذيب دقن."},
}

ENTERTAINMENT: dict[str,dict[str,Any]] = {
    "قعدة على القهوة":    {"price":15,"fun":16,"happiness":9,"emoji":"☕","desc":"شاي وطاولة ودومينو."},
    "سينما":             {"price":70,"fun":28,"happiness":20,"emoji":"🎬","desc":"فيلم عربي في السينما."},
    "ملاهي دريم بارك":   {"price":55,"fun":32,"happiness":24,"emoji":"🎡","desc":"ملاهي وألعاب."},
    "كافيه فاخر":        {"price":110,"fun":22,"happiness":16,"charisma":1,"emoji":"🍵","desc":"لاتيه وتشيز كيك."},
    "ماتش في الإستاد":   {"price":90,"fun":38,"happiness":28,"emoji":"⚽","desc":"أهلاوي ولا زملكاوي؟"},
    "حديقة الأزهر":      {"price":25,"fun":20,"happiness":14,"health":4,"emoji":"🌳","desc":"هدوء وخضرة ونسمة هوا."},
    "جيم (تمرين)":       {"price":45,"fun":12,"health":10,"fighting_skill":1,"fitness":3,"energy":-18,"emoji":"💪","desc":"حديد يا كابتن."},
    "بلاي ستيشن كافيه":  {"price":20,"fun":30,"happiness":16,"emoji":"🎮","desc":"فيفا مع الصحاب."},
    "شيشة":              {"price":35,"fun":22,"happiness":12,"health":-4,"emoji":"💨","desc":"تفاح ونعناع. (ضارة يا معلم)"},
    "فلوكة على النيل":   {"price":180,"fun":42,"happiness":32,"emoji":"⛵","desc":"رحلة رومانسية. «النيل بالليل»"},
    "ديسكو":             {"price":250,"fun":48,"happiness":38,"charisma":2,"emoji":"🪩","desc":"رقص ومزاج."},
    "حديقة الحيوان":     {"price":30,"fun":25,"happiness":18,"emoji":"🦁","desc":"الجيزة. «عمي قردة»"},
}

BOOKS: dict[str,dict[str,Any]] = {
    "رواية مصرية (نجيب محفوظ)":  {"price":25,"happiness":9,"xp":22,"emoji":"📖","desc":"زقاق المدق."},
    "كتاب تنمية (إبراهيم الفقي)":{"price":45,"happiness":5,"charisma":2,"xp":32,"emoji":"📕","desc":"قوة التفكير الإيجابي."},
    "كتاب برمجة بايثون":         {"price":100,"programming_skill":4,"xp":55,"emoji":"📘","desc":"من الصفر للاحتراف."},
    "كتاب تصميم جرافيك":         {"price":90,"design_skill":4,"xp":50,"emoji":"📗","desc":"أساسيات فوتوشوب."},
    "كتاب أمن سيبراني":          {"price":130,"hacking_skill":4,"xp":60,"emoji":"📙","desc":"مبادئ الحماية."},
    "كتاب طبخ ست الكل":          {"price":35,"cooking_skill":4,"xp":28,"emoji":"📒","desc":"أكلات مصرية أصيلة."},
    "مجلة كورة الأهرام":         {"price":10,"football_skill":1,"happiness":5,"xp":10,"emoji":"📰","desc":"أخبار الملاعب."},
    "كتاب بزنس وتجارة":          {"price":180,"trading_skill":4,"xp":65,"emoji":"📚","desc":"أسرار النجاح."},
}

# ═══════════════════════════════════════════════════════════════
# عقارات — بأحياء واقعية
# ═══════════════════════════════════════════════════════════════
HOUSES: dict[str,dict[str,Any]] = {
    "تحت الكوبري":          {"price":0,      "energy_bonus":8,  "happiness_bonus":-18,"security":0, "emoji":"🌉","desc":"ربنا يستر. بعوض وبرد. «اللي مالوش دار مالوش قرار»"},
    "غرفة على السطوح":      {"price":2500,   "energy_bonus":18, "happiness_bonus":3,  "security":5, "emoji":"🏚️","desc":"أحسن من الشارع. في إمبابة."},
    "أوضة إيجار في بولاق":  {"price":7000,   "energy_bonus":28, "happiness_bonus":8,  "security":10,"emoji":"🚪","desc":"في حارة شعبية. «الجار قبل الدار»"},
    "شقة في شبرا":          {"price":22000,  "energy_bonus":38, "happiness_bonus":15, "security":20,"emoji":"🏢","desc":"حي شعبي محترم."},
    "شقة في مدينة نصر":     {"price":50000,  "energy_bonus":48, "happiness_bonus":24, "security":30,"emoji":"🏬","desc":"سيتي ستارز قريب."},
    "شقة في المهندسين":     {"price":100000, "energy_bonus":55, "happiness_bonus":32, "security":40,"emoji":"🏙️","desc":"كافيهات ومطاعم."},
    "دوبلكس في التجمع":     {"price":250000, "energy_bonus":65, "happiness_bonus":45, "security":55,"emoji":"🏘️","desc":"كمبوند وحمام سباحة."},
    "فيلا في الشيخ زايد":   {"price":600000, "energy_bonus":78, "happiness_bonus":58, "security":70,"emoji":"🏡","desc":"جنينة وجراج."},
    "قصر في الساحل الشمالي": {"price":2500000,"energy_bonus":95, "happiness_bonus":78, "security":88,"emoji":"🏰","desc":"على البحر. «عيشة الملوك»"},
    "برج خاص في العلمين":   {"price":12000000,"energy_bonus":120,"happiness_bonus":100,"security":100,"emoji":"🗼","desc":"أنت بقيت فرعون يا باشا."},
}

CARS: dict[str,dict[str,Any]] = {
    "ماشي على رجلك":   {"price":0,      "speed":0, "happiness":0, "emoji":"🚶","desc":"«اللي مش لاقي يركب يمشي»"},
    "عجلة صيني":       {"price":1200,   "speed":8, "happiness":4, "emoji":"🚲","desc":"صحة وبيئة."},
    "موتوسيكل":        {"price":8000,   "speed":30,"happiness":14,"emoji":"🏍️","desc":"سريع ورخيص."},
    "توكتوك":          {"price":16000,  "speed":26,"happiness":18,"emoji":"🛺","desc":"ملك الحارة. «توكتوك يلا»"},
    "فيات 128":        {"price":30000,  "speed":32,"happiness":20,"emoji":"🚗","desc":"عربية الناس. «128 يا معلم»"},
    "لادا":            {"price":22000,  "speed":28,"happiness":16,"emoji":"🚗","desc":"مبتعطلش. كدب. 😂"},
    "هيونداي فيرنا":   {"price":75000,  "speed":48,"happiness":30,"emoji":"🚙","desc":"اعتمادية."},
    "تويوتا كورولا":   {"price":140000, "speed":55,"happiness":38,"emoji":"🚙","desc":"مابتخلصش."},
    "BMW 320":         {"price":380000, "speed":75,"happiness":58,"emoji":"🚘","desc":"فخامة ألماني."},
    "مرسيدس C200":    {"price":650000, "speed":82,"happiness":68,"emoji":"🚘","desc":"هيبة. «الشكل ده فلوس»"},
    "رينج روفر":      {"price":1100000,"speed":80,"happiness":75,"emoji":"🚙","desc":"SUV ملوك."},
    "بورش 911":       {"price":1800000,"speed":90,"happiness":85,"emoji":"🏎️","desc":"سبورت."},
    "لامبورجيني":     {"price":4500000,"speed":100,"happiness":100,"emoji":"🏎️","desc":"آخر دلع. «فلوس ومش عارف أعمل بيها إيه»"},
}

# ═══════════════════════════════════════════════════════════════
# بزنسات — مع محاكاة زبائن
# ═══════════════════════════════════════════════════════════════
BUSINESSES: dict[str,dict[str,Any]] = {
    "عربية فول وطعمية":     {"price":6000,   "income":160, "emoji":"🫘","desc":"فول وطعمية الصبح. زباينك: عم حسن، أم أحمد، المعلم سيد...","sign":"ممنوع الآجل | الزبون دايماً على حق 🫘"},
    "كشك سجاير وشاي":      {"price":10000,  "income":220, "emoji":"🚬","desc":"سجاير وحاجة ساقعة. مكانه جنب المسجد.","sign":"الشك ممنوع 🚫 | ادفع واستلم ☕"},
    "محل بقالة":            {"price":22000,  "income":340, "emoji":"🏪","desc":"بقالة ابن الحتة. كل حاجة عنده.","sign":"البضاعة المباعة لا ترد ولا تستبدل 🏪"},
    "صالون حلاقة أبو صلاح": {"price":40000,  "income":620, "emoji":"💈","desc":"حلاقة وتهذيب وعريس. زباينه ثابتين.","sign":"أهلاً بالزباين ✂️ | اللي مش عاجبه يعمل صالون 💈"},
    "مطعم كشري التحرير":    {"price":65000,  "income":900, "emoji":"🍝","desc":"أشهر كشري في المنطقة. طابور ع الباب.","sign":"كشري · دقة · شطة · دمعة الست 🍝"},
    "محل موبايلات":         {"price":110000, "income":1600,"emoji":"📱","desc":"بيع وصيانة واكسسوارات.","sign":"الموبايل اللي عندنا مش عند غيرنا 📱"},
    "كافيه":                {"price":180000, "income":2400,"emoji":"☕","desc":"قهوة وماتشات ومزاج.","sign":"Wi-Fi مجاني ☕ | ممنوع الصوت العالي 🤫"},
    "جيم حديد":             {"price":160000, "income":2000,"emoji":"💪","desc":"حديد وبروتين وكابتنات.","sign":"NO PAIN NO GAIN 💪"},
    "شركة تسويق ديجيتال":   {"price":300000, "income":4200,"emoji":"📊","desc":"ماركتنج وسوشيال ميديا.","sign":"نوصّلك للعميل 📊"},
    "شركة برمجة":           {"price":450000, "income":6500,"emoji":"💻","desc":"ويب وموبايل وحلول ذكية.","sign":"< code > We Build Solutions 💻"},
    "مطعم فاخر":            {"price":550000, "income":8000,"emoji":"🍷","desc":"Fine Dining. أكل فرنساوي مصري.","sign":"Reservation Only 🍷"},
    "مول تجاري":            {"price":1800000,"income":22000,"emoji":"🏬","desc":"محلات ومطاعم وسينما.","sign":"كل حاجة تحت سقف واحد 🏬"},
    "فندق 5 نجوم":          {"price":5000000,"income":52000,"emoji":"🏨","desc":"سياحة وأجانب ومؤتمرات.","sign":"⭐⭐⭐⭐⭐ Welcome"},
}

NEIGHBORHOODS = {
    "إمبابة":{"type":"شعبي","safety":22,"desc":"عشوائي بس فيه ناس طيبة."},
    "بولاق":{"type":"شعبي","safety":28,"desc":"حي شعبي عريق."},
    "السيدة زينب":{"type":"شعبي","safety":32,"desc":"حسين وسيدة. «الحارة كلها عيلة»"},
    "شبرا":{"type":"متوسط","safety":42,"desc":"الحي الكبير."},
    "مدينة نصر":{"type":"متوسط","safety":52,"desc":"سيتي ستارز."},
    "المهندسين":{"type":"راقي","safety":62,"desc":"كافيهات ومطاعم."},
    "الزمالك":{"type":"راقي","safety":72,"desc":"جزيرة الأغنياء."},
    "التجمع الخامس":{"type":"فاخر","safety":82,"desc":"كمبوندات."},
    "الشيخ زايد":{"type":"فاخر","safety":85,"desc":"فيلات وحدائق."},
    "الساحل الشمالي":{"type":"فاخر","safety":90,"desc":"على البحر. «صيفك معانا»"},
}

MARKET_CATEGORIES = {
    "🍗 أكل مصري": FOODS,
    "🥤 مشروبات": DRINKS,
    "👔 لبس وإكسسوارات": CLOTHES,
    "🔧 أدوات وأجهزة": TOOLS,
    "⚔️ أسلحة RPG": WEAPONS,
    "🧼 نظافة": HYGIENE_ITEMS,
    "🎭 ترفيه": ENTERTAINMENT,
    "📚 مكتبة": BOOKS,
}
