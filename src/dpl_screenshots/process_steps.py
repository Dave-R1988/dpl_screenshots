import inspect
from pathlib import Path
from typing import Tuple

import duckdb


def setup_db(db_directory: Path):
    con = duckdb.connect(database=db_directory / "dpl-screenshots.duckdb", 
                         read_only=False)
    con.execute("CREATE SEQUENCE IF NOT EXISTS run_id_seq START 1;")
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

    con.execute("""
        CREATE TABLE IF NOT EXISTS imagefile_hub (
            imagefile_hkey VARCHAR PRIMARY KEY,
            imagefile_path VARCHAR NOT NULL,
            inscription_timestamp TIMESTAMP NOT NULL
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS next_imagefile_link (
            next_imagefile_link_hkey VARCHAR PRIMARY KEY,
            previous_imagefile_hkey VARCHAR NOT NULL,
            next_imagefile_hkey VARCHAR NOT NULL,
            inscription_timestamp TIMESTAMP NOT NULL
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS textfile_hub (
            textfile_hkey VARCHAR PRIMARY KEY,
            textfile_path VARCHAR NOT NULL,
            inscription_timestamp TIMESTAMP NOT NULL
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS ocr_link (
            ocr_link_hkey VARCHAR PRIMARY KEY,
            imagefile_hkey VARCHAR NOT NULL,
            textfile_hkey VARCHAR NOT NULL,
            inscription_timestamp TIMESTAMP NOT NULL
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS next_textfile_link (
            next_textfile_link_hkey VARCHAR PRIMARY KEY,
            previous_textfile_hkey VARCHAR NOT NULL,
            next_textfile_hkey VARCHAR NOT NULL,
            inscription_timestamp TIMESTAMP NOT NULL
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS longest_common_substring_sat (
            next_textfile_link_hkey VARCHAR PRIMARY KEY,
            inscription_timestamp TIMESTAMP NOT NULL,
            inscription_record_id UINTEGER NOT NULL,
            longest_common_substring_length UBIGINT NULL
        );
    """)    


def get_previous_hwm(db_path: Path, task_name: str) -> Tuple[str] | None:
    con = duckdb.connect(database=db_path, read_only=True)
    con.execute("""
        SELECT
            high_water_mark_end
        FROM control
        WHERE run_id = (
            SELECT
                MAX(run_id)
            FROM control
            WHERE task_name = ?
            AND run_status = 'Succeeded'
        ) a;
        """,[task_name])
    return con.fetchone()


def control_start(db_path: Path, task_name: str) -> int | None:
    con = duckdb.connect(database=db_path, read_only=False)

    # start the run ...
    con.execute("""
        INSERT INTO control
        (
            run_start,
            run_status,
            task_name,
        )
        VALUES
        (
            current_timestamp,
            'Running',
            ?
        );
    """,[task_name])

    # ... and return him his run_id:
    con.execute("""
        SELECT
            run_id
        FROM control
        WHERE task_name = ?
        AND run_status = 'Running';
        """,[task_name])
    return con.fetchone()


def control_end(db_path: Path, task_name: str, run_id: int, 
                high_water_mark_start: str, high_water_mark_end: str):
    con = duckdb.connect(database=db_path, read_only=False)

    # end the run ...
    con.execute("""
        UPDATE control
            SET
                run_end = current_timestamp,
                run_status = 'Succeeded',
                high_water_mark_start = ?,
                high_water_mark_end = ?
        WHERE
            task_name = ?
            AND run_id = ?
        ;
    """,[high_water_mark_start, high_water_mark_end, task_name, run_id])


def load_imagefiles(db_path: Path,
                    input_dir: Path | None,  
                    max_batch_size: int = 100) -> int | None:
    task_name = inspect.currentframe().f_code.co_name

    run_id = control_start(db_path, task_name)
    if run_id is None: # failed to log the run start in the db
        return None

    files = list(input_dir.glob('**/*'))
    if len(files) == 0: # input_dir is empty - there is nothing to do
        return run_id
    
    previous_hwm = get_previous_hwm(db_path, task_name)

    if previous_hwm is None:
        hwm_idx = 0
    else:
        try:
            hwm_idx = files.index(Path(previous_hwm[0]))
        except ValueError:
            return None
        
    files = files[hwm_idx:min(hwm_idx + max_batch_size,len(files)-1)]

    for file in files:
        pass

    control_end(db_path, task_name, run_id, str(files[0]), str(files[-1]))
