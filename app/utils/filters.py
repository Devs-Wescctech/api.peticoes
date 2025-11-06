def like(term: str) -> str:
    return f"%{term.replace('%','')}%"
