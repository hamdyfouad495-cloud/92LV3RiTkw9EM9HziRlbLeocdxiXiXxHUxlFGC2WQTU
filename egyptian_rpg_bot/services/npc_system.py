# -*- coding: utf-8 -*-
"""
NPC AI System - Creates living, breathing NPCs with personalities and routines
"""

import random
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, time

class NPCPersonality(Enum):
    """NPC personality types"""
    FRIENDLY = "ودود"
    GRUMPY = "عبيط"
    BUSINESS = "تاجر"
    CRAZY = "مجنون"
    LAZY = "كسول"
    HARDWORKING = "شغيل"

class NPC:
    """Base NPC class with personality, mood, and routine"""
    
    def __init__(self, name: str, npc_type: str, personality: NPCPersonality):
        self.name = name
        self.npc_type = npc_type
        self.personality = personality
        self.mood = 50  # 0-100
        self.location = "الشارع"
        self.routine = {}
        self.relationships = {}  # Other NPCs they like/dislike
        self.money = random.randint(1000, 10000)
        self.reputation = 0
        self.energy = 100
        self.hunger = 50
    
    def get_greeting(self) -> str:
        """Return mood-based greeting"""
        greetings = {
            NPCPersonality.FRIENDLY: [
                "أهلاً بيك يا صديقي! 😊",
                "شنيك يا معلم؟ 🤝",
                "تمام التمام؟ 👋",
            ],
            NPCPersonality.GRUMPY: [
                "هاااه؟ إيه بتقول؟ 😤",
                "سيبك عني! 🚫",
                "روح من هنا! 💢",
            ],
            NPCPersonality.BUSINESS: [
                "تمام؟ في صفقة معاك؟ 💼",
                "كام اللي بتشتري؟ 💰",
                "حاجة تانية؟ 🤔",
            ],
            NPCPersonality.CRAZY: [
                "يالا نلعب! 🎮😵",
                "أنا ملك العالم! 👑😂",
                "عايز تسمع حكاية؟ 📖✨",
            ],
        }
        
        personality_greetings = greetings.get(self.personality, [])
        if self.mood > 70:
            return random.choice(personality_greetings + ["أهلاً يا باشا! 🌟"])
        elif self.mood < 30:
            return "خليني وحالي... 😠"
        else:
            return random.choice(personality_greetings)
    
    def get_reply(self, message: str) -> str:
        """Generate NPC reply based on personality and mood"""
        reactions = {
            NPCPersonality.FRIENDLY: [
                "ماشي يا صديقي! 👍",
                "تمام يا معلم! ✨",
                "أنت كويس! 😊",
            ],
            NPCPersonality.GRUMPY: [
                "طيب... 😒",
                "شنيك أنت! 🙄",
                "روح لحد تاني! 🚶",
            ],
            NPCPersonality.BUSINESS: [
                "كويس! في فلوس؟ 💰",
                "ماشي! التمن كام؟ 💳",
                "تمام! هقول لك السعر! 📊",
            ],
        }
        
        replies = reactions.get(self.personality, ["..."])
        return random.choice(replies)
    
    def update_mood(self):
        """Update NPC mood based on current state"""
        mood_changes = 0
        
        # Energy affects mood
        if self.energy < 20:
            mood_changes -= 10
        
        # Hunger affects mood
        if self.hunger > 80:
            mood_changes -= 5
        
        # Random events
        if random.random() < 0.1:
            mood_changes += random.randint(-10, 10)
        
        self.mood = max(0, min(100, self.mood + mood_changes))
    
    def work_routine(self, hour: int):
        """Execute work routine based on time of day"""
        if 6 <= hour < 9:
            self.location = "البيت"
            self.energy -= 5
        elif 9 <= hour < 17:
            self.location = self.get_work_location()
            self.energy -= 15
            self.hunger += 5
        elif 17 <= hour < 20:
            self.location = "المقهى"
            self.energy -= 10
            self.hunger += 10
        else:
            self.location = "البيت"
            self.energy += 20
    
    def get_work_location(self) -> str:
        """Get NPC work location based on type"""
        locations = {
            "بلطجي": ["الشارع", "الحارة", "الميدان"],
            "موظف": ["المكتب", "الشارع", "البنك"],
            "تاجر": ["المتجر", "السوق", "الشارع"],
            "ميكانيكي": ["الورشة", "الشارع"],
        }
        return random.choice(locations.get(self.npc_type, ["الشارع"]))

class NPCManager:
    """Manages all NPCs in the game world"""
    
    def __init__(self):
        self.npcs: Dict[str, NPC] = {}
        self.initialize_npcs()
    
    def initialize_npcs(self):
        """Create initial NPCs"""
        npc_data = [
            ("جمال", "بلطجي", NPCPersonality.GRUMPY),
            ("أحمد", "موظف", NPCPersonality.FRIENDLY),
            ("سالم", "تاجر", NPCPersonality.BUSINESS),
            ("عماد", "ميكانيكي", NPCPersonality.HARDWORKING),
            ("خالد", "عاطل", NPCPersonality.LAZY),
            ("محمود", "ستريمر", NPCPersonality.CRAZY),
            ("فاطمة", "سيدة متجر", NPCPersonality.FRIENDLY),
            ("نور", "طالبة", NPCPersonality.FRIENDLY),
            ("ياسين", "بلطجي", NPCPersonality.GRUMPY),
            ("ناصف", "تاجر", NPCPersonality.BUSINESS),
        ]
        
        for name, npc_type, personality in npc_data:
            self.npcs[name] = NPC(name, npc_type, personality)
    
    def get_npc(self, name: str) -> Optional[NPC]:
        """Get NPC by name"""
        return self.npcs.get(name)
    
    def get_npc_by_type(self, npc_type: str) -> List[NPC]:
        """Get all NPCs of a specific type"""
        return [npc for npc in self.npcs.values() if npc.npc_type == npc_type]
    
    def get_npc_at_location(self, location: str) -> List[NPC]:
        """Get all NPCs at a location"""
        return [npc for npc in self.npcs.values() if npc.location == location]
    
    def update_all_npcs(self, hour: int):
        """Update all NPCs (call this hourly)"""
        for npc in self.npcs.values():
            npc.work_routine(hour)
            npc.update_mood()
            
            # Hunger increases with time
            npc.hunger = min(100, npc.hunger + 1)
            npc.energy = max(0, npc.energy - 1)

class DialogueSystem:
    """Manages conversations with NPCs"""
    
    def __init__(self):
        self.dialogue_trees = {}
        self.initialize_dialogues()
    
    def initialize_dialogues(self):
        """Set up dialogue trees for interactions"""
        pass
    
    def get_dialogue_options(self, npc: NPC, context: str = "greeting") -> List[str]:
        """Get available dialogue options with NPC"""
        options = []
        
        if context == "greeting":
            options = [
                "📝 اسأل عن الوظائف",
                "💰 عرض للتجارة",
                "⚔️ تحدي",
                "😊 دردشة عادية",
                "👋 وداعاً"
            ]
        
        return options
