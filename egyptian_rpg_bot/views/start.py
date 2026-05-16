# -*- coding: utf-8 -*-
"""start.py — Character creation — dev by 7amo"""
from __future__ import annotations
import discord
from discord.ui import View,Button,Select,Modal,TextInput
from config import COLOR_GREEN
from data.classes import STARTER_CLASSES,AGE_GROUPS,GENDERS
from services.canvas import generate_profile_image
from services.economy import player_stats_text
from views.helpers import make_embed

class StartNameModal(Modal, title="✍️ اسم شخصيتك"):
    def __init__(self,v): super().__init__(timeout=120); self.pv=v; self.ni=TextInput(label="اكتب اسمك",min_length=2,max_length=32,placeholder="مثال: المعلم حمو / حبيبة"); self.add_item(self.ni)
    async def on_submit(self,i): self.pv.display_name=str(self.ni.value).strip(); await i.response.send_message(f"✅ الاسم: **{self.pv.display_name}**. اضغط تأكيد!",ephemeral=True)

class StartView(View):
    def __init__(self,user,db):
        super().__init__(timeout=300); self.uid=user.id; self.display_name=user.display_name[:32]
        self.char_class="موظف حكومة"; self.age_group="شب (23 سنة)"; self.gender="ولد"; self.db=db
    async def interaction_check(self,i):
        if i.user.id!=self.uid: await i.response.send_message("❌ مش بتاعتك.",ephemeral=True); return False
        return True
    @discord.ui.select(placeholder="🎭 اختار شخصيتك",min_values=1,max_values=1,
        options=[discord.SelectOption(label=f"{v.get('emoji','')} {k}",description=v["desc"][:100],value=k) for k,v in STARTER_CLASSES.items()],row=0)
    async def sel_class(self,i,s):
        self.char_class=s.values[0]; c=STARTER_CLASSES[self.char_class]
        await i.response.send_message(embed=make_embed(f"✅ {c.get('emoji','')} {self.char_class}",c['desc'],COLOR_GREEN),ephemeral=True)
    @discord.ui.select(placeholder="📅 العمر",min_values=1,max_values=1,
        options=[discord.SelectOption(label=f"{v.get('emoji','')} {k}",description=v["desc"][:100],value=k) for k,v in AGE_GROUPS.items()],row=1)
    async def sel_age(self,i,s): self.age_group=s.values[0]; await i.response.send_message(f"✅ العمر: **{self.age_group}**",ephemeral=True)
    @discord.ui.select(placeholder="🧑/👩 النوع",min_values=1,max_values=1,
        options=[discord.SelectOption(label=k,description=v["desc"],value=v["value"]) for k,v in GENDERS.items()],row=2)
    async def sel_gender(self,i,s): self.gender=s.values[0]; await i.response.send_message(f"✅ النوع: **{self.gender}**",ephemeral=True)
    @discord.ui.button(label="✍️ تغيير الاسم",style=discord.ButtonStyle.secondary,row=3)
    async def name_btn(self,i,b): await i.response.send_modal(StartNameModal(self))
    @discord.ui.button(label="✅ تأكيد البداية",style=discord.ButtonStyle.success,row=3,emoji="🎮")
    async def confirm(self,i,b):
        if await self.db.get_player(self.uid): await i.response.send_message("❌ مسجل بالفعل! `!منيو`",ephemeral=True); return
        await self.db.create_player(i.user,self.display_name,self.char_class,self.age_group,self.gender)
        p=await self.db.get_player(self.uid)
        e=make_embed("🎮 أهلاً بيك في مصر RPG!",f"مبروك يا **{self.display_name}**! 🎉\nبدأت كـ **{self.char_class}** ({self.gender})\n{player_stats_text(p)}\n\nاستخدم **!منيو** عشان تلعب! 👇",COLOR_GREEN)
        img=await generate_profile_image(p); f=discord.File(img,filename="profile.png"); e.set_image(url="attachment://profile.png")
        from views.main_menu import MainMenuView
        await i.response.send_message(embed=e,file=f,view=MainMenuView(self.uid,self.db)); self.stop()
