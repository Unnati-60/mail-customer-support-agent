from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import pandas as pd
from src.config import settings


class PostgreDb:
    def __init__(self):
        self.engine = create_engine(settings.POSTGRES_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()


    def get_schema(self) -> str:
        """
        Returns schema of all tables in PostgreSQL (public schema).
        Uses pandas.read_sql_query for cleaner data access.
        """
        schema_sql = """
        SELECT 
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """

        df = pd.read_sql_query(schema_sql, self.engine)      # equivalent to session.execute(text(schema_sql)).fetchall()

        if df.empty:
            return "No tables found."

        output = []
        current_table = None

        for _, row in df.iterrows():
            table_name = row["table_name"]
            col_name = row["column_name"]
            dtype = row["data_type"]

            if table_name != current_table:
                output.append(f"\nTable: {table_name}")
                current_table = table_name

            output.append(f"  - {col_name} ({dtype})")

        return "\n".join(output)


    def execute_sql(self, query: str):
        """
        Executes SELECT queries and returns dataframe converted to list of dicts.
        """
        q = query.strip().removeprefix("```sql").removesuffix("```").strip()
        

        forbidden = ["insert", "update", "delete", "drop", "alter"]
        if any(f in q.lower() for f in forbidden):
            return pd.DataFrame({"error": "Only SELECT queries are allowed."})

        try:
            df = pd.read_sql_query(q, self.engine)
            return df

        except Exception as e:
            print(f"SQL execution error: {e}")
            return pd.DataFrame({"error": [str(e)]})

if __name__ == "__main__":
    db = PostgreDb()

    print(db.get_schema())

    rows = db.execute_sql("SELECT * FROM customers LIMIT 5;")
    print(rows)
