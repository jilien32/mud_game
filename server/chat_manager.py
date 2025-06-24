class ChatManager:
    def __init__(self, players):
        self.players = players

    def chat_room(self, sender_id, message):
        sender = self.players[sender_id]
        loc = sender.get_location()
        msgs = []
        for uid, p in self.players.items():
            if uid != sender_id and p.get_location() == loc:
                msgs.append((uid, f"{sender_id} ▶ {message}"))
        return msgs

    def chat_group(self, sender_id, message):
        sender = self.players[sender_id]
        grp = getattr(sender, "group", None)
        if not grp:
            return []
        msgs = []
        for uid, p in self.players.items():
            if uid != sender_id and getattr(p, "group", None) == grp:
                msgs.append((uid, f"[그룹]{sender_id} ▶ {message}"))
        return msgs

    def chat_global(self, sender_id, message):
        return [
            (uid, f"[잡담]{sender_id} ▶ {message}")
            for uid in self.players
            if uid != sender_id
        ]

    def chat_whisper(self, sender_id, target_id, message):
        if target_id in self.players:
            return [(target_id, f"[귓속말]{sender_id} ▶ {message}")]
        return []
