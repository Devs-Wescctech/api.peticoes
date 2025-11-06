import os
import psycopg2
from urllib.parse import urlparse
from pathlib import Path

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/peticoes")
sql_file = Path(__file__).resolve().parents[1] / "app" / "migrations" / "001_initial_schema.sql"

def main():
    u = urlparse(DB_URL)
    dsn = f"dbname={u.path.lstrip('/')} user={u.username} password={u.password} host={u.hostname} port={u.port or 5432}"
    with psycopg2.connect(dsn) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(Path(sql_file).read_text(encoding="utf-8"))
    print("Migrations applied.")

if __name__ == "__main__":
    main()
