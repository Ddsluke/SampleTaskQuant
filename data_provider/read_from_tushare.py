# 导入tushare
import tushare as ts

class TushareReader():
    def __init__(self, cfg, fields=None):
        # 初始化pro接口
        self.pro = ts.pro_api('5d12fd005a33f96b664b0a393e72288545d2dfd6723be471c0bdb47f')
        self.cfg = cfg
        self.fields = fields

    def run(self):
        df = self.pro.daily(**self.cfg, fields=fields)
        return df

if __name__ == "__main__":
    import datetime
    today = datetime.date.today().strftime(r'%Y%m%d')
    past = int(today) - 50000
    cfg = {
        "ts_code": "000001.SZ", # sample ts code
        "trade_date": "",
        "start_date": past, # past 5 years
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
    print(reader.run())