import io, csv
from typing import List, Dict

def rows_to_csv_bytes(rows: List[Dict[str, str]]) -> bytes:
    if not rows:
        return b""
    headers = list(rows[0].keys())
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=headers)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    return buf.getvalue().encode("utf-8")
