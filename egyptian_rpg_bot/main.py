# -*- coding: utf-8 -*-
"""
Main Bot Entry Point - Orchestrates all systems
Production-level Egyptian RPG Bot
"""

import os
import sys
import logging
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands, tasks

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("EgyptianRPG")

# ════════════════════════════════════════════════════════════════
# IMPORTS
# ════════════════════════════════════════════════════════════════

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import BOT_TOKEN, PREFIX, DB_FILE, OWNER_BRAND
from database.sqlite_handler import ProDatabase
from services.managers import EconomyManager, SkillManager, StatManager
from services.npc_system import NPCManager
from services.world_events import EventManager, EventTrigger
from services.gambling import GamblingManager
from utils.helpers import format_money, get_random_greeting

# ════════════════════════════════════════════════════════════════
# BOT SETUP
# ════════════════════════════════════════════════════════════════

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# Global managers
db: Optional[ProDatabase] = None
economy_manager: Optional[EconomyManager] = None
skill_manager: Optional[SkillManager] = None
stat_manager: Optional[StatManager] = None
npc_manager: Optional[NPCManager] = None
event_manager: Optional[EventManager] = None
gambling_manager: Optional[GamblingManager] = None

# ════════════════════════════════════════════════════════════════
# BOT INITIALIZATION
# ════════════════════════════════════════════════════════════════

@bot.event
async def on_ready():
    """Bot startup"""
    global db, economy_manager, skill_manager, stat_manager, npc_manager, event_manager, gambling_manager
    
    log.info("═" * 60)
    log.info(f"  🎮 Bot Logged In: {bot.user}")
    log.info(f"  {OWNER_BRAND}")
    log.info(f"  Servers: {len(bot.guilds)}")
    log.info("═" * 60)
    
    # Initialize database
    if db is None:
        db = ProDatabase(DB_FILE)
        await db.init()
        log.info("✅ Database initialized")
    
    # Initialize managers
    if economy_manager is None:
        economy_manager = EconomyManager(db)
        skill_manager = SkillManager(db)
        stat_manager = StatManager(db)
        npc_manager = NPCManager()
        event_manager = EventManager()
        gambling_manager = GamblingManager(db)
        log.info("✅ All managers initialized")
    
    # Sync commands
    if not hasattr(bot, "_synced"):
        try:
            synced = await bot.tree.sync()
            log.info(f"✅ Synced {len(synced)} slash commands")
        except Exception as e:
            log.error(f"❌ Sync error: {e}")
        bot._synced = True
    
    # Start background tasks
    if not world_loop.is_running():
        world_loop.start()
        log.info("✅ World loop started")
    
    if not stat_decay_loop.is_running():
        stat_decay_loop.start()
        log.info("✅ Stat decay loop started")

# ════════════════════════════════════════════════════════════════
# SLASH COMMANDS
# ════════════════════════════════════════════════════════════════

@bot.tree.command(name="start", description="ابدأ لعبتك! 🎮")
async def cmd_start(interaction: discord.Interaction):
    """Start/register player"""
    player = await db.get_player(interaction.user.id)
    
    if player:
        await interaction.response.send_message(
            f"✅ أنت مسجل بالفعل يا **{player['display_name']}**!\n"
            f"استخدم `/menu` للدخول للعبة!",
            ephemeral=True
        )
        return
    
    # Show character selection
    await interaction.response.send_message(
        "🎮 اختار شخصيتك:\n"
        "👔 موظف | 💪 بلطجي | 😎 عريس الجنة | 🌾 فلاح\n"
        "📚 طالب | 💻 مبرمج | ⚽ لاعب كورة | 🎥 ستريمر",
        ephemeral=True
    )

@bot.tree.command(name="profile", description="شوف بروفايلك 👤")
async def cmd_profile(interaction: discord.Interaction, user: Optional[discord.Member] = None):
    """View player profile"""
    target = user or interaction.user
    player = await db.get_player(target.id)
    
    if not player:
        await interaction.response.send_message(f"❌ {target.name} لم يسجل بعد!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title=f"👤 {player['display_name']}",
        description=f"الفئة: {player['char_class']} | المستوى: {player['level']}",
        color=0xF1C40F
    )
    
    embed.add_field(name="💰 الأموال", value=format_money(player['money']), inline=True)
    embed.add_field(name="🏦 البنك", value=format_money(player['bank']), inline=True)
    embed.add_field(name="⭐ السمعة", value=str(player['reputation']), inline=True)
    
    embed.add_field(name="❤️ الصحة", value=f"{player['health']}/100", inline=True)
    embed.add_field(name="🍽️ الجوع", value=f"{player['hunger']}/100", inline=True)
    embed.add_field(name="⚡ الطاقة", value=f"{player['energy']}/100", inline=True)
    
    embed.set_footer(text=OWNER_BRAND)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="menu", description="القائمة الرئيسية 🎮")
async def cmd_menu(interaction: discord.Interaction):
    """Main game menu"""
    player = await db.get_player(interaction.user.id)
    
    if not player:
        await interaction.response.send_message(
            "❌ أنت لم تسجل بعد! استخدم `/start` أولاً",
            ephemeral=True
        )
        return
    
    embed = discord.Embed(
        title=f"🎮 المنيو الرئيسي - {player['display_name']}",
        description=f"اختار ما تبغى تعمل:\n\n{get_random_greeting()}",
        color=0x3498DB
    )
    
    embed.add_field(name="💼 الاقتصاد", value="💰 أموال | 🏦 بنك | 📊 استثمارات", inline=False)
    embed.add_field(name="👔 الوظيفة", value="💼 شغل | 📈 ترقية | 🎓 مهارات", inline=False)
    embed.add_field(name="🎰 الترفيه", value="🎲 مقامرة | 🎮 ألعاب | 🎉 أحداث", inline=False)
    embed.add_field(name="👥 اجتماعي", value="💍 جواز | 👥 عصابات | 📱 أصدقاء", inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="daily", description="المكافأة اليومية! 🎁")
async def cmd_daily(interaction: discord.Interaction):
    """Daily reward"""
    player = await db.get_player(interaction.user.id)
    
    if not player:
        await interaction.response.send_message("❌ اكتب `/start` أولاً!", ephemeral=True)
        return
    
    # Check cooldown
    remaining = await db.cooldown_remaining(interaction.user.id, "daily")
    if remaining > 0:
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        await interaction.response.send_message(
            f"⏰ تستطيع تحصل على المكافأة خلال: **{hours}س {minutes}د**",
            ephemeral=True
        )
        return
    
    # Calculate reward
    streak = player["daily_streak"] + 1
    base_reward = 200
    streak_bonus = streak * 50
    total = base_reward + streak_bonus
    
    if streak >= 7:
        total += 500
    
    # Give reward
    await economy_manager.add_money(interaction.user.id, total, "مكافأة يومية")
    await db.update_player(interaction.user.id, daily_streak=streak)
    await db.set_cooldown(interaction.user.id, "daily", hours=20)
    
    bonus_text = f"\n🎁 **بونص أسبوع +500**" if streak >= 7 else ""
    
    embed = discord.Embed(
        title="🎁 المكافأة اليومية!",
        description=f"💰 الجائزة: **{total:,}**\n🔥 السلسلة: **{streak}** يوم{bonus_text}",
        color=0x2ECC71
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="top", description="الترتيب العام 🏆")
async def cmd_top(interaction: discord.Interaction):
    """Leaderboard"""
    rows = await db.leaderboard(15)
    
    if not rows:
        await interaction.response.send_message("❌ لا يوجد لاعبين بعد!", ephemeral=True)
        return
    
    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 12
    
    description = ""
    for i, row in enumerate(rows):
        wealth = row["money"] + row["bank"]
        description += f"{medals[i]} **{row['display_name']}** ({row['char_class']})\n"
        description += f"   💰 {wealth:,} | ⭐ Lvl {row['level']}\n\n"
    
    embed = discord.Embed(
        title="🏆 الترتيب العام",
        description=description[:2000],
        color=0xF1C40F
    )
    
    await interaction.response.send_message(embed=embed)

# ════════════════════════════════════════════════════════════════
# BACKGROUND TASKS
# ════════════════════════════════════════════════════════════════

@tasks.loop(minutes=30)
async def world_loop():
    """World update loop"""
    try:
        # Update NPCs
        from datetime import datetime
        hour = datetime.now().hour
        npc_manager.update_all_npcs(hour)
        
        # Check for world events
        if event_manager:
            if len(event_manager.get_active_events()) < 3:
                event_manager.add_event(event_manager.create_random_event())
        
        log.debug("🌍 World updated")
    except Exception as e:
        log.error(f"World loop error: {e}")

@tasks.loop(hours=1)
async def stat_decay_loop():
    """Stat decay loop"""
    try:
        if db:
            # Decay player stats
            await db.execute("""
                UPDATE players SET
                    hunger = MIN(100, hunger + 3),
                    energy = MAX(0, energy - 2),
                    hygiene = MAX(0, hygiene - 1),
                    happiness = MAX(0, happiness - 1),
                    updated_at = CURRENT_TIMESTAMP
                WHERE 1=1
            """)
            log.debug("📉 Stats decayed")
    except Exception as e:
        log.error(f"Stat decay error: {e}")

# ════════════════════════════════════════════════════════════════
# ERROR HANDLING
# ════════════════════════════════════════════════════════════════

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        return
    
    log.error(f"Command error: {error}")
    await ctx.reply(f"⚠️ خطأ! {str(error)[:100]}", mention_author=False)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Handle slash command errors"""
    log.error(f"App command error: {error}")
    
    if not interaction.response.is_done():
        await interaction.response.send_message(
            f"⚠️ حدث خطأ! {str(error)[:100]}",
            ephemeral=True
        )

# ════════════════════════════════════════════════════════════════
# STARTUP
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ضع التوكن في متغير DISCORD_TOKEN")
        sys.exit(1)
    
    log.info("🚀 Starting Egyptian RPG Bot...")
    try:
        bot.run(BOT_TOKEN)
    except KeyboardInterrupt:
        log.info("⛔ Bot stopped")
    except Exception as e:
        log.error(f"❌ Fatal error: {e}")
        sys.exit(1)
