WITH valid_from_asc_or_desc AS (
    SELECT person_id, city, CAST(valid_from AS DATE),
        -- first row ordered by valid_from
        ROW_NUMBER() OVER (
            PARTITION BY person_id
            ORDER BY valid_from
        ) AS rn_asc,
        -- last row ordered by valid_from
        ROW_NUMBER() OVER (
            PARTITION BY person_id
            ORDER BY valid_from DESC
        ) AS rn_desc

    FROM person_history
)
SELECT
    person_id,
    -- Number of distinct cities
    COUNT(DISTINCT city) AS distinct_cities,
    -- First city in time
    MAX(CASE WHEN rn_asc = 1 THEN city END) AS first_city,
    -- Last city in time
    MAX(CASE WHEN rn_desc = 1 THEN city END) AS last_city,
FROM valid_from_asc_or_desc
GROUP BY person_id;