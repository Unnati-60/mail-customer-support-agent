import json
from pathlib import Path

import opik
import uuid

from src.infrastructure import opik_utils
from src.infrastructure.postgreDb import PostgreDb
from src.utils import normalize_db_output



def upload_dataset(name: str, data_path: Path) -> opik.Dataset:
    assert data_path.exists(), f"File {data_path} does not exist."

    with open(data_path, "r", encoding="utf-8") as f:
        evaluation_data = json.load(f)

    db_client = PostgreDb()
    dataset_items = []

    for sample in evaluation_data:
        if len(sample["expected_sql_output"]) <= 1:
            df = db_client.execute_sql(sample["expected_sql"][0])
            raw_rows = df.to_dict(orient="records")

            safe_rows = normalize_db_output(raw_rows)

            sample["expected_sql_output"].append(safe_rows)

        dataset_items.append(
            {
                "customer_mail": sample["customer_mail"],
                "expected_sql": sample["expected_sql"],
                "expected_sql_output": sample["expected_sql_output"],
                "query_type": sample["query_type"],
                "labels": sample["labels"],
            }
        )


    dataset = opik_utils.create_dataset(
        name=name,
        description="Dataset containing customer mails and queries.",
        items=dataset_items,
    )

    return dataset
