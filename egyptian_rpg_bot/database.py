# -*- coding: utf-8 -*-
"""database.py — SQLite DB layer — dev by 7amo"""
from __future__ import annotations
import asyncio,sqlite3
from datetime import datetime,timedelta
from typing import Any,Optional
from config import PLAYER_UPDATE_FIELDS, STAT_FIELDS, SKILL_FIELDS
from data.classes import STARTER_CLASSES, AGE_GROUPS
from data.quests import DEFAULT_QUESTS, GANGS

def now_str(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def clamp(v,lo=0,hi=100): return max(lo,min(hi,int(v)))

class ProDatabase:
    def __init__(self,fp):
        self.conn=sqlite3.connect(fp,check_same_thread=False)
        self.conn.row_factory=sqlite3.Row
        self.lock=asyncio.Lock()
        self._init()

    def _init(self):
        c=self.conn.cursor()
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA foreign_keys=ON")
        c.execute("""CREATE TABLE IF NOT EXISTS players(
            user_id INTEGER PRIMARY KEY,username TEXT,display_name TEXT,char_class TEXT,
            gender TEXT DEFAULT 'ولد',age_group TEXT,age INTEGER DEFAULT 23,
            job TEXT DEFAULT 'عاطل',job_xp INTEGER DEFAULT 0,job_rank TEXT DEFAULT '',
            money INTEGER DEFAULT 500,bank INTEGER DEFAULT 0,crypto INTEGER DEFAULT 0,
            health INTEGER DEFAULT 100,hunger INTEGER DEFAULT 100,thirst INTEGER DEFAULT 100,
            energy INTEGER DEFAULT 100,happiness INTEGER DEFAULT 100,hygiene INTEGER DEFAULT 80,
            fun INTEGER DEFAULT 50,fitness INTEGER DEFAULT 30,
            xp INTEGER DEFAULT 0,level INTEGER DEFAULT 1,
            house TEXT DEFAULT 'تحت الكوبري',car TEXT DEFAULT 'ماشي على رجلك',
            neighborhood TEXT DEFAULT 'بولاق',current_city TEXT DEFAULT 'القاهرة 🏙️',
            married_to INTEGER DEFAULT NULL,gang TEXT DEFAULT NULL,gang_rank TEXT DEFAULT NULL,
            programming_skill INTEGER DEFAULT 0,design_skill INTEGER DEFAULT 0,
            hacking_skill INTEGER DEFAULT 0,fighting_skill INTEGER DEFAULT 0,
            stealth_skill INTEGER DEFAULT 0,cooking_skill INTEGER DEFAULT 0,
            trading_skill INTEGER DEFAULT 0,football_skill INTEGER DEFAULT 0,
            streaming_skill INTEGER DEFAULT 0,music_skill INTEGER DEFAULT 0,
            acting_skill INTEGER DEFAULT 0,driving_skill INTEGER DEFAULT 0,
            charisma INTEGER DEFAULT 5,
            reputation INTEGER DEFAULT 0,wanted_level INTEGER DEFAULT 0,
            jail_until TEXT DEFAULT NULL,
            daily_streak INTEGER DEFAULT 0,total_earnings INTEGER DEFAULT 0,total_spent INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,updated_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        c.execute("""CREATE TABLE IF NOT EXISTS inventory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,
            item TEXT NOT NULL,quantity INTEGER DEFAULT 1,item_type TEXT DEFAULT 'عام',
            UNIQUE(user_id,item),FOREIGN KEY(user_id) REFERENCES players(user_id) ON DELETE CASCADE)""")
        c.execute("""CREATE TABLE IF NOT EXISTS cooldowns(
            user_id INTEGER NOT NULL,action TEXT NOT NULL,until TEXT NOT NULL,
            PRIMARY KEY(user_id,action))""")
        c.execute("""CREATE TABLE IF NOT EXISTS quests(
            id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,
            code TEXT NOT NULL,quest_name TEXT NOT NULL,completed INTEGER DEFAULT 0,
            progress INTEGER DEFAULT 0,target INTEGER DEFAULT 1,
            reward_money INTEGER DEFAULT 0,reward_xp INTEGER DEFAULT 0,reward_item TEXT DEFAULT NULL,
            UNIQUE(user_id,code),FOREIGN KEY(user_id) REFERENCES players(user_id) ON DELETE CASCADE)""")
        c.execute("""CREATE TABLE IF NOT EXISTS gangs(
            name TEXT PRIMARY KEY,leader_id INTEGER,territory TEXT,
            money INTEGER DEFAULT 0,reputation INTEGER DEFAULT 0,members_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        c.execute("""CREATE TABLE IF NOT EXISTS projects(
            id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,project_name TEXT,
            project_type TEXT,client_name TEXT,quality INTEGER DEFAULT 1,
            earnings INTEGER DEFAULT 0,success INTEGER DEFAULT 1,created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        c.execute("""CREATE TABLE IF NOT EXISTS criminal_records(
            id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,crime_type TEXT,
            severity INTEGER,caught INTEGER DEFAULT 0,fine INTEGER DEFAULT 0,
            jail_time INTEGER DEFAULT 0,date TEXT DEFAULT CURRENT_TIMESTAMP)""")
        c.execute("""CREATE TABLE IF NOT EXISTS assets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,
            asset_type TEXT NOT NULL,name TEXT NOT NULL,income INTEGER DEFAULT 0,
            sign TEXT DEFAULT '',last_collect TEXT DEFAULT NULL,
            UNIQUE(user_id,asset_type,name),FOREIGN KEY(user_id) REFERENCES players(user_id) ON DELETE CASCADE)""")
        c.execute("""CREATE TABLE IF NOT EXISTS transactions_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,action TEXT,
            amount INTEGER DEFAULT 0,details TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        c.execute("""CREATE TABLE IF NOT EXISTS gambling_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,game TEXT,
            bet INTEGER,won INTEGER DEFAULT 0,payout INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        c.execute("""CREATE TABLE IF NOT EXISTS pets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,
            name TEXT NOT NULL,pet_type TEXT NOT NULL,happiness INTEGER DEFAULT 80,
            hunger INTEGER DEFAULT 80,last_feed TEXT DEFAULT NULL,
            UNIQUE(user_id,name),FOREIGN KEY(user_id) REFERENCES players(user_id) ON DELETE CASCADE)""")
        for n,d in GANGS.items():
            c.execute("INSERT OR IGNORE INTO gangs(name,territory,members_count) VALUES(?,?,0)",(n,d["territory"]))
        self.conn.commit()

    async def fetchone(self,q,p=()):
        async with self.lock:
            return self.conn.execute(q,p).fetchone()
    async def fetchall(self,q,p=()):
        async with self.lock:
            return self.conn.execute(q,p).fetchall()
    async def execute(self,q,p=()):
        async with self.lock:
            self.conn.execute(q,p)
            self.conn.commit()
    async def executemany(self,q,p):
        async with self.lock:
            self.conn.executemany(q,p)
            self.conn.commit()

    async def get_player(self,uid): return await self.fetchone("SELECT * FROM players WHERE user_id=?",(uid,))

    async def create_player(self,user,name,char_class,age_group,gender="ولد"):
        b=STARTER_CLASSES[char_class]; a=AGE_GROUPS[age_group]
        hp=clamp(100+b.get("health",0)+a.get("health",0))
        en=clamp(100+b.get("energy",0)+a.get("energy",0))
        ha=clamp(100+b.get("happiness",0)+a.get("happiness",0))
        rep=b.get("reputation",0)+a.get("reputation",0)
        async with self.lock:
            self.conn.execute("""INSERT INTO players(
                user_id,username,display_name,char_class,gender,age_group,age,job,money,
                health,energy,happiness,fitness,
                programming_skill,design_skill,hacking_skill,fighting_skill,stealth_skill,
                cooking_skill,trading_skill,football_skill,streaming_skill,charisma,
                reputation,wanted_level) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (user.id,str(user),name[:32],char_class,gender,age_group,a["age"],
                 b.get("job","عاطل"),b.get("money",500),hp,en,ha,b.get("fitness",30),
                 b.get("programming_skill",0),b.get("design_skill",0),b.get("hacking_skill",0),
                 b.get("fighting_skill",0),b.get("stealth_skill",0),b.get("cooking_skill",0),
                 b.get("trading_skill",0),b.get("football_skill",0),b.get("streaming_skill",0),
                 b.get("charisma",5),rep,b.get("wanted_level",0)))
            for item,qty,itype in b.get("items",[]):
                self.conn.execute("INSERT OR IGNORE INTO inventory(user_id,item,quantity,item_type) VALUES(?,?,?,?)",(user.id,item,qty,itype))
            for q in DEFAULT_QUESTS:
                self.conn.execute("INSERT OR IGNORE INTO quests(user_id,code,quest_name,target,reward_money,reward_xp,reward_item) VALUES(?,?,?,?,?,?,?)",
                    (user.id,q["code"],q["name"],q["target"],q["money"],q["xp"],q.get("item")))
            self.conn.commit()

    async def update_player(self,uid,**kw):
        if not kw: return
        bad=set(kw)-PLAYER_UPDATE_FIELDS-{"current_city"}
        if bad: raise ValueError(f"Invalid fields: {bad}")
        kw["updated_at"]=now_str()
        a=", ".join([f"{k}=?" for k in kw])
        await self.execute(f"UPDATE players SET {a} WHERE user_id=?",tuple(kw.values())+(uid,))

    async def add_item(self,uid,item,qty=1,itype="عام"):
        await self.execute("INSERT INTO inventory(user_id,item,quantity,item_type) VALUES(?,?,?,?) ON CONFLICT(user_id,item) DO UPDATE SET quantity=quantity+excluded.quantity",(uid,item,qty,itype))

    async def remove_item(self,uid,item,qty=1):
        r=await self.fetchone("SELECT quantity FROM inventory WHERE user_id=? AND item=?",(uid,item))
        if not r or r["quantity"]<qty: return False
        if r["quantity"]==qty: await self.execute("DELETE FROM inventory WHERE user_id=? AND item=?",(uid,item))
        else: await self.execute("UPDATE inventory SET quantity=quantity-? WHERE user_id=? AND item=?",(qty,uid,item))
        return True

    async def get_inventory(self,uid):
        return await self.fetchall("SELECT item,quantity,item_type FROM inventory WHERE user_id=? ORDER BY item_type,item",(uid,))

    async def log(self,uid,action,amount=0,details=""):
        await self.execute("INSERT INTO transactions_log(user_id,action,amount,details) VALUES(?,?,?,?)",(uid,action,amount,details[:250]))

    async def set_cooldown(self,uid,action,*,minutes=0,hours=0,seconds=0):
        until=datetime.now()+timedelta(minutes=minutes,hours=hours,seconds=seconds)
        await self.execute("INSERT INTO cooldowns(user_id,action,until) VALUES(?,?,?) ON CONFLICT(user_id,action) DO UPDATE SET until=excluded.until",(uid,action,until.isoformat(timespec="seconds")))

    async def cooldown_remaining(self,uid,action):
        r=await self.fetchone("SELECT until FROM cooldowns WHERE user_id=? AND action=?",(uid,action))
        if not r: return 0
        return max(0,int((datetime.fromisoformat(r["until"])-datetime.now()).total_seconds()))

    async def progress_quest(self,uid,code,amount=1,*,absolute=False):
        r=await self.fetchone("SELECT * FROM quests WHERE user_id=? AND code=?",(uid,code))
        if not r or r["completed"]: return []
        np=amount if absolute else r["progress"]+amount
        done=np>=r["target"]; np=min(np,r["target"])
        await self.execute("UPDATE quests SET progress=?,completed=? WHERE user_id=? AND code=?",(np,1 if done else 0,uid,code))
        if done:
            p=await self.get_player(uid)
            if p:
                await self.update_player(uid, money=p["money"]+r["reward_money"], xp=p["xp"]+r["reward_xp"])
                if r["reward_item"]: await self.add_item(uid,r["reward_item"],1,"جائزة")
            return [f"✅ **مهمة اكتملت:** {r['quest_name']} | 💰{r['reward_money']:,} | ⭐{r['reward_xp']:,}"]
        return []

    async def leaderboard(self):
        return await self.fetchall("SELECT display_name,char_class,gender,money,bank,level,xp,reputation,(money+bank+level*1000+reputation*20) AS score FROM players ORDER BY score DESC LIMIT 15")

    async def log_gamble(self,uid,game,bet,won,payout):
        await self.execute("INSERT INTO gambling_history(user_id,game,bet,won,payout) VALUES(?,?,?,?,?)",(uid,game,bet,1 if won else 0,payout))

    async def add_pet(self,uid,name,pet_type):
        await self.execute("INSERT OR IGNORE INTO pets(user_id,name,pet_type) VALUES(?,?,?)",(uid,name,pet_type))

    async def get_pets(self,uid):
        return await self.fetchall("SELECT * FROM pets WHERE user_id=?",(uid,))

    async def delete_player(self,uid):
        for t in ["inventory","cooldowns","quests","projects","criminal_records","assets","transactions_log","gambling_history","pets"]:
            await self.execute(f"DELETE FROM {t} WHERE user_id=?",(uid,))
        await self.execute("DELETE FROM players WHERE user_id=?",(uid,))
