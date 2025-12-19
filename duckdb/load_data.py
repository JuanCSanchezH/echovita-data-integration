# ruff: noqa
import duckdb

con = duckdb.connect("duckdb/echovita.db")

con.execute(
    """
    CREATE OR REPLACE TABLE person_history AS
    SELECT
        person_id,
        name,
        state,
        city,
        valid_from AS valid_from,
        valid_to AS valid_to
    FROM read_csv_auto('duckdb/person_history.csv')
    """
)

print("Table person_history created successfully")
