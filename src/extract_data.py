from sqlalchemy import MetaData, create_engine
from dotenv import dotenv_values
import pandas as pd
import datetime as dt

config = dotenv_values(".env")

db_url = config['SALE_CONNECTOR']
engine = create_engine(db_url)
connection = engine.connect()

def extract_transaction_log():
        query = """
                SELECT *
                FROM transactions AS t
                LEFT JOIN customers AS c ON t.customer_code = c.customer_code
                LEFT JOIN date AS d ON t.order_date = d.date
                LEFT JOIN markets AS m ON t.market_code = m.markets_code
                LEFT JOIN products AS p ON t.product_code = p.product_code
                """
        results = connection.execute(query).fetchall()
        df = pd.DataFrame(results)
        return df

def extract_transaction_log_with_date(begin,end):
        query = """
                SELECT *
                FROM transactions AS t
                LEFT JOIN customers AS c ON t.customer_code = c.customer_code
                LEFT JOIN date AS d ON t.order_date = d.date
                LEFT JOIN markets AS m ON t.market_code = m.markets_code
                LEFT JOIN products AS p ON t.product_code = p.product_code
                WHERE t.order_date >= '{}'
                AND t.order_date <= '{}'
                """.format(begin,end)
        results = connection.execute(query).fetchall()
        df = pd.DataFrame(results)
        return df



tl = extract_transaction_log()
tl['year'] = pd.to_datetime(tl['order_date']).dt.year
# customgroup = tl.groupby('markets_name').agg({'sales_amount':'sum','sales_qty':'sum'}).reset_index()
# top5_revenue = (customgroup.sort_values(by=['sales_amount'], ascending=False)).head(5)
# print(top5_revenue)
print(tl['year'])
