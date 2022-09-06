import sys
sys.path.append(r"C:\Users\A\quant")
from sqlalchemy import create_engine
from data_provider import *

class DBParser(object):
    def __init__(self, hostname, dbname, uname, pwd):
        self.engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
            .format(host=hostname, db=dbname, user=uname, pw=pwd))

    def save_table(self, df, tablename):
        df.to_sql(tablename, self.engine, index=False)


if __name__ == "__main__":
    hostname="localhost"
    dbname="sample_tasks_quant"
    uname="root"
    pwd="root"

    parser = DBParser(hostname, dbname, uname, pwd)

    cfg = {
        "ts_code": "000001.SZ", # sample ts code
        "trade_date": "",
        "start_date": 20170906, # past 5 years
        "end_date": "",
        "offset": "",
        "limit": ""
        }

    fields = [
            "ts_code",
            "trade_date",
            "open",
            "high",
            "low",
            "close",
            "pre_close",
            "change",
            "pct_chg",
            "vol",
            "amount"
        ]

    reader = TushareReader(cfg, fields=fields) 
    res_df = reader.run()

    parser.save_table(res_df, 'sample_tushare_data')

    reader = HKEXReader("20220904", "Shanghai Connect Southbound")
    res_df = reader.run()
    res_df.insert(0, 'Date', "20220904")
    res_df.insert(res_df.shape[1], 'Connect', 'Shanghai_Connect_Southbound')

    parser.save_table(res_df, 'sample_hkex_data')
    

