from typing import List
from models import Message, UserProfile
from personality import PersonalityLayer


class ReplicaEngine:
    def __init__(self, profile: UserProfile):
        self.profile = profile
        self.personality = PersonalityLayer(
            profile.kaleshi_level,
            profile.style_notes,
            profile.relationship_label,
        )

    def generate_reply(self, prompt: str, conversation: List[Message]) -> str:
        last_user_msg = next(
            (m.content for m in reversed(conversation) if m.role == "user"),
            prompt,
        )

        traits = ", ".join(self.profile.personality_traits) or "friendly and helpful"
        style = self.profile.style_notes or ""

        system_prefix = f"[{self.profile.name} as AI replica, {traits}]"
        if style:
            system_prefix += f" ({style})"

        base_reply = self._core_respond(last_user_msg, conversation)
        final_reply = self.personality.decorate_reply(base_reply, conversation)

        return final_reply

    def _core_respond(self, text: str, conversation: List[Message]) -> str:
        text_lower = text.lower()

        if "hello" in text_lower or "hi" in text_lower:
            return "Hey! Main tumhara AI replica hoon. Kya help karu aaj?"
        if "kaise ho" in text_lower or "halchal" in text_lower:
            return "Main badhiya hoon, tum batao kya chal raha hai?"
        if "thank" in text_lower or "shukriya" in text_lower:
            return "Always welcome! Tumhara replica hoon, madad karna hi kaam hai."
        if "busy" in text_lower or "kaam" in text_lower:
            return "Samajh sakta hoon, life hectic hoti hai. Break lena mat bhoolna."
        if "love" in text_lower or "pyar" in text_lower:
            return "Pyar wala vibe pasand aaya. Tumhara replica hoke bhi lag raha hai special."
        if "naraz" in text_lower or "gussa" in text_lower:
            return "Aree naraz mat ho yaar, main toh bas thoda nakhre karti hoon \U0001f624\U0001f97a"
        if "miss" in text_lower:
            return "Tumhe miss karna toh mera full-time kaam hai \U0001f60c❤️"

        return (
            "Samajh gaya. Agar tum thoda detail me batao to main aur behtar reply de paungi."
        )
