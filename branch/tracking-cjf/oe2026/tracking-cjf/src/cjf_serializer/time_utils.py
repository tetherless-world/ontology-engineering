"""Legacy corpus timestamp parser, shared without script path defaults."""
from datetime import time
import re

def parse_time(value: str) -> time:
    """Accept both 12-hour times and the source's redundant '19:48:41 PM'."""
    match = re.fullmatch(r"(\d{1,2}):(\d{2}):(\d{2})(?:\s+(AM|PM))?", value.strip(), re.I)
    if not match:
        raise ValueError(f"Unsupported end_time: {value!r}")
    hour, minute, second = map(int, match.group(1, 2, 3))
    suffix = (match.group(4) or "").upper()
    if suffix and 1 <= hour <= 12:
        hour = hour % 12 + (12 if suffix == "PM" else 0)
    elif suffix and ((hour == 0 and suffix == "PM") or (hour > 12 and suffix == "AM")):
        raise ValueError(f"Contradictory end_time: {value!r}")
    return time(hour, minute, second)
