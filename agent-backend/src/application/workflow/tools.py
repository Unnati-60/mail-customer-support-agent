

# def execute_sql(query: str, db_path: str) -> pd.DataFrame:
#     """
#     Execute any SELECT over the event-sourced 'transactions' table.
#     """
#     q = query.strip().removeprefix("```sql").removesuffix("```").strip()
#     conn = sqlite3.connect(db_path)
#     try:
#         return pd.read_sql_query(q, conn)
#     except Exception as e:
#         return pd.DataFrame({"error": [str(e)]})
#     finally:
#         conn.close()