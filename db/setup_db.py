from sqlalchemy import text

from .config import ENGINE


def setup_db():
    with open('/app/db/sql_query_create_table.txt', 'r') as f:
        crate_table_query = f.read()
    with ENGINE.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS autoria_cars"))
        conn.execute(text(crate_table_query))