import sqlalchemy as db
import datetime

class Retriever(object):
    def __init__(self):
        hostname="localhost"
        dbname="sample_tasks_quant"
        uname="root"
        pwd="root"

        self.engine = db.create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=dbname, user=uname, pw=pwd))
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()

    @property
    def _current_date():
        today = datetime.date.today().strftime(r'%Y%m%d')
        return str(today)

    def get_current_data(self, tablename='sample_hkex_data', datekey='Date'): # another solution is to get LATEST data using orderby
        sample_data = db.Table(tablename, self.metadata, autoload=True, autoload_with=self.engine)
        
        get_datekey = lambda x: getattr(x, datekey, None)
        query = db.select([sample_data]).where(get_datekey(sample_data.columns) == self._current_date)
        result_proxy = self.connection.execute(query)

        return result_proxy.fetchall()

    def get_historical_data(self, tablename='sample_hkex_data'):
        sample_data = db.Table(tablename, self.metadata, autoload=True, autoload_with=self.engine)
        query = db.select([sample_data])
        result_proxy = self.connection.execute(query)

        return result_proxy.fetchall()


if __name__ == '__main__':
    retriever = Retriever()
    print(retriever.get_current_data())
    print(retriever.get_historical_data())