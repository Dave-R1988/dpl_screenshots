import inspect
from pathlib import Path

import cv2
import duckdb
import pytesseract


def process_screenshots_extract_text(output_dir: Path, 
                                     input_dir: Path | None, 
                                     db_path: Path, 
                                     max_batch_size: int = 0) -> Path | None:
    # get the last high-water mark from the control table:
    task_name = inspect.currentframe().f_code.co_name
    con = duckdb.connect(database=db_path, read_only=False)
    con.execute("""
        SELECT
            high_water_mark_end,
            task_status
        FROM control
        WHERE run_id = (
            SELECT
                MAX(run_id)
            FROM control
            WHERE task_name = ?
        ) a;
    """,[task_name])
    previous_hwm = con.fetchone()

    # there was a previous run, but not (yet) successful - do nothing
    if previous_hwm is not None and previous_hwm[2] != 'Succeeded':
        return None

    # log the start of our run:
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
        )
    """,[task_name])

    i = 0
    if previous_hwm is None:

        if input_dir is None:
            raise ValueError("An input directory must be specified for the first run")
        
        for file in input_dir.glob('**/*'):
            if file.is_file() and file.suffix == '.jpg':
                image = cv2.imread(file)
                image_str = pytesseract.image_to_string(image)
                output_file = output_dir / file.name
                output_file.write_text(image_str)
                i += 1
                if max_batch_size > 0 and i >= max_batch_size:
                    break

    # determine our starting file: 'next' file after last high_water_mark
