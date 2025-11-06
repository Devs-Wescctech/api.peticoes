from typing import Tuple

def normalize_pagination(limit: int | None, offset: int | None, max_limit: int = 200) -> Tuple[int, int]:
    l = limit if (limit and limit > 0) else 50
    l = min(l, max_limit)
    o = offset if (offset and offset >= 0) else 0
    return l, o
