# -*- coding: utf-8 -*-
"""
Enhanced async SQLite database handler for production bot
Supports all game systems and advanced queries
"""

import asyncio
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Optional, List, Dict
import logging

log = logging.getLogger(__name__)

def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def clamp(v: float, lo: float = 0, hi: float = 100) -> int:
    return max(lo, min(hi, int(v)))

class ProDatabase:
    """
    Production-level SQLite database with async support
    Manages all game data structures
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.lock = asyncio.Lock()
    
    async def init(self):
        """Initialize database connection and schema"""
        async with self.lock:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self._init_schema()
            log.info(f"✅ Database initialized: {self.db_path}")
    
    def _init_schema(self):
        """Create all tables"""
        c = self.conn.cursor()
        
        # Enable optimizations
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA foreign_keys=ON")
        c.execute("PRAGMA synchronous=NORMAL")
        
        # ══════════════════════════════════════════════════════════════
        # PLAYERS TABLE - Core character data
        # ══════════════════════════════════════════════════════════════
        c.execute("""CREATE TABLE IF NOT EXISTS players(
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            display_name TEXT NOT NULL,
            char_class TEXT DEFAULT 'عاطل',
            gender TEXT DEFAULT 'ولد',
            age_group TEXT DEFAULT 'شاب',
            age INTEGER DEFAULT 23,
            
            -- Job & Career
            job TEXT DEFAULT 'عاطل',
            job_xp INTEGER DEFAULT 0,
            job_rank TEXT DEFAULT '',
            job_level INTEGER DEFAULT 1,
            
            -- Economy
            money INTEGER DEFAULT 500,
            bank INTEGER DEFAULT 0,
            crypto INTEGER DEFAULT 0,
            total_earnings INTEGER DEFAULT 0,
            total_spent INTEGER DEFAULT 0,
            
            -- Stats (0-100)
            health INTEGER DEFAULT 100,
            hunger INTEGER DEFAULT 100,
            thirst INTEGER DEFAULT 100,
            energy INTEGER DEFAULT 100,
            happiness INTEGER DEFAULT 100,
            hygiene INTEGER DEFAULT 80,
            fun INTEGER DEFAULT 50,
            fitness INTEGER DEFAULT 30,
            
            -- Experience & Progression
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            
            -- Assets
            house TEXT DEFAULT 'تحت الكوبري',
            car TEXT DEFAULT 'ماشي على رجلك',
            neighborhood TEXT DEFAULT 'بولاق',
            current_city TEXT DEFAULT 'القاهرة 🏙️',
            
            -- Relationships
            married_to INTEGER DEFAULT NULL,
            gang TEXT DEFAULT NULL,
            gang_rank TEXT DEFAULT NULL,
            
            -- Skills (0-100)
            programming_skill INTEGER DEFAULT 0,
            design_skill INTEGER DEFAULT 0,
            hacking_skill INTEGER DEFAULT 0,
            fighting_skill INTEGER DEFAULT 0,
            stealth_skill INTEGER DEFAULT 0,
            cooking_skill INTEGER DEFAULT 0,
            trading_skill INTEGER DEFAULT 0,
            football_skill INTEGER DEFAULT 0,
            streaming_skill INTEGER DEFAULT 0,
            music_skill INTEGER DEFAULT 0,
            acting_skill INTEGER DEFAULT 0,
            driving_skill INTEGER DEFAULT 0,
            charisma INTEGER DEFAULT 5,
            
            -- Social
            reputation INTEGER DEFAULT 0,
            wanted_level INTEGER DEFAULT 0,
            jail_until TEXT DEFAULT NULL,
            
            -- Daily/Streak
            daily_streak INTEGER DEFAULT 0,
            last_daily TEXT DEFAULT NULL,
            
            -- Timestamps
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        
        # ══════════════════════════════════════════════════════════════
        # INVENTORY - Items and equipment
        # ══════════════════════════════════════════════════════════════
        c.execute("""CREATE TABLE IF NOT EXISTS inventory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            item_type TEXT DEFAULT 'عام',
            rarity TEXT DEFAULT 'عام',
            acquired_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, item),
            FOREIGN KEY(user_id) REFERENCES players(user_id) ON DELETE CASCADE
        )""")
        
        # ══════════════════════════════════════════════════════════════
        # COOLDOWNS - Action cooldown tracking
        # ══════════════════════════════════════════════════════════════
        c.execute("""CREATE TABLE IF NOT EXISTS cooldowns(
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            until TEXT NOT NULL,
            PRIMARY KEY(user_id, action)
        )""")
        
        # ══════════════════════════════════════════════════════════════
        # QUESTS - Quest progress and rewards
        # ══════════════════════════════════════════════════════════════
        c.execute("""CREATE TABLE IF NOT EXISTS quests(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            quest_name TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            progress INTEGER DEFAULT 0,
            target INTEGER DEFAULT 1,
            reward_money INTEGER DEFAULT 0,
            reward_xp INTEGER DEFAULT 0,
            reward_item TEXT DEFAULT NULL,
            UNIQUE(user_id, code),
            FOREIGN KEY(user_id) REFERENCES players(user_id) ON DELETE CASCADE
        )""")
        
        # ══════════════════════════════════════════════════════════════
        # GANGS - Gang management
        # ══════════════════════════════════════════════════════════════
        c.execute("""CREATE TABLE IF NOT EXISTS gangs(
            name TEXT PRIMARY KEY,
            leader_id INTEGER,
            territory TEXT,
            money INTEGER DEFAULT 0,
            reputation INTEGER DEFAULT 0,
            members_count INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        
        # ══════════════════════════════════════════════════════════════
        # BUSINESSES - Business ownership and management
        # ══════════════════════════════════════════════════════════════
        c.execute("""CREATE TABLE IF NOT EXISTS businesses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER NOT NULL,
            business_type TEXT NOT NULL,
            name TEXT NOT NULL,
            location TEXT,
            money INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            employees INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(owner_id) REFERENCES players(user_id) ON DELETE CASCADE
        )""")
        
        # ══════════════════════════════════════════════════════════════
        # TRANSACTIONS - Economic log
        # ══════════════════════════════════════════════════════════════
        c.execute("""CREATE TABLE IF NOT EXISTS transactions_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            amount INTEGER DEFAULT 0,
            details TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        
        # ══════════════════════════════════════════════════════════════
        # GAMBLING - Gambling history and stats
        # ══════════════════════════════════════════════════════════════
        c.execute("""CREATE TABLE IF NOT EXISTS gambling_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game TEXT NOT NULL,
            bet INTEGER,
            won INTEGER DEFAULT 0,
            payout INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        
        # ══════════════════════════════════════════════════════════════
        # PETS - Pet system
        # ══════════════════════════════════════════════════════════════
        c.execute("""CREATE TABLE IF NOT EXISTS pets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            pet_type TEXT NOT NULL,
            happiness INTEGER DEFAULT 80,
            hunger INTEGER DEFAULT 80,
            last_feed TEXT DEFAULT NULL,
            UNIQUE(user_id, name),
            FOREIGN KEY(user_id) REFERENCES players(user_id) ON DELETE CASCADE
        )""")
        
        # ══════════════════════════════════════════════════════════════
        # WORLD EVENTS - Global game events
        # ══════════════════════════════════════════════════════════════
        c.execute("""CREATE TABLE IF NOT EXISTS world_events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            event_name TEXT NOT NULL,
            description TEXT,
            severity INTEGER DEFAULT 5,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT DEFAULT NULL
        )""")
        
        # ══════════════════════════════════════════════════════════════
        # MARKET - Dynamic market data
        # ══════════════════════════════════════════════════════════════
        c.execute("""CREATE TABLE IF NOT EXISTS market_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            current_price INTEGER,
            base_price INTEGER,
            demand INTEGER DEFAULT 50,
            trend TEXT DEFAULT 'stable',
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(item_name)
        )""")
        
        self.conn.commit()
        log.info("✅ Database schema initialized")
    
    # ════════════════════════════════════════════════════════════════
    # BASIC OPERATIONS
    # ════════════════════════════════════════════════════════════════
    
    async def fetchone(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch single row"""
        async with self.lock:
            result = self.conn.execute(query, params).fetchone()
            return dict(result) if result else None
    
    async def fetchall(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch all rows"""
        async with self.lock:
            results = self.conn.execute(query, params).fetchall()
            return [dict(row) for row in results]
    
    async def execute(self, query: str, params: tuple = ()):
        """Execute query"""
        async with self.lock:
            self.conn.execute(query, params)
            self.conn.commit()
    
    async def executemany(self, query: str, params: List[tuple]):
        """Execute multiple queries"""
        async with self.lock:
            self.conn.executemany(query, params)
            self.conn.commit()
    
    # ════════════════════════════════════════════════════════════════
    # PLAYER OPERATIONS
    # ════════════════════════════════════════════════════════════════
    
    async def get_player(self, user_id: int) -> Optional[Dict]:
        """Get player data"""
        return await self.fetchone(
            "SELECT * FROM players WHERE user_id=?", 
            (user_id,)
        )
    
    async def create_player(self, user_id: int, username: str, display_name: str,
                          char_class: str, gender: str = "ولد", age_group: str = "شاب"):
        """Create new player with initial stats"""
        from core.config import STARTER_CLASSES, AGE_GROUPS, clamp
        
        class_data = STARTER_CLASSES.get(char_class, {})
        age_data = AGE_GROUPS.get(age_group, {})
        
        health = clamp(100 + class_data.get("health", 0) + age_data.get("health", 0))
        energy = clamp(100 + class_data.get("energy", 0) + age_data.get("energy", 0))
        
        query = """INSERT INTO players(
            user_id, username, display_name, char_class, gender, age_group, age,
            job, money, health, energy, happiness, fitness
        ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        params = (
            user_id, username, display_name[:32], char_class, gender, age_group,
            age_data.get("age", 23),
            class_data.get("job", "عاطل"),
            class_data.get("money", 500),
            health,
            energy,
            clamp(100 + class_data.get("happiness", 0)),
            class_data.get("fitness", 30)
        )
        
        await self.execute(query, params)
        log.info(f"✅ Player created: {user_id} ({display_name})")
    
    async def update_player(self, user_id: int, **kwargs):
        """Update player fields safely"""
        if not kwargs:
            return
        
        kwargs["updated_at"] = now_str()
        
        fields = ", ".join([f"{k}=?" for k in kwargs.keys()])
        query = f"UPDATE players SET {fields} WHERE user_id=?"
        params = tuple(kwargs.values()) + (user_id,)
        
        await self.execute(query, params)
    
    async def delete_player(self, user_id: int):
        """Delete player and all related data"""
        async with self.lock:
            tables = [
                "inventory", "cooldowns", "quests", "businesses",
                "transactions_log", "gambling_history", "pets"
            ]
            for table in tables:
                self.conn.execute(f"DELETE FROM {table} WHERE user_id=?", (user_id,))
            self.conn.execute("DELETE FROM players WHERE user_id=?", (user_id,))
            self.conn.commit()
        
        log.info(f"✅ Player deleted: {user_id}")
    
    # ════════════════════════════════════════════════════════════════
    # INVENTORY OPERATIONS
    # ════════════════════════════════════════════════════════════════
    
    async def add_item(self, user_id: int, item: str, quantity: int = 1,
                      item_type: str = "عام", rarity: str = "عام"):
        """Add item to inventory"""
        query = """INSERT INTO inventory(user_id, item, quantity, item_type, rarity)
                   VALUES(?, ?, ?, ?, ?)
                   ON CONFLICT(user_id, item) DO UPDATE SET quantity=quantity+excluded.quantity"""
        await self.execute(query, (user_id, item, quantity, item_type, rarity))
    
    async def remove_item(self, user_id: int, item: str, quantity: int = 1) -> bool:
        """Remove item from inventory"""
        row = await self.fetchone(
            "SELECT quantity FROM inventory WHERE user_id=? AND item=?",
            (user_id, item)
        )
        
        if not row or row["quantity"] < quantity:
            return False
        
        if row["quantity"] == quantity:
            await self.execute(
                "DELETE FROM inventory WHERE user_id=? AND item=?",
                (user_id, item)
            )
        else:
            await self.execute(
                "UPDATE inventory SET quantity=quantity-? WHERE user_id=? AND item=?",
                (quantity, user_id, item)
            )
        
        return True
    
    async def get_inventory(self, user_id: int) -> List[Dict]:
        """Get all inventory items"""
        return await self.fetchall(
            "SELECT item, quantity, item_type, rarity FROM inventory WHERE user_id=? ORDER BY item_type, item",
            (user_id,)
        )
    
    # ════════════════════════════════════════════════════════════════
    # COOLDOWN OPERATIONS
    # ════════════════════════════════════════════════════════════════
    
    async def set_cooldown(self, user_id: int, action: str, *,
                          minutes: int = 0, hours: int = 0, seconds: int = 0):
        """Set action cooldown"""
        until = datetime.now() + timedelta(minutes=minutes, hours=hours, seconds=seconds)
        query = """INSERT INTO cooldowns(user_id, action, until)
                   VALUES(?, ?, ?)
                   ON CONFLICT(user_id, action) DO UPDATE SET until=excluded.until"""
        await self.execute(query, (user_id, action, until.isoformat(timespec="seconds")))
    
    async def cooldown_remaining(self, user_id: int, action: str) -> int:
        """Get cooldown remaining in seconds"""
        row = await self.fetchone(
            "SELECT until FROM cooldowns WHERE user_id=? AND action=?",
            (user_id, action)
        )
        
        if not row:
            return 0
        
        remaining = datetime.fromisoformat(row["until"]) - datetime.now()
        return max(0, int(remaining.total_seconds()))
    
    # ════════════════════════════════════════════════════════════════
    # LEADERBOARD & STATS
    # ════════════════════════════════════════════════════════════════
    
    async def leaderboard(self, limit: int = 15) -> List[Dict]:
        """Get top players leaderboard"""
        query = """
        SELECT 
            display_name, char_class, gender, money, bank, level, xp, reputation,
            (money + bank + level*1000 + reputation*20) AS score
        FROM players
        ORDER BY score DESC
        LIMIT ?
        """
        return await self.fetchall(query, (limit,))
    
    async def get_rank(self, user_id: int) -> int:
        """Get player rank"""
        player = await self.get_player(user_id)
        if not player:
            return 0
        
        score = player["money"] + player["bank"] + player["level"]*1000 + player["reputation"]*20
        
        result = await self.fetchone(
            """SELECT COUNT(*) as count FROM players
               WHERE (money + bank + level*1000 + reputation*20) > ?""",
            (score,)
        )
        
        return result["count"] + 1 if result else 0
    
    # ════════════════════════════════════════════════════════════════
    # UTILITY
    # ════════════════════════════════════════════════════════════════
    
    async def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            log.info("✅ Database connection closed")
    
    async def backup(self, backup_path: str):
        """Create database backup"""
        import shutil
        async with self.lock:
            shutil.copy(self.db_path, backup_path)
        log.info(f"✅ Database backed up to {backup_path}")
