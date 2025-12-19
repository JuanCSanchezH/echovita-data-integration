# ruff: noqa
import pandas as pd

import duckdb

con = duckdb.connect("duckdb/echovita.db")

result = con.execute(open("duckdb/scd_consolidate.sql").read()).fetchall()

result_df = pd.DataFrame(result, columns=["person_id", "distinct_cities", "first_city", "last_city"])

print(result_df)
