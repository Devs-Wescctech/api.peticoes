from sqlalchemy import text as sqltext

def petition_overview(session, petition_id: str):
    q = session.execute(sqltext("""
        SELECT p.id, p.title, p.goal, p.status,
               COUNT(s.id) AS signature_count,
               COALESCE(ROUND(COUNT(s.id)::NUMERIC / NULLIF(p.goal,0) * 100, 2), 0) AS progress_percentage,
               p.views_count, p.shares_count, p.created_date
          FROM petitions p
          LEFT JOIN signatures s ON s.petition_id = p.id
         WHERE p.id = :pid
         GROUP BY p.id
    """), {"pid": petition_id}).mappings().first()
    return dict(q) if q else None
