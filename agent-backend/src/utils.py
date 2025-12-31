from datetime import date, datetime
from decimal import Decimal

def normalize_db_output(rows: list[dict]) -> list[dict]:
    normalized = []
    for row in rows:
        clean_row = {}
        for k, v in row.items():
            if isinstance(v, (date, datetime)):
                clean_row[k] = v.isoformat()
            elif isinstance(v, Decimal):
                clean_row[k] = float(v)
            else:
                clean_row[k] = v
        normalized.append(clean_row)
    return normalized