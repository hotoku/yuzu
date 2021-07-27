from sys import argv
from google.cloud import bigquery
from yuzu.cache import cache

bqclient = bigquery.Client()


@cache(ignore_args=[0])
def query(client: bigquery.Client, sql: str):
    ret = client.query(sql).to_dataframe()
    return ret


team = argv[1]

sql = f"""
SELECT
  awayTeamName
FROM
  `bigquery-public-data.baseball.schedules`
WHERE
  homeTeamName = '{team}'
ORDER BY
  startTime
LIMIT
  1
"""


df = query(bqclient, sql)
print(f"First opponent is {df.iloc[0, 0]}")
