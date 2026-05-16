# -*- coding: utf-8 -*-
"""الوظائف ومسارات الترقية والأحداث — 𝐝𝐞𝐯 𝐛𝐲 𝟕𝐚𝐦𝐨"""
from __future__ import annotations
from typing import Any

JOBS: dict[str, dict[str, Any]] = {
    "عاطل":{"salary":0,"energy_cost":0,"req_level":1,"emoji":"😴","desc":"قاعد ع القهوة. يا رب الفرج.","ranks":[]},
    "شحات":{"salary":25,"energy_cost":12,"req_level":1,"emoji":"🥺","desc":"يا عم ادّيني جنيه ربنا يخليك.","ranks":[
        {"name":"شحات مبتدئ","job_xp":0,"salary_bonus":0},{"name":"شحات محترف","job_xp":200,"salary_bonus":20},{"name":"ملك الشحاتة","job_xp":600,"salary_bonus":55}]},
    "طالب":{"salary":20,"energy_cost":10,"req_level":1,"emoji":"📚","desc":"مصاريف من البيت ودروس خصوصية.","ranks":[
        {"name":"طالب مستجد","job_xp":0,"salary_bonus":0},{"name":"طالب مجتهد","job_xp":300,"salary_bonus":15},{"name":"الأول ع الدفعة","job_xp":800,"salary_bonus":40}]},
    "عامل يومية":{"salary":65,"energy_cost":35,"req_level":1,"emoji":"🧱","desc":"شغلانة متعبة بس رزقها حلال.","ranks":[
        {"name":"عامل يومية","job_xp":0,"salary_bonus":0},{"name":"معلم بناء","job_xp":400,"salary_bonus":30},{"name":"مقاول صغير","job_xp":1000,"salary_bonus":90},{"name":"مقاول كبير","job_xp":2500,"salary_bonus":220}]},
    "سواق توكتوك":{"salary":90,"energy_cost":25,"req_level":1,"emoji":"🛺","desc":"توكتوك وأغاني مهرجانات ع الفل.","ranks":[
        {"name":"سواق مبتدئ","job_xp":0,"salary_bonus":0},{"name":"سواق شاطر","job_xp":350,"salary_bonus":25},{"name":"ملك التوكتوك","job_xp":900,"salary_bonus":65}]},
    "بياع كشك":{"salary":75,"energy_cost":18,"req_level":1,"emoji":"🫖","desc":"شاي وحاجة ساقعة وسجاير. الكشك ده رزقه واسع.","ranks":[
        {"name":"بياع","job_xp":0,"salary_bonus":0},{"name":"صاحب كشك","job_xp":500,"salary_bonus":40},{"name":"سلسلة أكشاك","job_xp":1500,"salary_bonus":130}]},
    "موظف كول سنتر":{"salary":125,"energy_cost":26,"req_level":2,"emoji":"📞","desc":"ألو يا فندم.. أقدر أساعدك؟","ranks":[
        {"name":"موظف جديد","job_xp":0,"salary_bonus":0},{"name":"تيم ليدر","job_xp":600,"salary_bonus":50},{"name":"سوبرفايزر","job_xp":1400,"salary_bonus":130},{"name":"مدير القسم","job_xp":3000,"salary_bonus":280}]},
    "فريلانسر مبتدئ":{"salary":150,"energy_cost":22,"req_level":2,"emoji":"💻","desc":"شغل من البيت على فايفر وخمسات.","ranks":[
        {"name":"فريلانسر مبتدئ","job_xp":0,"salary_bonus":0},{"name":"فريلانسر محترف","job_xp":800,"salary_bonus":90},{"name":"توب ريتد","job_xp":2000,"salary_bonus":220}]},
    "لاعب ناشئ":{"salary":170,"energy_cost":38,"req_level":2,"emoji":"⚽","desc":"بتتمرن في النادي وحلمك المنتخب.","ranks":[
        {"name":"ناشئ","job_xp":0,"salary_bonus":0},{"name":"لاعب درجة تانية","job_xp":600,"salary_bonus":120},{"name":"لاعب دوري ممتاز","job_xp":2000,"salary_bonus":600},
        {"name":"نجم المنتخب","job_xp":5000,"salary_bonus":2500},{"name":"محترف أوروبي","job_xp":12000,"salary_bonus":9000}]},
    "ستريمر مبتدئ":{"salary":95,"energy_cost":20,"req_level":2,"emoji":"🎥","desc":"بتعمل لايف ومحتوى. إنفلونسر الحارة.","ranks":[
        {"name":"ستريمر مبتدئ","job_xp":0,"salary_bonus":0},{"name":"يوتيوبر","job_xp":500,"salary_bonus":85},{"name":"يوتيوبر مشهور","job_xp":1500,"salary_bonus":350},
        {"name":"إنفلونسر","job_xp":4000,"salary_bonus":1200},{"name":"نجم السوشيال","job_xp":10000,"salary_bonus":5000}]},
    "موظف بنك":{"salary":210,"energy_cost":32,"req_level":4,"emoji":"🏦","desc":"بدلة وتأمين وقرض عقاري.","ranks":[
        {"name":"تيلر","job_xp":0,"salary_bonus":0},{"name":"أخصائي","job_xp":800,"salary_bonus":80},{"name":"مدير فرع","job_xp":2000,"salary_bonus":220},{"name":"مدير منطقة","job_xp":5000,"salary_bonus":550}]},
    "دكتور":{"salary":400,"energy_cost":40,"req_level":6,"emoji":"🩺","desc":"كشف وروشتة والعيادة دايماً مليانة.","ranks":[
        {"name":"نائب","job_xp":0,"salary_bonus":0},{"name":"أخصائي","job_xp":1000,"salary_bonus":160},{"name":"استشاري","job_xp":3000,"salary_bonus":450},{"name":"بروفيسور","job_xp":8000,"salary_bonus":1100}]},
    "مهندس":{"salary":500,"energy_cost":40,"req_level":7,"emoji":"👷","desc":"موقع ورسومات ومقاولين.","ranks":[
        {"name":"مهندس موقع","job_xp":0,"salary_bonus":0},{"name":"مهندس أول","job_xp":1000,"salary_bonus":160},{"name":"مدير مشروع","job_xp":3000,"salary_bonus":450},{"name":"مدير شركة","job_xp":8000,"salary_bonus":1400}]},
    "تاجر ذهب":{"salary":680,"energy_cost":28,"req_level":9,"emoji":"💰","desc":"الدهب دهب. الجنيه بكام؟","ranks":[
        {"name":"بياع مجوهرات","job_xp":0,"salary_bonus":0},{"name":"تاجر","job_xp":1200,"salary_bonus":220},{"name":"ملك الدهب","job_xp":4000,"salary_bonus":650}]},
    "رجل أعمال":{"salary":1050,"energy_cost":45,"req_level":12,"emoji":"🤵","desc":"اجتماعات وصفقات وقهوة سادة.","ranks":[
        {"name":"بزنسمان صغير","job_xp":0,"salary_bonus":0},{"name":"مدير شركة","job_xp":2000,"salary_bonus":420},{"name":"ملياردير","job_xp":8000,"salary_bonus":2200}]},
    "مطور برمجيات":{"salary":1700,"energy_cost":32,"req_level":18,"emoji":"⌨️","desc":"كود وديباج وستاك أوفرفلو.","ranks":[
        {"name":"جونيور","job_xp":0,"salary_bonus":0},{"name":"سينيور","job_xp":2000,"salary_bonus":550},{"name":"تيك ليد","job_xp":5000,"salary_bonus":1300},{"name":"CTO","job_xp":12000,"salary_bonus":3500}]},
    "خبير أمن سيبراني":{"salary":2300,"energy_cost":42,"req_level":22,"emoji":"🛡️","desc":"حماية أنظمة وأمان.","ranks":[
        {"name":"محلل أمني","job_xp":0,"salary_bonus":0},{"name":"خبير","job_xp":3000,"salary_bonus":850},{"name":"CISO","job_xp":8000,"salary_bonus":2200}]},
    "زعيم عصابة":{"salary":3800,"energy_cost":60,"req_level":30,"emoji":"🔫","desc":"نفوذ وخطر. اللي بيقول كلمته.","ranks":[
        {"name":"زعيم صغير","job_xp":0,"salary_bonus":0},{"name":"دون","job_xp":5000,"salary_bonus":2200},{"name":"الجودفاذر","job_xp":15000,"salary_bonus":7000}]},
}

WORK_EVENTS: list[dict[str, Any]] = [
    {"msg":"المدير اداك بونص عشان شاطر! 💸 «الشاطر يكمّل نقصه»","money_bonus":90,"chance":0.11},
    {"msg":"زميلك جابلك سندوتشات من البيت 🥙 «الجار قبل الدار»","hunger":10,"happiness":6,"chance":0.10},
    {"msg":"المواصلات كانت زحمة الموت 😤 «اللي يركب المواصلات لازم يتحمّل»","happiness":-5,"energy":-4,"chance":0.16},
    {"msg":"لقيت 50 جنيه ورا المكتب! 💵","money_bonus":50,"chance":0.07},
    {"msg":"عميل شتمك على التليفون 😡","happiness":-7,"chance":0.09},
    {"msg":"اتعلمت سكيل جديد 🧠 «العلم نور»","xp_bonus":35,"chance":0.11},
    {"msg":"صاحبك عزمك على قهوة في البريك ☕","happiness":5,"thirst":8,"chance":0.12},
    {"msg":"المرتب اتأخر النهارده 😤 «الصبر مفتاح الفرج»","happiness":-4,"chance":0.08},
    {"msg":"مديرك شافك بتشتغل كويس وشجعك 🌟","happiness":8,"reputation":2,"chance":0.08},
]

# ── أسماء زبائن واقعية ──
CUSTOMERS_MALE = [
    "عم حسن البقال","الحاج سيد الجزار","أستاذ مجدي","باشمهندس وائل",
    "دكتور محمد","المعلم حسن الكبابجي","عم صابر","كابتن عمرو",
    "أبو تريكة الحلاق","حاج عبدالله","مستر كريم","باشمهندس خالد",
    "عم فتحي الفكهاني","الأسطى محمود","أبو العربي","الحاج نبيل",
]
CUSTOMERS_FEMALE = [
    "مدام سلوى","أم أحمد","طنط فاطمة","ميس نجلاء",
    "نوران هانم","مدام غادة","الحاجة زينب","ست الكل أم محمد",
    "بشمهندسة سارة","دكتورة مريم","مدام هدى","أم كريم",
]
CUSTOMERS_ALL = CUSTOMERS_MALE + CUSTOMERS_FEMALE
