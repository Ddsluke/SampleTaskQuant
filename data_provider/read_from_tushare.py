# 导入tushare
import tushare as ts

class TushareReader():
    def __init__(self, *args, **kwargs):
        # 初始化pro接口
        self.pro = ts.pro_api('5d12fd005a33f96b664b0a393e72288545d2dfd6723be471c0bdb47f')
        self.args = args
        self.kwargs = kwargs
        print(args, kwargs)

    def pull(self):
        df = self.pro.daily(*self.args, **self.kwargs)
        return df

if __name__ == "__main__":
    cfg = {
        "ts_code": "",
        "trade_date": "",
        "start_date": 20170904, # past 5 years
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
    reader.pull()