import sqlalchemy as db

class RetrieverLatest(object):
    def __init__(self):
        hostname="localhost"
        dbname="sample_tasks_quant"
        uname="root"
        pwd="root"

        self.engine = db.create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=dbname, user=uname, pw=pwd))
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()

    def get_current_data(self, tablename=['sample_tushare_data', 'sample_hkex_data']):
        census = db.Table()
        db.Table('sample_tushare_data', self.metadata, autoload=True, autoload_with=self.engine)