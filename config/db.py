from sqlalchemy import create_engine, MetaData

engine = create_engine('mysql+pymysql://adminReposteria:123456789@127.0.0.1:3306/reposteriarosario')

meta_data = MetaData()