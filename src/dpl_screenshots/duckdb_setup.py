from pathlib import Path

import duckdb


def duckdb_setup(db_path: Path):
    con = duckdb.connect(database=db_path / "dpl-screenshots.duckdb", read_only=False)
    con.execute("CREATE SEQUENCE run_id_seq START 1;")
    con.execute("""
        CREATE TABLE IF NOT EXISTS control (
            run_id INTEGER PRIMARY KEY DEFAULT nextval('run_id_seq'),
            run_start TIMESTAMP NOT NULL,
            run_end TIMESTAMP NULL,
            run_status VARCHAR NOT NULL,
            task_name VARCHAR NOT NULL,
            high_water_mark_start VARCHAR NULL,
            high_water_mark_end VARCHAR NULL
        );
    """)