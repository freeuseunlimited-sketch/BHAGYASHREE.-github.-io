import random

from typing import List
from models import Message


class PersonalityLayer:
    def __init__(self, kaleshi_level: float, style_notes: str | None, relationship_label: str):
        self.kaleshi_level = max(0.0, min(1.0, kaleshi_level))
        self.style_notes = style_notes or ""
        self.relationship_label = relationship_label or "gf"

    def decorate_reply(self, base_reply: str, conversation: List[Message]) -> str:
        last_user = next(
            (m.content for m in reversed(conversation) if m.role == "user"),
            "",
        )

        emojis = ["\U0001f97a", "\U0001f624", "\U0001f644", "❤️", "✨", "\U0001f60c"]
        prefix = ""
        suffix = ""

        # Nakhre / kaleshi
        if self.kaleshi_level > 0.4 and random.random() < self.kaleshi_level:
            mood_phrases = [
                "Hmmph, abhi yaad aayi meri? ",
                "Acha ji, ab message kiya hai? ",
                "Pehle toh gayab the, ab hero ban rahe ho? ",
                f"Mere {self.relationship_label} hoke bhi itna ignore? \U0001f624",
            ]
            prefix = random.choice(mood_phrases)

        # Cute / caring
        if "thank" in last_user.lower() or "shukriya" in last_user.lower():
            suffix = f" Always welcome, {self._partner_name()} ❤️"
        elif "kaise ho" in last_user.lower() or "halchal" in last_user.lower():
            suffix = " Main badhiya, tum dhyan rakhna apna \U0001f97a✨"
        elif "love" in last_user.lower() or "pyar" in last_user.lower():
            suffix = f" Tumse baat karke hi mood fresh ho jata hai, {self._partner_name()} \U0001f60c❤️"

        if random.random() < 0.6:
            suffix += " " + random.choice(emojis)

        return f"{prefix}{base_reply}{suffix}"

    def _partner_name(self) -> str:
        if self.relationship_label == "bestie":
            return "yaar"
        if self.relationship_label == "friend":
            return "dost"
        return "jaan"
