"""Who may triage what on the website.

- Anyone can run the free sample notes (SAMPLES).
- Your own notes need an access code: LINETRIAGE_ACCESS_CODES (comma-separated,
  for people you give access to) or LINETRIAGE_OWNER_CODE (yours: no rate limits).
- If neither variable is set (e.g. running locally), everything is open.
"""

import hmac
import os

SAMPLES = [
    {"tag": "EN", "text": "st2 guard on the robot cell is off bc the latch broke, we just keep going lol"},
    {"tag": "HU", "text": "2es hegesztonel a vesz-stop gomb beragadt, de megy a gep"},
    {"tag": "DE", "text": "ST07 Prüfung - Kratzer auf Gehäuse, ganze Charge, kein Stillstand"},
    {"tag": "REAL", "text": "WJ525 P/BRAKE FAULT"},
    {"tag": "EN", "text": "the big conveyor near the dock stopped again for like 20 min"},
]
SAMPLE_TEXTS = {s["text"] for s in SAMPLES}


class Access:
    def __init__(self, owner_code: str = "", member_codes: list[str] | None = None):
        self.owner_code = owner_code
        self.member_codes = [c for c in (member_codes or []) if c]

    @classmethod
    def from_env(cls) -> "Access":
        codes = os.environ.get("LINETRIAGE_ACCESS_CODES", "")
        return cls(os.environ.get("LINETRIAGE_OWNER_CODE", "").strip(), [c.strip() for c in codes.split(",")])

    @property
    def open(self) -> bool:
        return not self.owner_code and not self.member_codes

    def role(self, code: str) -> str:
        """'owner', 'member', 'open' (no codes configured) or 'guest'."""
        if self.open:
            return "open"
        code = (code or "").strip()
        if code and self.owner_code and hmac.compare_digest(code, self.owner_code):
            return "owner"
        if code and any(hmac.compare_digest(code, c) for c in self.member_codes):
            return "member"
        return "guest"


access = Access.from_env()
