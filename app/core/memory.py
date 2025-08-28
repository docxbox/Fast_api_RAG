from __future__ import annotations

import json
from typing import Dict, List, Optional, Literal
import redis
from app.config import settings

class RedisChatMemory:
    def __init__(self, redis_url: str = settings.REDIS_URL, max_turns: int = settings.MAX_TURNS):
        self.redis_url = redis_url
        self.max_turns = max_turns
        self.max_messages = max(2 * self.max_turns, 2)
        self._redis: Optional[redis.Redis] = None

    def connect(self) -> None:
        self._redis = redis.from_url(self.redis_url, decode_responses=True)

    def close(self) -> None:
        if self._redis:
            self._redis.close()

    def _get_redis(self) -> redis.Redis:
        if self._redis is None:
            self.connect()
        return self._redis

    def _history_key(self, session_id: str) -> str:
        return f"chat:{session_id}:history"

    def append_message(self, session_id: str, role: Literal["user", "assistant", "system", "tool"], content: str) -> None:
        """ Append a message to the chat history """
        r = self._get_redis()
        item = json.dumps({"role": role, "content": content})
        r.rpush(self._history_key(session_id), item)
        r.ltrim(self._history_key(session_id), -self.max_messages, -1)

    def append_messages(self, session_id: str, messages: List[Dict[str, str]]) -> None:
        """ Append multiple messages to the chat history """
        if not messages:
            return
        r = self._get_redis()
        items = [json.dumps({"role": m["role"], "content": m["content"]}) for m in messages]
        r.rpush(self._history_key(session_id), *items)
        r.ltrim(self._history_key(session_id), -self.max_messages, -1)

    def _parse_messages(self, raw_messages: List[str]) -> List[Dict[str, str]]:
        out: List[Dict[str, str]] = []
        for x in raw_messages:
            try:
                obj = json.loads(x)
                if isinstance(obj, dict) and "role" in obj and "content" in obj:
                    out.append({"role": str(obj["role"]), "content": str(obj["content"])})
            except Exception:
                continue
        return out

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        r = self._get_redis()
        raw = r.lrange(self._history_key(session_id), 0, -1)
        return self._parse_messages(raw)

    def clear_history(self, session_id: str) -> None:
        r = self._get_redis()
        r.delete(self._history_key(session_id))

    def get_last_n(self, session_id: str, n: int) -> List[Dict[str, str]]:
        if n <= 0:
            return []
        r = self._get_redis()
        raw = r.lrange(self._history_key(session_id), -n, -1)
        return self._parse_messages(raw)